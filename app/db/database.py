from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()


def get_db():
    return Chroma(
        collection_name ="books",
        embedding_function =embeddings,
        persist_directory="db"
    )


