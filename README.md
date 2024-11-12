# Devops da infraestrutura Nosssas

Este projeto utiliza `awscli` e `terraform` para gerenciar infraestrutura como código. A configuração do estado da infraestrutura é persistida em um bucket S3 e o controle de lock é gerenciado por uma tabela no DynamoDB. 

## Dependências

Para executar este projeto, você precisará instalar as seguintes ferramentas:

- `awscli`: Ferramenta de linha de comando da AWS para gerenciar e interagir com serviços da AWS.
- `terraform`: Ferramenta de infraestrutura como código para gerenciar e provisionar recursos em várias plataformas.

### Instalação no MacOS
aws-cli:
```bash
brew install awscli
```

terraform:
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
brew update
brew upgrade hashicorp/tap/terraform
```

### Instalação no Debian/Ubuntu
aws-cli:
```bash
sudo apt update
sudo apt install awscli -y
```

terraform:
```bash
sudo apt update
sudo apt install -y software-properties-common
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### Variáveis de ambiente
É necessário inserir duas chaves no seu env para rodar os comandos terraform.
```bash
export AWS_ACCESS_KEY_ID=<inserir chave aqui>
export AWS_SECRET_ACCESS_KEY=<inserir chave aqui>
```

### Chave ssh da AWS
Para fins de criação e manutenção de instâncias na AWS é necessário incluir a chave pública `ailton-krenak.pem` no seguinte path do seu ambiente de desenvolvimento `˜/.ssh/ailton-krenak.pem`.

## Como executar

### Configurando a infraestrutura com Terraform

O estado do terraform está sendo compartilhado no S3 com gerenciamento de lock em uma tabela no DynamoDB.

Se o bucket configurado `bonde-terraform-up-and-running-state` não existir na lista de buckets da sua conta Amazon (região: us-east-1), você deve executar os seguintes comandos na pasta `instances/boostrap`:

```bash
terraform init
terraform plan
terraform init -auto-approve
```

Essa sequência de comandos acima irá criar a infraestrutura não persistente responsável por cuidar do estado da nossa infraestrutura persistente.

### Executando a infraestrutura com esquema de workspaces do terraform
Este projeto utiliza *workspaces* do Terraform para gerenciar múltiplos ambientes (como `dev`, `stage` e `prod`) dentro de uma única configuração de infraestrutura. Cada *workspace* permite isolar o estado e os recursos entre diferentes ambientes.

Dentro da estrutura do nosso código, temos o arquivo `main.tf` onde nós definimos todas as variáveis *default*, como a seguir:
```
locals {
  # Tipo de imagem para o servidor legado (APIS e Clientes Bonde)
  ami                         = "ami-0866a3c8686eaeeba"

  # Nome da chave SSH
  key_name                    = "custom-host"

  # Caminho para a chave privada SSH
  private_key_path            = "~/.ssh/ailton-krenak.pem"

  # Ambiente (dev, staging, production)
  env                         = terraform.workspace

  # Tipo de instância para o servidor legado (APIS e Clientes Bonde)
  legacy_server_instance_type = terraform.workspace == "stage" ? "t3.small" : "t3.micro"

  # Tipo de instância para o servidor de sites (Bonde Público e CMS)
  sites_server_instance_type  = terraform.workspace == "stage" ? "t3.micro" : "t2.micro"
}
```

1. **Criando ou Selecionando um Workspace**:
   - Para criar um novo *workspace*, execute:
     ```bash
     terraform workspace new nome-do-workspace
     ```
   - Para alternar para um *workspace* existente, execute:
     ```bash
     terraform workspace select nome-do-workspace
     ```

2. **Executando a Configuração no Workspace Selecionado**:
   Com o *workspace* adequado selecionado, você pode executar os comandos do Terraform normalmente. O estado será armazenado separadamente para cada *workspace*, mantendo os recursos de cada ambiente isolados.
   
   ```bash
   terraform init
   terraform apply -auto-approve
   ```

## Sites


## TODO

- [X] Persistir o estado no S3 e lock com DynamoDB
- [ ] Criar fluxo de trabalho para publicação automatizada no Github
- [X] Resolver caminho da chave privada
- [X] Documentar o uso do workspace
- [X] Documentar o uso da chave privada `custom-host / ailton-krenak`
- [X] Configuração da awscli e terraform e das variaveis de ambiente que precisam ser configuradas para acessar a conta AWS
