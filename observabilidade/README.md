# Observabilidade

Este componente reúne as ferramentas e integrações usadas para instrumentar, coletar, armazenar e explorar telemetria da plataforma.

## Subcomponentes

- [OpenTelemetry](./opentelemetry/README.md): instrumentação padronizada e protocolo OTLP para traces, métricas e logs.
- [Grafana](./grafana/README.md): painéis, exploração visual e alertas. Na configuração atual, não há datasource pré-configurado.
- [Kibana e Elastic Stack](./kibana/README.md): Elasticsearch para armazenar telemetria, Kibana para pesquisa e visualização, e Collector OTLP para ingestão.
- [Dynatrace](./dynatrace/README.md): integração externa opcional para monitoramento de serviços e workloads, agentes Kubernetes e eventos de deploy.

## Fluxo de telemetria

Aplicações instrumentadas podem enviar sinais por OTLP aos Collectors disponíveis. A stack principal recebe OTLP em `4317`/`4318` e registra os sinais no exporter `debug`. O Collector da Elastic Stack recebe em `14317`/`14318` e exporta logs, métricas e traces para Elasticsearch. Grafana é iniciado sem datasource configurado. Dynatrace é independente e requer ambiente e credenciais externos.

Os subcomponentes podem ser usados separadamente. Para iniciar a stack de referência com Docker Compose ou aplicar os manifests principais em Kubernetes, consulte [Execução da plataforma](../docs/deployment.md).
