FROM python:3.13-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install poetry

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем проект
COPY . .

# Укажи здесь, какую команду запускать при старте контейнера
CMD ["poetry", "run", "python", "main.py"]
