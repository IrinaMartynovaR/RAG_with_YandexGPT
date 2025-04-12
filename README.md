# Схема проекта 
![Снимок экрана (6135)](https://github.com/user-attachments/assets/c38dffb3-32a2-4811-8d1b-dd672f3f183e)

# Проект RAG (Retrieval-Augmented Generation) для медицинских вопросов

Этот проект использует Retrieval-Augmented Generation (RAG). Система извлекает релевантные фрагменты текста из базы данных Chroma и генерирует ответы с помощью модели YandexGPT.

## Требования

Для работы с проектом вам понадобятся:
- Python 3.12 или выше
- Установленный Git
- Доступ к API YandexGPT (folder_id и api_key)
- База знаний в текстовом формате (.txt`)

---

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/IrinaMartynovaR/RAG_with_YandexGPT.git
   cd RAG_with_YandexGPT
   ```

2. **Создайте виртуальную среду и установите зависимости с помощью Poetry:**
   Убедитесь, что у вас установлен Poetry. Если нет, установите его, следуя инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).
   Затем выполните команду для создания виртуальной среды и установки всех зависимостей, указанных в `pyproject.toml`:
   ```bash
   poetry install
   ```

3. **Активируйте виртуальную среду:**
   Для активации виртуальной среды используйте:
   ```bash
   poetry shell
   ```

4. **Убедитесь, что зависимости установлены корректно.**

---

## Настройка

1. **Создайте файл `.env`:**
   В корневой директории проекта создайте файл `.env` со следующим содержимым:
   ```plaintext
   folder_id=your_folder_id_here
   api_key=your_api_key_here
   IAM_TOKEN = IAM_TOKEN
   ```

2. **Добавьте исходный текстовый файл:**
   Поместите ваш исходный текстовый файл в папку `data/`.

3. **Запустите предобработку текста:**
   Запустите скрипт для очистки текста и создания базы данных Chroma:
   ```bash
   python preprocessing.py
   ```

---

## Использование

1. **Запустите основной скрипт:**
   ```bash
   poetry run python main.py
   ```

2. **Задайте вопросы:**
   После запуска программы вы можете задавать вопросы в консоли. Например:
   ```plaintext
   Вопрос: Как лечить простуду?
   Ответ: Простуду можно лечить с помощью отдыха, обильного питья и противовоспалительных препаратов.
   ```

3. **Обработка запрещенных тем:**
   Если вопрос выходит за рамки допустимой темы (например, политика, финансы), система ответит:
   ```plaintext
   Этот вопрос выходит за пределы моей компетенции.
   ```

   ```

## Структура проекта

```
/project_directory
│
├── data/                     # Исходные данные
│   ├── .txt          # Исходный текстовый файл
│   └── cleaned_.txt  # Очищенный текстовый файл
│
├── .env                      # Переменные окружения
├── .gitignore                # Игнорируемые файлы
├── README.md                 # Документация
├── pyproject.toml            # Зависимости
├── prompt_template.txt       # Промт
│
├── main.py                   # Основной скрипт
├── preprocessing.py          # Предобработка текста
├── database.py               # Работа с базой данных Chroma
├── prompts.py                # Шаблоны промптов и цепочка
└── YaLLM.py                  # Модель
```
