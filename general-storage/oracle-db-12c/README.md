# Oracle Database 12c

Banco relacional Oracle da família 12c, encontrado em ambientes corporativos e sistemas legados. Compatibilidade, versão exata (12.1 ou 12.2), suporte e licenciamento devem ser confirmados com a documentação e os contratos aplicáveis.

## Observação sobre XE

“Oracle Database 12c XE” não corresponde a uma edição XE publicada pela Oracle. A página oficial de downloads de XE lista 18c; a documentação de migração também trata de XE 11.2 para 18c e depois 21c. Por isso, este guia cobre Oracle Database 12c em geral. Se o objetivo for laboratório com XE, consulte a [documentação e downloads de Oracle Database 18c XE](https://www.oracle.com/database/technologies/express-edition-downloads.html). XE tem limites e não recebe patches de segurança, conforme o [FAQ oficial](https://www.oracle.com/database/technologies/appdev/xe/18c-faq.html); avalie os termos atuais antes de usar.

## CLI: SQL*Plus

Instale o Oracle Instant Client com SQL*Plus para a plataforma desejada, seguindo a [documentação oficial de SQL*Plus](https://docs.oracle.com/en/database/oracle/oracle-database/12.2/sqpug/SQL-Plus-quick-start.html). Configure o endereço de um servidor já provisionado:

```sh
export ORACLE_HOST=localhost
export ORACLE_PORT=1521
export ORACLE_SERVICE=ORCLPDB1
export ORACLE_USER=app_user
bash general-storage/scripts/connect/oracle-db-12c.sh
```

SQL*Plus solicita a senha. No prompt, execute `SELECT sysdate FROM dual;` e `EXIT` para sair. Nome do serviço e método de autenticação dependem da configuração do servidor; confirme-os com o DBA. Não use a conta administrativa `SYS` pela aplicação.

## Imagem Docker

A Oracle fornece Dockerfiles de exemplo, mas não oferece download automático do binário de Oracle Database 12c por esse projeto. Para 12c Release 2, baixe legalmente a mídia Linux x86-64 aplicável, aceite os termos Oracle e coloque o arquivo ZIP sem descompactar em `OracleDatabase/SingleInstance/dockerfiles/12.2.0.1/` do repositório oficial [`oracle/docker-images`](https://github.com/oracle/docker-images/tree/main/OracleDatabase/SingleInstance). Então construa a edição que sua licença permite:

```sh
git clone https://github.com/oracle/docker-images.git /tmp/oracle-docker-images
cd /tmp/oracle-docker-images/OracleDatabase/SingleInstance/dockerfiles
# Copie a mídia licenciada para ./12.2.0.1/ antes do build.
./buildContainerImage.sh -v 12.2.0.1 -s -t oracle/database:12.2.0.1-se2
```

O exemplo seleciona Standard Edition 2 (`-s`); use a opção de edição compatível com a mídia e sua licença. Ajuste `ORACLE_IMAGE` em `.env.example` se a tag construída for diferente. A documentação do projeto oficial lista 12.2.0.1 entre as versões de exemplo e exige a mídia fornecida pelo usuário para 12c.

## Docker Compose

Após construir a imagem, execute o Compose isolado. A inicialização pode ser demorada; os dados ficam no volume nomeado.

```sh
cd general-storage/oracle-db-12c
cp .env.example .env
# Ajuste ORACLE_PWD e confirme que ORACLE_IMAGE corresponde à imagem construída.
docker compose up -d
docker compose ps
docker compose logs -f oracle-db
```

## Kubernetes

O StatefulSet pede 20 Gi de armazenamento e usa a mesma imagem local/privada, que precisa estar disponível no runtime do cluster. Injete a senha por secret manager; o comando abaixo é apenas exemplo local.

```sh
kubectl create namespace general-storage
kubectl -n general-storage create secret generic oracle-db-credentials --from-literal=password='<senha-local>'
kubectl apply -k general-storage/oracle-db-12c/kubernetes
kubectl -n general-storage get pods,pvc,services
kubectl -n general-storage port-forward svc/oracle-db 1521:1521
```

A conexão interna usa `oracle-db.general-storage.svc:1521`. Configure o serviço/alias correto no SQL*Plus. Oracle 12c requer atenção especial a suporte, plataforma compatível e termos de licença; estes manifests são somente uma base de laboratório.
