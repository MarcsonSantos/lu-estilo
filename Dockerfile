# Imagem base oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho no container
WORKDIR /code

# Copia o requirements.txt e instala as dependências
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando padrão (substituído no docker-compose.yml)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
