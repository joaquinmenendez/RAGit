import os
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma


# Create DB
def transcription_to_db(transcriptions: list, persist_directory="./chroma_db",
                        embedding_function: VertexAIEmbeddings = None):
    embedding_function = embedding_function if embedding_function else VertexAIEmbeddings(
        os.environ['EMBEDDING_MODEL'])
    texts = [text["text"] for text in transcriptions]
    metadatas = [{'start': text.get('start'), 'duration': text.get('duration'), 'url': text.get('url')} for text
                 in transcriptions]
    db = Chroma.from_texts(texts,
                           embedding_function,
                           metadatas=metadatas,
                           persist_directory=persist_directory)
    return db


def load_db(persist_directory: str = "./chroma_db",
            embedding_function=None) -> Chroma:
    embedding_function = embedding_function if embedding_function else VertexAIEmbeddings(
        os.environ['EMBEDDING_MODEL'])
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embedding_function)
    return db


