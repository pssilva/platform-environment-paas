# Microsoft SQL Server

Banco relacional da Microsoft, com SQL e transações, comum em aplicações corporativas que dependem do ecossistema Microsoft ou de compatibilidade T-SQL.

## CLI: `sqlcmd`

Instale `sqlcmd` seguindo a [documentação oficial de ferramentas para SQL Server no Linux](https://learn.microsoft.com/sql/linux/sql-server-linux-setup-tools). O script deste componente usa host e porta configuráveis e deixa a senha para o mecanismo de autenticação seguro do cliente:

```sh
export SQLSERVER_HOST=localhost
export SQLSERVER_PORT=1433
export SQLSERVER_DATABASE=master
export SQLSERVER_USER=sa
bash general-storage/scripts/connect/sql-server.sh
```

No prompt `sqlcmd`, execute `SELECT @@VERSION;` e finalize com `GO`. O script não configura nem inicia o servidor. Consulte também a documentação de [sqlcmd](https://learn.microsoft.com/sql/tools/sqlcmd/sqlcmd-utility).

## Docker Compose

Revise e aceite os termos da licença antes de usar a imagem. O perfil `Developer` é para desenvolvimento e testes. O exemplo usa imagem SQL Server 2022 da Microsoft e expõe a porta somente no loopback:

```sh
cd general-storage/sql-server
cp .env.example .env
# Altere MSSQL_SA_PASSWORD antes de iniciar.
docker compose up -d
docker compose ps
docker compose logs -f sql-server
```

## Kubernetes

O StatefulSet usa PVC de 20 Gi e edição Developer. Crie o namespace e o Secret de senha por mecanismo seguro. Este comando serve apenas como exemplo local e pode gravar o valor no histórico:

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic sql-server-credentials --from-literal=sa-password='<senha-forte>'
kubectl apply -k general-storage/sql-server/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/sql-server 1433:1433
```

A porta interna é `sql-server.general-storage.svc:1433`. Licença e edição de produção exigem configuração apropriada; veja [execução de SQL Server em Docker](https://learn.microsoft.com/sql/linux/quickstart-install-connect-docker).

Em ambientes corporativos, avalie edição, licença, autenticação integrada, TLS, backups e alta disponibilidade com base na documentação aplicável ao servidor. Não use a conta `sa` por aplicações.
