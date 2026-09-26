# OpenTelemetry

## Objetivo

Instrumentar aplicações e serviços para coletar telemetria de forma padronizada.

## Sinais

- **Traces:** acompanhar requisições entre frontend, backend e dependências.
- **Métricas:** observar latência, taxa de erros e uso de recursos.
- **Logs:** correlacionar eventos com traces quando possível.

## Integração

Instrumente o backend e, quando aplicável, os frontends com os SDKs e propagadores apropriados. Envie os dados via OTLP para um Collector configurado para exportar a destinos compatíveis, incluindo Grafana e seus componentes de observabilidade. Evite incluir dados pessoais ou segredos na telemetria.

