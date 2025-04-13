from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1")

def create_chroma_db(chunks, persist_directory="chroma_db_med"):
    """Создает базу данных Chroma из чанков."""
    chroma_db = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("База данных успешно создана и сохранена.")
    return chroma_db

def load_chroma_db(persist_directory="chroma_db_med"):
    """Загружает базу данных Chroma."""
    chroma_db = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_directory
    )
    print("База данных успешно загружена.")
    return chroma_db