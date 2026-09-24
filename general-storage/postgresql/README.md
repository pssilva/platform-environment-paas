# PostgreSQL

Banco relacional open source que oferece SQL, transações e extensibilidade. É o banco relacional habilitado na stack padrão deste repositório.

## Uso neste repositório

O serviço Compose raiz usa PostgreSQL 16 e persiste dados em volume nomeado. Para iniciar somente o banco:

```sh
docker compose up -d postgresql
docker compose ps postgresql
docker compose logs -f postgresql
```

Este subcomponente também fornece um Compose isolado, com seu próprio volume:

```sh
cd general-storage/postgresql
cp .env.example .env
# Substitua a senha de exemplo por uma senha local.
docker compose up -d
docker compose ps
```

Conecte com o `psql` instalado no host ou use o cliente da imagem:

```sh
bash general-storage/scripts/connect/postgresql.sh
docker compose exec postgresql psql -U "${POSTGRES_USER:-platform}" -d "${POSTGRES_DB:-platform}"
```

Configure `PGHOST`, `PGPORT`, `PGDATABASE` e `PGUSER` para conexão do host (padrões: `localhost`, `5432`, `platform` e `platform`). O Compose carrega usuário, banco e senha do `.env`; veja [Execução da plataforma](../../docs/deployment.md). Não remova volumes com `docker compose down -v` se precisar dos dados.

## Kubernetes

O StatefulSet persiste os dados em PVC de 10 Gi e espera que exista uma StorageClass padrão. Crie o Secret por meio de um secret manager ou fluxo seguro; este comando é apenas para laboratório, pois o valor pode aparecer no histórico:

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic postgresql-credentials --from-literal=password='<senha-local>'
kubectl apply -k general-storage/postgresql/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/postgresql 5432:5432
```

A conexão interna é `postgresql.general-storage.svc:5432`. Remova os recursos com `kubectl delete -k general-storage/postgresql/kubernetes`; faça backup e avalie o PVC antes de excluí-lo.

## Cliente CLI

O cliente oficial é `psql`, incluído nas distribuições de cliente PostgreSQL. Referência: [documentação do PostgreSQL](https://www.postgresql.org/docs/current/app-psql.html) e [imagem oficial PostgreSQL](https://hub.docker.com/_/postgres).

Exemplos no prompt `psql`:

```sql
\conninfo
\dt
SELECT current_database(), current_user;
\q
```

Para operações repetíveis, versione migrações com a aplicação, não credenciais. Use um banco e usuário por aplicação/ambiente, TLS fora do ambiente local, permissões mínimas e backups com restauração verificada. Métricas e logs podem ser integrados à observabilidade.
