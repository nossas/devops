# Contexto

Sites são páginas web desenvolvidas dentro do time de tecnologia do NOSSAS e usado principalmente por Mobilizadores como um canal para criar Campanhas, criam-se páginas para documentar a narrativa da Campanha e costumam usar de Estratégias para impactar mudanças politicas públicas gerando Ações de Ativistas que se indentificam com a causa.


## Tecnologia Principal

Por serem páginas web, a principal funcionalidade dos Sites é levar um endereço web para uma página diponível em algum servidor. Para cuidar disso usamos um serviço de DNS hospedado pela Amazon, o Mobilizador compra um endereço em alguma empresa de vendas de domínio, como Registro.br, e então aponta as configurações de DNS do seu domínio para o  serviço de DNS da Amazon o Route53.

Após configurar o Route53 com o direcionamento correto, esse domínio está apto para acessar um serviço dentro de um servidor, hoje também hospedado pela Amazon usando instâncias EC2.

Ao chegar na instância, existe uma nova camada, agora de aplicação, que consegue rotear a conexão dos endereços entre aplicações e serviços internos. Isso permite ter vários serviços em uma única instância. Para resolver o redirecionamento ou proxy reverse (como se chama essa técnica na computação) usamos uma tecnologia chamada [Traefik](https://doc.traefik.io/traefik/).

Agora então existe uma capacidade de apontar vários endereços para uma instância e cada endereço desse para um serviço dentro dessa instância. Então passa a ser responsabilidade da aplicação que responde aquele serviço responder a esse endereço, podendo ou não conseguir responder a diversos endereços, mas agora a nível interno como uma aplicação CMS por exemplo.