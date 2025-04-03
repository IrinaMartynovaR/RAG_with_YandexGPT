from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from yandex_chain import YandexLLM, YandexGPTModel
import os

# Инициализация модели
llm = YandexLLM(
    folder_id=os.environ['folder_id'],
    api_key=os.environ['api_key'],
    model=YandexGPTModel.Pro
)

# Функция для загрузки шаблона промпта из файла
def load_prompt_template(file_path):
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с шаблоном промпта не найден: {file_path}")

# Функция для загрузки списка запрещенных ключевых слов
def load_forbidden_keywords(file_path):
    """Загружает список запрещенных ключевых слов из текстового файла."""
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            keywords = [line.strip() for line in file if line.strip()]
        return keywords
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с запрещенными ключевыми словами не найден: {file_path}")

# Путь к файлу с шаблоном промпта
template_file = 'prompt_template.txt'

# Загрузка шаблона промпта из файла
prompt_template = load_prompt_template(template_file)

# Создание объекта PromptTemplate
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# Загрузка списка запрещенных слов
forbidden_keywords_file = 'forbidden_keywords.txt'
FORBIDDEN_KEYWORDS = load_forbidden_keywords(forbidden_keywords_file)

# Функция для проверки вопроса на наличие запрещенных слов
def is_forbidden_question(question):
    """Проверяет, содержит ли вопрос запрещенные ключевые слова."""
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
    """Объединяет документы в один текст."""
    return "\n\n".join(doc.page_content for doc in docs)

# Создание цепочки для генерации ответов
def create_chain(retriever):
    """Создает цепочку для генерации ответов."""
    chain = (
        {"context": retriever | join_docs, "question": RunnablePassthrough()}
        | RunnableLambda(check_question)  # Добавляем проверку на запрещенные слова
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain