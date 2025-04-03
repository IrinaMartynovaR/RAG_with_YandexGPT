from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from yandex_chain import YandexEmbeddings
import os
load_dotenv()

# Инициализация модели эмбеддингов
embeddings = YandexEmbeddings(
    folder_id=os.environ['folder_id'],  
    api_key=os.environ['api_key'],      
    model="YandexGPTModel.Pro"
)

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