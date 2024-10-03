# Usar uma imagem base oficial do Python
FROM python:3.12-slim

# Instalar dependências para build
RUN apt-get update && apt-get install -y curl

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adicionar o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Definir a variável de ambiente para que o Poetry instale as dependências no sistema global (fora do ambiente virtual)
ENV POETRY_VIRTUALENVS_CREATE=false

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de configuração do Poetry (pyproject.toml e poetry.lock) para o container
COPY pyproject.toml poetry.lock* ./

# Instalar as dependências do projeto
RUN poetry install --no-dev --no-interaction --no-ansi

# Copiar o código da aplicação para o container
COPY . .

# Definir a variável de ambiente para o Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Executar o python-etcd3
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Expor a porta em que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["flask", "run", "--reload", "--debug"]
