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

- Persistir o estado no S3
- Criar fluxo de trabalho para publicação automatizada no Github