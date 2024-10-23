# Etapa 1: Usando imagem base Python com suporte a Slim para reduzir tamanho
FROM python:3.12-slim

# Etapa 2: Definindo diretório de trabalho
WORKDIR /app

# Etapa 3: Instalando dependências do sistema para rodar o Django e o Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: Instalando o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Etapa 5: Adicionando o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Etapa 6: Copiando os arquivos de dependências (pyproject.toml e poetry.lock)
COPY pyproject.toml poetry.lock /app/

# Etapa 7: Instalando as dependências
RUN poetry install --no-root

# Etapa 8: Copiando o código da aplicação
COPY . /app

# Etapa 9: Configurando o volume para sincronizar com o diretório local
VOLUME ["/app"]

# Etapa 10: Expondo a porta padrão do Django (8000)
EXPOSE 8000

# Etapa 11: Rodando o servidor do Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
