Na instância onde essa arquitetura será implantada cria uma rede docker:

```bash
docker network create web
```

<!-- Após iniciar o stack `common` você deve criar as chaves no container do etcd
```
etcdctl put traefik/tls/options/default/cipherSuites/ "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
etcdctl put traefik/tls/options/default/cipherSuites/0 "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
etcdctl put traefik/tls/options/default/cipherSuites/1 "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
etcdctl put traefik/tls/options/default/cipherSuites/2 "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
etcdctl put traefik/tls/options/default/cipherSuites/3 "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
etcdctl put traefik/tls/options/default/cipherSuites/4 "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305"
etcdctl put traefik/tls/options/default/cipherSuites/5 "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
etcdctl put traefik/tls/options/default/minVersion "VersionTLS12"
``` -->