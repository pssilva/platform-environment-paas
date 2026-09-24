# MongoDB

Banco NoSQL orientado a documentos BSON. Documentos podem representar agregados de aplicação e evoluir sem que todas as coleções compartilhem uma definição relacional fixa; ainda assim, índices, validação e modelagem precisam ser planejados.

## CLI: `mongosh`

Instale o MongoDB Shell seguindo o [guia oficial de instalação](https://www.mongodb.com/docs/mongodb-shell/install/). O script conecta usando `MONGODB_URI`:

```sh
export MONGODB_URI='mongodb://localhost:27017/app'
bash general-storage/scripts/connect/mongodb.sh
```

Para autenticação, use um mecanismo seguro de injeção de segredo e evite deixar credenciais em histórico, URI versionada ou log de processo. No shell, tente `db.runCommand({ ping: 1 })`, `show collections` e `db.collection.findOne()`.

O wrapper conecta a um servidor existente. Planeje índices, backup/restauração, controles de acesso e topologia de replicação conforme os requisitos. Consulte o [manual do mongosh](https://www.mongodb.com/docs/mongodb-shell/).

## Docker Compose

O Compose usa a imagem oficial MongoDB 8.0, cria o usuário root inicial e persiste os dados em volume.

```sh
cd general-storage/mongodb
cp .env.example .env
# Altere MONGO_INITDB_ROOT_PASSWORD.
docker compose up -d
docker compose ps
docker compose logs -f mongodb
```

## Kubernetes

O StatefulSet inclui PVC de 10 Gi e autenticação inicial. Crie a chave `root-password` no Secret `mongodb-credentials` via mecanismo seguro:

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic mongodb-credentials --from-literal=root-password='<senha-local>'
kubectl apply -k general-storage/mongodb/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/mongodb 27017:27017
```

Conexões internas usam `mongodb.general-storage.svc:27017`. As variáveis `MONGO_INITDB_*` só inicializam uma base vazia; trocar o Secret não altera usuários existentes. Crie um usuário de aplicação com privilégios mínimos em vez de usar root. Veja a [imagem oficial MongoDB](https://hub.docker.com/_/mongo).
