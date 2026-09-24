# Kibana e Elastic Stack

## Objetivo

Kibana é a interface para explorar, visualizar e correlacionar dados armazenados no Elasticsearch. Neste componente, aplicações distribuídas enviam logs, métricas e traces por OpenTelemetry Protocol (OTLP) ao OpenTelemetry Collector; o Collector grava os sinais no Elasticsearch, que Kibana consulta para investigação e dashboards.

## Componentes e fluxo de dados

```text
Aplicações instrumentadas
          │ OTLP (logs, métricas e traces)
          ▼
OpenTelemetry Collector ──► Elasticsearch ◄── Kibana
                                  índices e        Discover,
                                  data streams      dashboards
```

- **Elasticsearch** indexa, armazena e pesquisa os sinais.
- **Kibana** explora documentos, monta dashboards e ajuda a investigar falhas relacionadas a serviços distribuídos.
- **OpenTelemetry Collector** recebe OTLP, agrupa os sinais e os exporta ao Elasticsearch.
- **Logstash** é opcional e pode ser adicionado quando fontes legadas exigirem parsing e enriquecimento de eventos antes da indexação. Este componente usa OTLP e Collector para a ingestão de telemetria.

O Exporter Elasticsearch do Collector grava logs, métricas e traces em data streams com mapeamento nativo OpenTelemetry. Instrumente cada serviço com atributos consistentes, em especial `service.name`, `service.namespace`, `deployment.environment.name` e `trace_id`/`span_id` quando aplicável, para filtrar e correlacionar eventos. A configuração básica disponibiliza os dados para busca e dashboards; recursos APM especializados, como mapas de serviço, podem exigir o gateway Elastic Agent/APM e enriquecimento adicional.

## Docker Compose

O [compose.yaml](./compose.yaml) sobe Elasticsearch, Kibana e um Collector OTLP para avaliação local. Elasticsearch e Kibana usam a mesma versão `9.5.4`. O Elasticsearch fica em modo single-node, com segurança desativada e dados persistidos em volume; as portas publicadas ficam limitadas ao loopback do host. **Use esta configuração apenas localmente; ela não protege o Elasticsearch com autenticação ou TLS.**

Requisitos: Docker Engine, Docker Compose v2.20 ou superior e pelo menos 4 GiB de memória disponíveis para o Docker. Como esta configuração usa Elasticsearch 9.5.4, configure `vm.max_map_count` no host para `1048576` antes de iniciar:

```sh
sudo sysctl -w vm.max_map_count=1048576
```

Inicie somente este componente:

```sh
docker compose -f kibana/compose.yaml up -d
docker compose -f kibana/compose.yaml ps
```

Ou inicie a plataforma completa, que inclui este Compose:

```sh
docker compose up -d
```

Interfaces locais:

| Serviço | Endereço |
|---|---|
| Kibana | <http://localhost:5601> |
| Elasticsearch API | <http://localhost:9200> |
| OTLP gRPC | `localhost:14317` |
| OTLP HTTP | `localhost:14318` |

Configure as aplicações para exportar OTLP a `http://localhost:14317` (gRPC) ou `http://localhost:14318` (HTTP/protobuf). Aplicações em containers da mesma stack podem enviar para `elastic-otel-collector:4317` ou `elastic-otel-collector:4318`. Depois, em Kibana, use **Discover** e selecione (ou crie) data views `logs-*-*`, `metrics-*-*` ou `traces-*-*`; os índices só aparecem após a chegada de sinais.

`docker compose -f kibana/compose.yaml down` preserva os dados. `docker compose -f kibana/compose.yaml down -v` remove o volume do Elasticsearch. A stack completa também remove esse volume se executada com `docker compose down -v` na raiz.

## Kubernetes com ECK

Em Kubernetes, Elasticsearch e Kibana são gerenciados pelo [Elastic Cloud on Kubernetes (ECK)](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html). O operador instala CRDs com escopo de cluster e cria os recursos com TLS e credenciais gerenciadas. O arquivo [elastic-stack.yaml](./kubernetes/elastic-stack.yaml) define Elasticsearch e Kibana no namespace `platform`; [otel-collector.yaml](./kubernetes/otel-collector.yaml) define um Collector OTLP com TLS e chave de ingestão com permissões limitadas.

### Instalação

Pré-requisitos: cluster Kubernetes com uma StorageClass padrão, namespace `platform` criado e permissões de administrador do cluster para instalar o operador ECK. A instalação cluster-wide do operador e de suas CRDs é necessária para que os recursos `Elasticsearch` e `Kibana` sejam reconhecidos.

Instale uma versão específica do operador seguindo os manifests oficiais e aplique os recursos Elasticsearch/Kibana:

```sh
kubectl create -f https://download.elastic.co/downloads/eck/3.5.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/3.5.0/operator.yaml
kubectl apply -f kibana/kubernetes/elastic-stack.yaml
kubectl get elasticsearch,kibana --namespace platform
```

Espere até Elasticsearch e Kibana estarem prontos. A senha inicial do usuário `elastic` é armazenada pelo operador no Secret `elasticsearch-es-elastic-user` no namespace `platform` e pode ser lida assim:

```sh
kubectl get secret elasticsearch-es-elastic-user --namespace platform \
  -o go-template='{{.data.elastic | base64decode}}'
```

Entre no Kibana via port-forward:

```sh
kubectl port-forward --namespace platform service/kibana-kb-http 5601:5601
```

Abra <https://localhost:5601> e autentique-se com o usuário `elastic`. O certificado é autoassinado para avaliação local; em ambientes reais, configure certificados confiáveis.

### Habilitar ingestão OTLP no Kubernetes

Crie uma API key para o Collector pelo **Dev Tools** do Kibana. Ela deve ter somente os privilégios `auto_configure` e `create_doc` nos data streams `logs-*`, `metrics-*` e `traces-*`:

```http
POST /_security/api_key
{
  "name": "otel-collector",
  "role_descriptors": {
    "otel_ingest": {
      "cluster": [],
      "indices": [
        {
          "names": ["logs-*", "metrics-*", "traces-*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    }
  }
}
```

Salve o campo `encoded` retornado em um arquivo local protegido e crie o Secret sem versionar a chave:

```sh
kubectl create secret generic elasticsearch-otel-api-key \
  --namespace platform \
  --from-file=api_key=/caminho-seguro/api-key-encoded
kubectl apply -f kibana/kubernetes/otel-collector.yaml
kubectl get pods,services --namespace platform
```

Dentro do cluster, configure as aplicações para enviar OTLP ao Collector em `elastic-otel-collector.platform.svc.cluster.local`, porta `4317` para gRPC ou `4318` para HTTP/protobuf. Os endpoints só são expostos por Services internos do tipo ClusterIP.

## Operação e limites

- A configuração de um nó e volumes de 10 GiB são valores iniciais para avaliação, não uma arquitetura de alta disponibilidade.
- Configure retenção e políticas de ciclo de vida dos data streams, snapshots e restauração antes de armazenar dados relevantes.
- Não envie segredos, dados pessoais desnecessários ou payloads sensíveis para logs e traces.
- Kibana mostra apenas dados que foram ingeridos e ainda estão retidos no Elasticsearch; instrumente serviços e valide atributos, timestamps e propagação de contexto distribuído.
- A configuração local Docker desativa segurança. Kubernetes usa TLS e API key de ingestão; para produção, planeje acesso, certificados, retenção, capacidade e backup.

## Referências oficiais

- [Instalar Kibana com Docker](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-kibana-with-docker)
- [Instalar Elasticsearch localmente](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/local-development-installation-quickstart)
- [Elastic Cloud on Kubernetes](https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html)
- [Elasticsearch Exporter do OpenTelemetry Collector Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter)
- [Requisito de memória virtual do Elasticsearch](https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/virtual-memory)
