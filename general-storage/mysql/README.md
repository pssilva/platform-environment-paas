# MySQL

Banco relacional open source com ampla adoção em aplicações web. Use quando SQL, transações e a compatibilidade com o ecossistema MySQL atenderem ao modelo e às necessidades operacionais da aplicação.

## CLI: `mysql` e MySQL Shell

Instale os clientes por meio dos [repositórios e instruções oficiais](https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-shell-install-linux-quick.html). Para uma sessão SQL tradicional:

```sh
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_DATABASE=app
export MYSQL_USER=app_user
bash general-storage/scripts/connect/mysql.sh
```

O cliente solicita a senha interativamente. Também é possível usar MySQL Shell (`mysqlsh`) para administração e automação; consulte o [manual oficial do MySQL Shell](https://dev.mysql.com/doc/mysql-shell/8.4/en/).

No prompt, tente `SELECT VERSION();` e `SHOW TABLES;`. O script conecta a um servidor existente, não o provisiona. Planeje backups, replicação, atualizações e privilégios mínimos para cada aplicação.

## Docker Compose

O Compose isolado usa a imagem oficial MySQL 8.4 e volume nomeado. O usuário da aplicação e o banco são criados na primeira inicialização; o root é administrativo.

```sh
cd general-storage/mysql
cp .env.example .env
# Troque as duas senhas de exemplo.
docker compose up -d
docker compose ps
docker compose logs -f mysql
```

## Kubernetes

O StatefulSet solicita um PVC de 10 Gi. Crie um Secret com as chaves `app-password` e `root-password` em `general-storage` por meio de um secret manager ou provisionamento seguro:

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic mysql-credentials --from-literal=app-password='<senha-app>' --from-literal=root-password='<senha-root>'
kubectl apply -k general-storage/mysql/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/mysql 3306:3306
```

Os parâmetros `--from-literal` são apenas ilustrativos: valores podem aparecer no histórico. Internamente, o serviço atende em `mysql.general-storage.svc:3306`. As variáveis de inicialização da imagem só criam usuário/banco quando o diretório de dados está vazio; alteração posterior de Secret não troca automaticamente credenciais já gravadas no volume. Veja a [imagem oficial MySQL](https://hub.docker.com/_/mysql).
