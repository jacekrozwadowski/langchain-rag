import os
from typing import Dict
from langchain.chat_models import init_chat_model
from langchain_elasticsearch import ElasticsearchRetriever
from langchain_openai import OpenAIEmbeddings
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain import hub
from langchain_core.documents import Document
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    llm = init_chat_model("gpt-4.1-nano", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

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
        }

    hybrid_retriever = ElasticsearchRetriever.from_es_params(
        index_name=os.environ["ES_INDEX"],
        body_func=hybrid_query,
        content_field="text",
        url=os.environ["ES_URL"],
        username=os.environ["ES_USERNAME"],
        password=os.environ["ES_PASSWORD"],
    )

    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=hybrid_retriever, llm=llm, include_original=True
    )

    # retrieved_docs = hybrid_retriever.invoke("Czym różni się Agile od Scrum'a?")
    # for rd in retrieved_docs:
    #     print(rd.metadata["_source"]["metadata"]["tags"])

    prompt = hub.pull("rlm/rag-prompt")

    # Define state for application
    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str

    # Define application steps
    def retrieve(state: State):
        retrieved_docs = retriever_from_llm.invoke(state["question"])
        return {"context": retrieved_docs}

    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke(
            {"question": state["question"], "context": docs_content}
        )
        response = llm.invoke(messages)
        return {"answer": response.content}

    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    for query in [
        "Czym różni się Agile od Scrum'a?",
        "Co to jest Agile?",
        "Co to jest Sprint?",
        "Jak duży powinien być zespół w Scrum?",
        "Jak duży powinien być zespół w Agile?",
        "Jakie jest zadanie Scrum Master'a?",
    ]:
        response = graph.invoke({"question": query})
        print(f"Query: {query}\nAnswer: {response['answer']}")
