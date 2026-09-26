# Entendimento do projeto

## Propósito

O Platform Environment PaaS é um repositório de referência para estudar e executar partes de uma plataforma de desenvolvimento e operação de aplicações. Reúne ferramentas de CI/CD, análise de qualidade, armazenamento, observabilidade, mensageria, exemplos de aplicações e toolboxes de nuvem. O projeto documenta suas decisões e práticas com IA-DLC e SDD.

## Organização funcional

- **CI/CD e qualidade:** GitLab, Jenkins e SonarQube.
- **Persistência:** `general-storage/` cataloga bancos relacionais e NoSQL. PostgreSQL integra a stack padrão; os demais são exemplos independentes.
- **Mensageria:** RabbitMQ, Kafka e ActiveMQ Artemis, com guias e artefatos próprios.
- **Observabilidade:** `observabilidade/` agrupa OpenTelemetry, Grafana, Kibana/Elastic Stack e Dynatrace como subcomponentes.
- **Aplicações de referência:** `backend-restful/` e `frontend-angular-react/` descrevem aplicações sem código executável de aplicação atualmente.
- **Nuvem:** `provedores-nuvem/` contém guias e toolbox de CLIs para provedores e plataformas.
- **Automação:** `scripts/` guarda utilitários PaaS, incluindo implementações e testes por linguagem.
- **Práticas de engenharia:** `iadlc-sdd/` documenta IA-DLC e SDD; `docs/decisions/` guarda ADRs.

## Execução e limites atuais

O Docker Compose na raiz combina serviços de laboratório: PostgreSQL, GitLab, Jenkins, SonarQube, Grafana, Collector OpenTelemetry e serviços Elastic/Kibana incluídos pelo Compose do subcomponente. Os serviços publicam portas em loopback; credenciais e limites locais estão descritos em `.env.example` e `docs/deployment.md`.

A base Kustomize em `kubernetes/base/` aplica os workloads principais no namespace `platform`, com PostgreSQL, Jenkins, SonarQube, Grafana e Collector. Ela pressupõe StorageClass adequada e credenciais do PostgreSQL criadas fora do repositório. ECK/Kibana e Dynatrace são instalados separadamente por exigirem operadores e recursos externos. A toolbox de nuvem e os bancos adicionais também são iniciados sob demanda.

Esta infraestrutura é uma base de avaliação, não uma configuração dimensionada ou endurecida para produção. Os exemplos de backend e frontend não têm código, imagem nem endpoints de health. O Collector da plataforma usa exporter `debug`; o Collector da Elastic Stack exporta sinais para Elasticsearch; Grafana não tem datasource inicial configurado. Dynatrace requer conta, tokens e configuração externos.

## Pontos de entrada

- [README principal](../README.md): catálogo dos componentes e instalação inicial.
- [Execução da plataforma](./deployment.md): Compose, Kubernetes, endereços locais e limitações.
- [Observabilidade](../observabilidade/README.md): visão geral e fluxo de telemetria.
- [Decisões de arquitetura](./decisions/): contexto e justificativas registradas.

Ao iniciar uma tarefa, consulte primeiro o README do componente envolvido e os ADRs relacionados. Trate os caminhos descritos aqui como orientação de navegação; confirme os manifests e comandos atuais antes de executá-los.
