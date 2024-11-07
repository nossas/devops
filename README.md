## Como desenvolver

Instale a aws-cli:

```bash
```

Instale o terraform:

```bash
```


## Instancias

Tecnologia: terraform

### Como executar a infraestrutura

O estado do terraform está sendo compartilhado no S3 com gerenciamento de lock em uma tabela no DynamoDB.

Se o bucket configurado `bonde-terraform-up-and-running-state` não existir na lista de buckets da sua conta Amazon (região: us-east-1), você deve executar os seguintes comandos na pasta `instances/boostrap`:

```bash
terraform init
terraform plan
terraform init -auto-approve
```

Essa sequência de comandos acima irá criar a infraestrutura não persistente responsável por cuidar do estado da nossa infraestrutura persistente.

#### Executando a infraestrutura persistente



## Sites


## TODO

- [X] Persistir o estado no S3 e lock com DynamoDB
- [ ] Criar fluxo de trabalho para publicação automatizada no Github
- [X] Resolver caminho da chave privada
- [ ] Documentar o uso do workspace
- [ ] Documentar o uso da chave privada `custom-host / ailton-krenak`
- [ ] Configuração da awscli e terraform e das variaveis de ambiente que precisam ser configuradas para acessar a conta AWS