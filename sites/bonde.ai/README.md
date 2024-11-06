# bonde.ai

Este é um projeto de assistente virtual em Django para facilitar o acesso a ferramentas úteis de administração das aplicações BONDE.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose

## Configuração do Ambiente

### 1. Clonar o Repositório

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/nossas/devops.git
cd devops/sites/bonde.ai/
```

### 2. Criar o Ambiente Virtual

Crie e ative o ambiente virtual com o `venv`:

```bash
# No Linux ou macOS
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativo, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 4. Configuração de Variáveis de Ambiente

Renomeie o arquivo .env.example para .env e configure as variáveis necessárias:

```bash
cd ../

# Na pasta devops/sites
mv .env.example .env
```

Certifique-se de ajustar as variáveis de ambiente, como credenciais do banco de dados, configurações de cache, etc.

### 5. Rodar os Serviços com Docker Compose

Os serviços auxiliares, como Traefik, Localstack ou qualquer outro serviço, serão executados com Docker Compose. Para rodar os serviços, utilize os seguintes comandos:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Isso irá iniciar todos os serviços configurados no `docker-compose.yml` e no arquivo de configuração de desenvolvimento `docker-compose.dev.yml`.

### 6. Aplicar as Migrações do Banco de Dados

Depois de rodar os containers, aplique as migrações para configurar o banco de dados:

```bash
cd bonde.ai/

# Na pasta devops/sites/bonde.ai
python manage.py migrate
```

### 7. Criar o Superusuário

Se precisar acessar o painel administrativo do Django, crie um superusuário:

```bash
python manage.py createsuperuser
```

Você também pode autenticar com usuários do Bonde Staging.

### 8. Rodar o Servidor de Desenvolvimento

Agora, você pode rodar o servidor localmente:

```bash
python manage.py runserver
```

O projeto estará disponível em http://127.0.0.1:8000/.

## Contribuição

Se quiser contribuir com o projeto, faça um fork e abra um Pull Request com suas melhorias.

### Explicações:

- **Ambiente virtual (venv)**: O Python e dependências são gerenciados localmente com o `venv`.
- **Docker Compose**: Os serviços como Traefik ou Localstack são executados dentro de containers.
- **Arquivos Compose**: O `docker-compose.yml` é o arquivo principal, enquanto o `docker-compose.dev.yml` pode conter configurações específicas para desenvolvimento, como containers extras, volumes, etc.
