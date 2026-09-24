# Armazenamentos Gerais

Componente de referência para estudar e operar bancos de dados relacionais e NoSQL comuns em plataformas de aplicações. Cada subcomponente documenta o modelo de dados, cenários de uso, cliente de linha de comando (CLI) e um script de conexão.

Cada subcomponente inclui um Compose independente e manifests Kubernetes para laboratório. Eles são exemplos de nó único, com volume persistente, e não configurações de alta disponibilidade ou prontas para produção. Os serviços não iniciam juntos. A stack padrão deste repositório continua com seu PostgreSQL próprio; use os artefatos abaixo para subir apenas o banco necessário.

## Relacional e NoSQL

Bancos relacionais organizam dados em tabelas e relações, normalmente com esquema definido e consultas SQL. PostgreSQL, Microsoft SQL Server, MySQL e Oracle Database são opções relacionais. Escolha considerando compatibilidade, consistência, transações, operação, licenciamento e experiência da equipe.

NoSQL reúne modelos diferentes, não uma ausência de esquema. MongoDB armazena documentos; Cassandra usa tabelas distribuídas orientadas ao padrão de consulta; Redis oferece estruturas de dados em memória e é frequentemente usado como cache. Modelagem, consistência, persistência e particionamento variam entre eles.

## Subcomponentes

| Grupo | Banco | Guia |
|---|---|---|
| Relacional | PostgreSQL | [postgresql/README.md](./postgresql/README.md) |
| Relacional | Microsoft SQL Server | [sql-server/README.md](./sql-server/README.md) |
| Relacional | MySQL | [mysql/README.md](./mysql/README.md) |
| Relacional | Oracle Database 12c | [oracle-db-12c/README.md](./oracle-db-12c/README.md) |
| NoSQL: documentos | MongoDB | [mongodb/README.md](./mongodb/README.md) |
| NoSQL: colunas largas | Apache Cassandra | [cassandra/README.md](./cassandra/README.md) |
| NoSQL: chave-valor / cache | Redis | [redis-cache/README.md](./redis-cache/README.md) |

## Executar um banco

### Docker Compose

Entre na pasta do banco escolhido, copie `.env.example` para `.env`, substitua os valores locais e inicie apenas aquele Compose. Exemplo com PostgreSQL:

```sh
cd general-storage/postgresql
cp .env.example .env
docker compose up -d
docker compose ps
docker compose logs -f
```

Repita na pasta de outro subcomponente. `docker compose down` para o serviço mantendo o volume; `docker compose down -v` também apaga os dados persistidos. As portas ficam publicadas em `127.0.0.1` para acesso local.

### Kubernetes

Cada diretório `kubernetes/` pode ser aplicado isoladamente. Crie no namespace `general-storage` o Secret exigido pelo README daquele banco por meio de um secret manager ou fluxo seguro. Não use credenciais de laboratório em cluster compartilhado.

```sh
kubectl create namespace general-storage
kubectl apply -k general-storage/postgresql/kubernetes
kubectl -n general-storage get pods,pvc,services
```

Os PVCs pressupõem uma StorageClass padrão no cluster. Para remover recursos, execute `kubectl delete -k general-storage/postgresql/kubernetes`; o PVC de StatefulSet pode permanecer ou ser excluído conforme a política do cluster. Faça backup antes de qualquer remoção. Para imagens locais (incluindo Oracle), carregue-as no runtime do cluster ou publique-as em registry acessível e ajuste a referência da imagem.

Os nomes de variáveis e Secrets de cada banco estão nos guias individuais. Use versões de imagem fixas e revise as notas de versão antes de atualizar.

## Scripts de conexão

Os wrappers chamam os clientes nativos instalados no host. Instale cada CLI conforme a documentação oficial indicada no respectivo guia e configure as variáveis de ambiente necessárias. Para executá-los:

```sh
bash general-storage/scripts/connect/postgresql.sh
bash general-storage/scripts/connect/sql-server.sh
bash general-storage/scripts/connect/mysql.sh
bash general-storage/scripts/connect/oracle-db-12c.sh
bash general-storage/scripts/connect/mongodb.sh
bash general-storage/scripts/connect/cassandra.sh
bash general-storage/scripts/connect/redis-cache.sh
```

Não coloque senhas em scripts, arquivos versionados ou argumentos de linha de comando. Prefira prompts interativos, arquivos de credenciais com permissões restritas ou um gerenciador de segredos. Use contas com privilégios mínimos e conexões TLS quando suportadas.

## Uso na plataforma

O serviço PostgreSQL já definido no Compose raiz é destinado ao desenvolvimento local. Para iniciar somente ele e conferir o estado:

```sh
docker compose up -d postgresql
docker compose ps postgresql
```

O cliente pode ser executado no host, se instalado, ou dentro do container:

```sh
docker compose exec postgresql psql -U "${POSTGRES_USER:-platform}" -d "${POSTGRES_DB:-platform}"
```

As variáveis e credenciais usadas pelo Compose estão documentadas no [guia de execução](../docs/deployment.md). A base Kubernetes da plataforma inclui PostgreSQL; os manifests independentes deste componente cobrem os demais serviços sob demanda.

## Escolha e operação

Avalie o padrão de leitura e escrita, volume e crescimento dos dados, transações, consistência, disponibilidade, latência, backup/restauração, recuperação de desastre, segurança, observabilidade e custo operacional. Não escolha uma tecnologia apenas por popularidade: valide o modelo de dados e teste os requisitos de falha e recuperação antes de produção.
