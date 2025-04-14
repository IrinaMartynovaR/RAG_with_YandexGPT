# Схема проекта 
![Снимок экрана (6135)](https://github.com/user-attachments/assets/c38dffb3-32a2-4811-8d1b-dd672f3f183e)

# Проект RAG (Retrieval-Augmented Generation) для медицинских вопросов

Этот проект использует Retrieval-Augmented Generation (RAG). Система извлекает релевантные фрагменты текста из базы данных Chroma и генерирует ответы с помощью модели YandexGPT.

## Требования

Для работы с проектом вам понадобятся:
- Python 3.12 или выше
- Docker
- Доступ к API YandexGPT (folder_id и api_key)
- База знаний в текстовом формате (.txt`)

---
## Настройка

1. **Создайте файл `.env`:**
   В папке scripts создайте `.env` со следующим содержимым:
   ```plaintext
   folder_id=your_folder_id_here
   api_key=your_api_key_here
   IAM_TOKEN = IAM_TOKEN
   ```

2. **Добавьте исходныe текстовый файлы для базы знаний:**
   Поместите ваши исходные текстовый файлы в папку `data/`.


## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/IrinaMartynovaR/RAG_with_YandexGPT.git
   cd RAG_with_YandexGPT
   ```

2. **Построение Docker-образа::**
   Убедитесь, что у вас установлен Poetry. Если нет, установите его, следуя инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation).
   Затем выполните команду для сборки контейнера:
   ```bash
   docker build -t rag_for_us .
   ```

3. **Запуск Docker-контейнера:**
   Для активации виртуальной среды используйте:
   ```bash
   docker run rag_for_us
   ```
