# Bem-vinda à nossa stack DevOps

Este repositório é a fonte central de conhecimento sobre nossa infraestrutura, processos e padrões. Aqui você encontrará tudo o que precisa para configurar seu ambiente local e começar a interagir com nossos recursos na AWS e Kubernetes.

## Índice

- [Primeiro Passos](#primeiros-passos)
    - [Pré-requisitos](#pré-requisitos)
    - [Instalação das Ferramentas](#instalação-das-ferramentas)
    - [Configuração da AWS](#configuração-da-aws)
    - [Acesso ao Kubernetes (EKS)](#acesso-ao-kubernetes-eks)
- [Verificanto o Acesso](#verificando-o-acesso)
- [Próximos Passos](#próximos-passos)
- [Suporte](#suporte)

---

# Primeiros Passos

## Pré-requisitos
- Acesso ao Bitwarden (cofre compartilhado da tecnologia)
- **Conta AWS individual** com acesso já solicitado e aprovado
- Sistema operacional: Linux, macOS ou WSL2 (Windows)

## Instalação das Ferramentas

### 1. AWS CLI v2

A AWS CLI é necessária para autenticar e interagir com nossos serviços.

**Linux/macOS:**
```bash
# macOS (com Homebrew)
brew install awscli

# Linux (Ubuntu/Debian)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows (PowerShell como Administrador)**
```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```


Verifique a instalação:

```bash
aws --version
```

### 2. kubectl

Ferramenta de linha de comando para interagir com o Kubernetes.

**Linux/macOS:**
```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Windows**
```powershell
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/windows/amd64/kubectl.exe"
# Adicione ao PATH
```

## Configuração da AWS

### Modelo de Acesso: Credenciais Individuais

Nosso modelo de segurança exige que **cada desenvolvedor utilize suas próprias credenciais AWS**, nunca compartilhadas. Isso garante:

- **Rastreabilidade completa** de todas as ações (CloudTrail registra quem fez o quê)
- **Controle de acesso granular** baseado no princípio do menor privilégio
- **Rotação individual de credenciais** sem impacto para o time

### Solicitar acesso à AWS

Se você ainda não tem uma conta AWS com acesso aos recursos do time:

1. Envie uma mensagem para o time de plataforma **(@devs no canal #n_bonde do Slack)** com:
   - Seu nome completo
   - E-mail corporativo
   - Justificativa do acesso
2. Um administrador criará seu usuário IAM e concederá as permissões necessárias
3. Você receberá instruções para configurar seu primeiro acesso

### Gerar credenciais de acesso

Após ter seu usuário IAM criado:

1. Acesse o console AWS: https://console.aws.amazon.com
2. Navegue até **IAM > Users > [seu-usuário] > Security credentials**
3. Clique em **Create access key**
4. Escolha "Command Line Interface (CLI)"
5. Faça download ou copie as credenciais (Access Key ID e Secret Access Key)

### Configurar o profile AWS local

Com suas credenciais individuais em mãos, configure o profile da AWS CLI:

```bash
aws configure --profile nossas
```

- AWS Access Key ID: [sua access key]
- AWS Secret Access Key: [sua secret key]
- Default region name: us-east-1 (ou a região que você utiliza)
- Default output format: json

**⚠️ IMPORTANTE:** Você pode usar um nome de profile que identifique que são suas credenciais pessoais (ex: pessoal, seunome-aws). O profile `nossas` mencionado no kubeconfig é um exemplo; você poderá adaptar para seu profile real. Caso você use outro nome de profile, deve seguir a etapa [Adaptando o kubeconfig para seu profile](#adaptando-o-kubeconfig-para-seu-profile).

### Verificando a configuração

```bash
aws sts get-caller-identity --profile nossas
```

Você deve ver as informações do **seu usuário** AWS.

## Acesso ao Kubernetes (EKS)

### Obter a configuração do cluster e configurar acesso

1. Acesse o Bitwarden (cofre compartilhado da tecnologia).
2. Pesquise por **"Kubeconfig - EKS Cluster"** e copie todo o conteúdo.
3. Configure o acesso:
    ```bash
    # Crie o diretório se não existir
    mkdir -p ~/.kube

    # Faça backup caso já exista uma configuração
    [ -f ~/.kube/config ] && cp ~/.kube/config ~/.kube/config.backup

    # Cole o conteúdo do Bitwarden (use seu editor preferido nano/code/vim)
    vim ~/.kube/config
    ```

### Já usa Kubernetes e tem outros clusters?

Sem problemas! O kubectl trabalha com contextos. Seu cluster atual vai aparecer como `nossas` e você pode alternar entre eles:

```bash
# Ver todos os contextos disponíveis
kubectl config get-contexts

# Mudar para outro contexto
kubectl config use-context NOME-DO-CONTEXTO

# Voltar para nosso cluster
kubectl config use-context nossas
```

[Documentação oficial sobre contextos](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

### Adaptando o kubeconfig para seu profile

O arquivo de kubeconfig do Bitwarden referencia o profile `nossas`. Você precisará ajustar para usar seu profile pessoal:

```bash
users:
- name: eks-user
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: aws
      args:
      - --region
      - us-east-1
      - eks
      - get-token
      - --cluster-name
      - eks-cluster-da5d31b
      - --output
      - json
      env:
      - name: AWS_PROFILE  # ← Importante!
        value: nossas # ← Altere para SEU profile caso você tenha mudado nos passos anteriores (ex: pessoal, joao-aws, etc.)
```

### Autorização no Cluster (AWS IAM → Kubernetes RBAC)

**Como funciona o acesso**

O EKS integra a autenticação AWS IAM com a autorização Kubernetes RBAC através de um ConfigMap especial chamado `aws-auth` no namespace `kube-system`.

**Fluxo de autenticação/autorização:**

1. Você executa `kubectl` → a CLI chama `aws eks get-token`
2. AWS valida suas credenciais IAM e gera um token
3. O token é enviado para o API server do Kubernetes
4. O EKS consulta o ConfigMap `aws-auth` para mapear seu usuário IAM para uma Role/Usuário do Kubernetes
5. O RBAC do Kubernetes valida se você tem permissão para executar a ação

**Adicionar seu usuário ao cluster**

**Seu acesso ao cluster ainda não está configurado?** Você precisará que um administrador adicione seu usuário IAM ao ConfigMap `aws-auth`.

**Para administradores** - Conceder acesso a um novo desenvolvedor:

1. Edite o ConfigMap aws-auth:
    ```bash
    kubectl edit configmap aws-auth -n kube-system
    ```

2. Adicione o novo usuário na seção `mapUsers` (se não existir a seção, crie):
    ```bash
    data:
    mapUsers: |
        - userarn: arn:aws:iam::519061744633:user/nome-do-desenvolvedor
        username: nome-do-desenvolvedor
        groups:
            - system:masters  # Acesso de administrador (ajuste conforme necessário)
    ```

3. Salve e saia. O acesso é concedido imediatamente.

### Verificando o Acesso

Após configurar tudo, valide se está conseguindo acessar o cluster:

```bash
# Verifique qual contexto está ativo
kubectl config current-context

# Liste todos os contextos disponíveis
kubectl config get-contexts

# Liste os nodes do cluster (deve funcionar se as permissões estiverem corretas)
kubectl get nodes

# Teste um comando simples
kubectl get pods -A
```

Se tudo estiver correto, você verá a lista de nodes e pods do cluster.

## Próximos passos

TODO

## Suporte

Precisa de ajuda? Entre em contato:

- **Slack:** Canal [#n_bonde](https://nossas.slack.com/archives/C3T46K8AW)
- **GitHub Issues:** Abra uma issue neste repositório
- **Time de Plataforma:** @devs (marque no Slack)
