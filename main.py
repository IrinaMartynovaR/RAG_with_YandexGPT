from dotenv import load_dotenv
import os
from src.scripts.preprocessing import read_file, clean_text, split_text_into_chunks
from src.scripts.database import create_chroma_db, load_chroma_db
from src.scripts.prompts import create_chain
import warnings

load_dotenv()

data_folder = "data"
file_paths = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]

# Обрабатываем файлы
all_chunks = []
for file_path in file_paths:
    med_book = read_file(file_path)
    cleaned_med_book = clean_text(med_book)
    chunks = split_text_into_chunks(cleaned_med_book)
    all_chunks.extend(chunks)  # Собираем все чанки в один список

# Создание базы данных
chroma_db = create_chroma_db(chunks)

# Загрузка базы данных
loaded_db = load_chroma_db()

# Создание retriever
retriever = loaded_db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2}
)

# Создание цепочки
chain = create_chain(retriever)
# green_questions = [
#     "Что делать при боли в мышцах?",
#     "Какие симптомы Боли в области сердца?",
#     "Как долго заживает перелом руки?"]

# for q in green_questions:
#     answer = chain.invoke(q)
#     print(f"Вопрос: {q}")
#     print(f"Ответ: {answer}\n")

# red_questions = [
#     "Кто победит на следующих выборах?"
# ]
# for q in red_questions:
#     answer = chain.invoke(q)
#     print(f"Вопрос: {q}")
#     print(f"Ответ: {answer}\n")