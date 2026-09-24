# Apache Cassandra

Banco distribuído NoSQL de colunas largas, projetado para disponibilidade e escala horizontal. A modelagem começa pelos padrões de consulta e pela chave de partição; CQL tem sintaxe familiar a SQL, mas Cassandra não é um banco relacional geral.

## CLI: `cqlsh`

`cqlsh` acompanha as distribuições Apache Cassandra compatíveis. Consulte [ferramentas oficiais](https://cassandra.apache.org/doc/stable/cassandra/managing/tools/cqlsh.html) e a [instalação do Cassandra](https://cassandra.apache.org/doc/latest/cassandra/installing/installing.html).

```sh
export CASSANDRA_HOST=localhost
export CASSANDRA_PORT=9042
bash general-storage/scripts/connect/cassandra.sh
```

No prompt, use `DESCRIBE KEYSPACES;` e `SELECT release_version FROM system.local;`. A versão do `cqlsh` deve ser compatível com o servidor. Para autenticação, configure o arquivo de credenciais/`cqlshrc` com acesso restrito conforme a documentação, sem incluir senhas no repositório ou na linha de comando.

O script apenas conecta; não implanta um cluster. Projete partições, replicação, consistência e reparo com base nas consultas e no desenho do cluster.

## Docker Compose

O Compose inicia um nó Cassandra 5 para laboratório, com dados em volume nomeado e a porta publicada apenas em `localhost`.

```sh
cd general-storage/cassandra
cp .env.example .env
docker compose up -d
docker compose ps
docker compose logs -f cassandra
```

Cassandra pode levar alguns minutos para inicializar. O exemplo não habilita autenticação; mantenha-o restrito ao ambiente local e não exponha a porta em rede compartilhada. Consulte a [imagem oficial Cassandra](https://hub.docker.com/_/cassandra).

## Kubernetes

O StatefulSet de nó único solicita PVC de 10 Gi e cria Service interno em `cassandra.general-storage.svc:9042`:

```sh
kubectl create namespace general-storage
kubectl apply -k general-storage/cassandra/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/cassandra 9042:9042
```

Este exemplo também não ativa autenticação e é restrito a laboratório. Antes de disponibilizar em cluster compartilhado, configure autenticação/autorização, restrinja tráfego de rede e planeje um cluster com réplicas, rack awareness, backups e reparação. Um StatefulSet singleton não fornece HA nem tolerância a falhas de nó.
