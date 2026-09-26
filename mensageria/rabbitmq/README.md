# RabbitMQ

Broker de mensagens orientado a filas, com roteamento por exchanges e bindings. Suporta AMQP 0-9-1 e AMQP 1.0, acknowledgements, confirmações do publisher, filas duráveis e plugins. A imagem `management` inclui console web para laboratório.

## Docker Compose

```sh
cd mensageria/rabbitmq
cp .env.example .env
# Edite .env e defina uma senha local.
docker compose up -d
docker compose ps
```

Console: [http://localhost:15672](http://localhost:15672). Porta AMQP: `5672`. As portas publicadas são limitadas a `127.0.0.1`. Dados ficam no volume `rabbitmq-data`; `docker compose down -v` apaga o volume.

## Kubernetes

Crie o Secret e aplique os manifests:

```sh
kubectl create namespace mensageria
kubectl -n mensageria create secret generic rabbitmq-credentials --from-literal=username=platform --from-literal=password='<senha-local>'
kubectl apply -k mensageria/rabbitmq/kubernetes
kubectl -n mensageria get pods,pvc,services
```

Clientes no cluster usam `rabbitmq.mensageria.svc:5672`. Faça port-forward para console (15672) ou AMQP (5672) se necessário. Use um secret manager em clusters compartilhados; evite inserir senhas no histórico do shell. PVC pressupõe StorageClass padrão. Remova com `kubectl delete -k mensageria/rabbitmq/kubernetes`.

## Referências

[Documentação oficial RabbitMQ](https://www.rabbitmq.com/docs) · [Instalação e imagem Docker](https://www.rabbitmq.com/docs/download) · [Management plugin](https://www.rabbitmq.com/docs/management)
