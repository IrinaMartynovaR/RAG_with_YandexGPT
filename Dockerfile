FROM python:3.13-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-root

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN poetry install --no-interaction --no-root

CMD ["poetry", "run", "python", "main.py"]
