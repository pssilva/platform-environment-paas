# Apache Kafka

Plataforma distribuída de eventos organizada em tópicos e partições. Eventos são retidos conforme configuração e podem ser lidos novamente; grupos de consumidores coordenam o processamento. O broker único deste laboratório usa KRaft, sem ZooKeeper.

## Docker Compose

```sh
cd mensageria/kafka
docker compose up -d
docker compose logs -f kafka
```

Bootstrap local: `localhost:9092`. O volume `kafka-data` mantém os dados entre reinicializações; `docker compose down -v` apaga os dados. Não use esta configuração para produção ou para avaliar disponibilidade de cluster.

## Kubernetes

```sh
kubectl create namespace mensageria
kubectl apply -k mensageria/kafka/kubernetes
kubectl -n mensageria get pods,pvc,services
```

Clientes dentro do cluster usam `kafka.mensageria.svc:9092`. Como o broker anuncia esse endereço interno, clientes fora do cluster precisam de configuração específica de listener/advertised listener; um port-forward simples não basta para completar a descoberta Kafka. O PVC precisa de StorageClass padrão. Remova com `kubectl delete -k mensageria/kafka/kubernetes`.

## Referências

[Documentação oficial do Kafka: Docker](https://kafka.apache.org/documentation/#docker) · [Conceitos e configuração](https://kafka.apache.org/documentation/)
