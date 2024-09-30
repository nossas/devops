# Contexto

Sites são páginas web desenvolvidas dentro do time de tecnologia do NOSSAS e usado principalmente por Mobilizadores como um canal para criar Campanhas, criam-se páginas para documentar a narrativa da Campanha e costumam usar de Estratégias para impactar mudanças politicas públicas gerando Ações de Ativistas que se indentificam com a causa.


## Tecnologia Principal

Por serem páginas web, a principal funcionalidade dos Sites é levar um endereço web para uma página diponível em algum servidor. Para cuidar disso usamos um serviço de DNS hospedado pela Amazon, o Mobilizador compra um endereço em alguma empresa de vendas de domínio, como Registro.br, e então aponta as configurações de DNS do seu domínio para o  serviço de DNS da Amazon o Route53.

Após configurar o Route53 com o direcionamento correto, esse domínio está apto para acessar um serviço dentro de um servidor, hoje também hospedado pela Amazon usando instâncias EC2.

Ao chegar na instância, existe uma nova camada, agora de aplicação, que consegue rotear a conexão dos endereços entre aplicações e serviços internos. Isso permite ter vários serviços em uma única instância. Para resolver o redirecionamento ou proxy reverse (como se chama essa técnica na computação) usamos uma tecnologia chamada [Traefik](https://doc.traefik.io/traefik/).

Agora então existe uma capacidade de apontar vários endereços para uma instância e cada endereço desse para um serviço dentro dessa instância. Então passa a ser responsabilidade da aplicação que responde aquele serviço responder a esse endereço, podendo ou não conseguir responder a diversos endereços, mas agora a nível interno como uma aplicação CMS por exemplo.

### Roteamento

É muito comum o mesmo site responder em diferentes extensões como por exemplo, .org, .org.br, .com e .com.br, pra isso devemos usar uma funcionalidade do Traefik que possibilita configurar regras de roteamento com [Regex](https://doc.traefik.io/traefik/routing/routers/#host-and-hostregexp). Outro problema que o Regex resolve, são sites com subdomínios, o que também pode ser super comum em aplicações CMS.

Para esses casos podemos configurar o seguinte regex:

```
HostRegexp(`^.*whoami.(devel|local)$`)
```

NOTE: O domínio e subdomínios, whoami.devel e whoami.local, irão ser direcionados para o serviço que configurou essa regra no Traefik.

Entende-se que não existam limites para possíveis endereços que devam responder a aplicações deste domínio, por isso para facilitar a criação e manutenção dinâmica dessas configurações adicionamos o [Etcd](https://etcd.io) como um provedor de configurações no Traefik.

Dessa maneira a consolidação de um roteamento acontece ao configurar as seguintes chave-valor no etcd:

```
etcdctl put traefik/http/routers/whoami-devel/rule "HostRegexp(\`^.*whoami\.(devel|local)$\`)"

etcdctl put traefik/http/routers/whoami-devel/service "whoami-sites@docker"
```

### Serviços

Existem 2 principais serviços em nossa stack de tecnologias que se encaixam no domínio Sites.

- BONDE (versão pública)
- CMS
