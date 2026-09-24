# Redis Cache

Redis é um armazenamento em memória de estruturas de dados, usado com frequência para cache, sessões, filas e contadores. Defina TTL e política de invalidação para cada dado de cache. Cache não substitui automaticamente a fonte durável de dados; persistência, replicação e recuperação dependem da configuração do Redis.

## CLI: `redis-cli`

Instale o cliente conforme a [documentação oficial do Redis CLI](https://redis.io/docs/latest/develop/tools/cli/). Configure a conexão:

```sh
export REDIS_HOST=localhost
export REDIS_PORT=6379
bash general-storage/scripts/connect/redis-cache.sh
```

Se houver senha, habilite o prompt seguro com `export REDIS_ASKPASS=true`; o wrapper usa `--askpass` sem colocar a senha no comando. No prompt, `PING` verifica a conexão; `INFO server` consulta dados do servidor. Para TLS, defina `REDIS_TLS=true`. Prefira ACLs com privilégios mínimos em ambientes remotos. Evite `FLUSHALL`/`FLUSHDB` sem autorização e plano de recuperação.

## Docker Compose

O Compose usa Redis 7.4, exige senha e habilita AOF para persistência de laboratório. A porta publicada é limitada ao loopback.

```sh
cd general-storage/redis-cache
cp .env.example .env
# Troque REDIS_PASSWORD.
docker compose up -d
docker compose ps
docker compose logs -f redis
```

Conecte com `redis-cli -h localhost -p 6379 --askpass` e digite a senha. Os dados ficam em volume nomeado.

## Kubernetes

O StatefulSet solicita PVC de 5 Gi e carrega a senha do Secret `redis-credentials`:

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic redis-credentials --from-literal=password='<senha-local>'
kubectl apply -k general-storage/redis-cache/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/redis 6379:6379
```

A conexão intra-cluster usa `redis.general-storage.svc:6379`. Port-forward e acesso do cliente precisam de autenticação. Este recurso de nó único não substitui cache gerenciado, Sentinel/Cluster ou desenho de persistência para produção.
