import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from langchain_text_splitters import SpacyTextSplitter
from dotenv import load_dotenv

load_dotenv()


def setup():
    llm = init_chat_model("gpt-4.1-nano", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = ElasticsearchStore(
        index_name=os.environ["ES_INDEX"],
        embedding=embeddings,
        es_url=os.environ["ES_URL"],
        es_user=os.environ["ES_USERNAME"],
        es_password=os.environ["ES_PASSWORD"],
    )

    text_splitter = SpacyTextSplitter(pipeline="pl_core_news_md")

    return llm, embeddings, vector_store, text_splitter


def load_files_pathlib(path, split_dir, vector_store, text_splitter):
    for entry in path.iterdir():
        if entry.is_file():
            print(f"processing {entry}")
            loader = PyPDFLoader(entry)
            docs = loader.load()

            for doc in docs:
                metadata = doc.metadata

                file_path = metadata.get("source", None)
                if file_path:
                    _, file_uri = file_path.split(split_dir)
                    file_path_parts = list(Path(file_uri).parts[1:-1])
                    file_path_parts = [p.lower() for p in file_path_parts]
                    if file_path_parts and len(file_path_parts) > 0:
                        metadata["tags"] = file_path_parts

            nodes = text_splitter.split_documents(docs)
            vector_store.add_documents(documents=nodes)

        elif entry.is_dir():
            load_files_pathlib(entry, split_dir, vector_store, text_splitter)


def main(path, split_dir):
    llm, embeddings, vector_store, text_splitter = setup()
    load_files_pathlib(path, split_dir, vector_store, text_splitter)


if __name__ == "__main__":
    documents_path = "documents"
    main(Path(documents_path), documents_path)
