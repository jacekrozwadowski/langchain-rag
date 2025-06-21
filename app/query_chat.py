import os
from typing import Dict
from langchain_elasticsearch import ElasticsearchRetriever
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState, StateGraph
from langchain_core.tools import tool
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":

    # llm/embedding setup
    llm = init_chat_model("gpt-4.1-nano", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Prepare hybrid query to ES
    def hybrid_query(search_query: str) -> Dict:
        terms = ["hr"]
        vector = embeddings.embed_query(search_query)  # same embeddings as for indexing

        return {
            "query": {
                "bool": {
                    "must": {"match": {"text": {"query": search_query, "boost": 0.5}}},
                    "filter": {
                        "terms_set": {
                            "metadata.tags": {
                                "terms": terms,
                                "minimum_should_match_script": {
                                    "source": "params.num_terms"
                                },
                            }
                        }
                    },
                }
            },
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": 5,
                "num_candidates": 10,
                "boost": 0.5,
                "filter": {
                    "terms_set": {
                        "metadata.tags": {
                            "terms": terms,
                            "minimum_should_match_script": {
                                "source": "params.num_terms"
                            },
                        }
                    }
                },
            },
            "size": 5,
        }

    # prepare retriever
    hybrid_retriever = ElasticsearchRetriever.from_es_params(
        index_name=os.environ["ES_INDEX"],
        body_func=hybrid_query,
        content_field="text",
        url=os.environ["ES_URL"],
        username=os.environ["ES_USERNAME"],
        password=os.environ["ES_PASSWORD"],
    )

    # retriever tool used in graph
    @tool(response_format="content_and_artifact")
    def retrieve(query: str):
        """Retrieve information related to a query."""
        retrieved_docs = hybrid_retriever.invoke(query)
        serialized = "\n\n".join(
            (
                f"Source: {doc.metadata['_source']['metadata']}\n"
                f"Content: {doc.page_content}"
            )
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    # generate new query or response based on original query content
    def query_or_respond(state: MessagesState):
        """Generate tool call for retrieval or respond."""
        llm_with_tools = llm.bind_tools([retrieve])
        response = llm_with_tools.invoke(state["messages"])
        # MessagesState appends messages to state instead of overwriting
        return {"messages": [response]}

    # Step 2: Execute the retrieval.
    tools = ToolNode([retrieve])

    # generate a response using the retrieved content.
    def generate(state: MessagesState):
        """Generate answer."""
        # Get generated ToolMessages
        recent_tool_messages = []
        for message in reversed(state["messages"]):
            if message.type == "tool":
                recent_tool_messages.append(message)
            else:
                break
        tool_messages = recent_tool_messages[::-1]
        # print(tool_messages)

        # Format into prompt
        docs_content = "\n\n".join(doc.content for doc in tool_messages)
        system_message_content = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            f"{docs_content}"
        )
        conversation_messages = [
            message
            for message in state["messages"]
            if message.type in ("human", "system")
            or (message.type == "ai" and not message.tool_calls)
        ]
        prompt = [SystemMessage(system_message_content)] + conversation_messages

        # Run
        response = llm.invoke(prompt)
        return {"messages": [response]}

    # build graph
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    graph = graph_builder.compile()

    # asked for query
    for query in [
        "Czym różni się Agile od Scrum'a?",
        "Co to jest Agile?",
        "Co to jest Sprint?",
        "Jak duży powinien być zespół w Scrum?",
        "Jak duży powinien być zespół w Agile?",
        "Jakie jest zadanie Scrum Master'a?",
    ]:

        response = graph.invoke({"messages": [{"role": "user", "content": query}]})
        response_content = response["messages"][-1].content
        print(f"Query: {query}\nAnswer: {response_content}")
