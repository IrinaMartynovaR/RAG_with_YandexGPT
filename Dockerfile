# Базовый образ
FROM python:3.13-slim

# Установка системных зависимостей
# Установка системных зависимостей
# Компиляторы C и C++
# Заголовочные файлы Python
# Curl для установки Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    libpython3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Рабочая директория
WORKDIR /app

# Копируем манифесты зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей с виртуальным окружением
RUN poetry config virtualenvs.create true && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем весь проект
COPY . /app

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app/src

# Запуск основного скрипта
CMD ["poetry", "run", "python", "main.py"]