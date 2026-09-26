# Apache ActiveMQ Artemis

Broker multiprotocolo para filas e tópicos. O Artemis oferece suporte a AMQP, MQTT, OpenWire, Core e STOMP, sendo útil para integração com clientes JMS e sistemas legados. Este exemplo usa um broker único com console web.

## Docker Compose

```sh
cd mensageria/activemq-artemis
cp .env.example .env
# Edite .env e defina uma senha local.
docker compose up -d
docker compose logs -f artemis
```

Console: [http://localhost:8161](http://localhost:8161). Porta Core/OpenWire: `61616`; AMQP: `5672`; MQTT: `1883`. Configure o cliente para o protocolo correspondente. Dados e configuração persistem no volume `artemis-data`; `docker compose down -v` os apaga.

## Kubernetes

```sh
kubectl create namespace mensageria
kubectl -n mensageria create secret generic artemis-credentials --from-literal=username=platform --from-literal=password='<senha-local>'
kubectl apply -k mensageria/activemq-artemis/kubernetes
kubectl -n mensageria get pods,pvc,services
```

O DNS interno é `artemis.mensageria.svc`; faça port-forward para `8161` (console) ou para o protocolo necessário. O PVC pressupõe StorageClass padrão. Remova com `kubectl delete -k mensageria/activemq-artemis/kubernetes`.

## Referências

[Documentação oficial Apache Artemis](https://artemis.apache.org/components/artemis/documentation/latest/) · [Downloads e releases](https://artemis.apache.org/components/artemis/download/) · [Imagens Docker oficiais](https://artemis.apache.org/components/artemis/documentation/latest/docker.html)
