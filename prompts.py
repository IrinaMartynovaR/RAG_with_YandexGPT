from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.embeddings import HuggingFaceEmbeddings
from YaLLM import YandexLLM
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()


# Настройка переменных окружения
folder_id = os.getenv('folder_id')
iam_token = os.getenv('IAM_TOKEN')
api_key = os.getenv('api_key')


# Путь к файлам
template_file = 'prompt_template.txt'
forbidden_keywords_file = 'forbidden_keywords.txt'

# Инициализация модели Yandex GPT
llm = YandexLLM(
    folder_id=folder_id,
    api_key=api_key,
    iam_token=iam_token,
    temperature=0,
    max_tokens=300,
    instruction_text = template_file
)


# Инициализация эмбеддингов
embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1")

# Функция для загрузки шаблона промпта из файла
def load_prompt_template(file_path):
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с шаблоном промпта не найден: {file_path}")

# Функция для загрузки списка запрещенных ключевых слов
def load_forbidden_keywords(file_path):
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с запрещенными ключевыми словами не найден: {file_path}")



# Загрузка шаблона промпта и запрещенных слов
prompt_template = load_prompt_template(template_file)
FORBIDDEN_KEYWORDS = load_forbidden_keywords(forbidden_keywords_file)

# Создание объекта PromptTemplate
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Функция для проверки вопроса на наличие запрещенных слов
def is_forbidden_question(question):
    question_lower = question.lower()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in question_lower:
            return True
    return False

# Функция для проверки вопроса перед отправкой в модель
def check_question(inputs):
    question = inputs["question"]
    if is_forbidden_question(question):
        return {"response": "Я не могу помочь с этим вопросом."}
    return inputs

# Функция для объединения документов
def join_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Создание цепочки для генерации ответов
def create_chain(retriever):
    chain = (
        {"context": retriever | join_docs, "question": RunnablePassthrough()}
        | RunnableLambda(check_question)  # Добавляем проверку на запрещенные слова
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
