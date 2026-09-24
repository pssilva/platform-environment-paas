# Dynatrace: monitoramento de deploy e saúde de microsserviços

Dynatrace é uma plataforma de observabilidade que correlaciona telemetria de aplicações, serviços, hosts e Kubernetes. O **OneAgent** descobre serviços, coleta métricas/traces e instrumenta processos compatíveis. O **Dynatrace Operator** administra OneAgent, ActiveGate e módulos de código no cluster Kubernetes. O ActiveGate roteia telemetria e pode consultar plataformas/tecnologias por API; sozinho, não substitui a instrumentação dos serviços pelo OneAgent. [Visão geral oficial do Dynatrace](https://docs.dynatrace.com/docs/discover-dynatrace/what-is-dynatrace) · [OneAgent](https://docs.dynatrace.com/docs/ingest-from/dynatrace-oneagent) · [ActiveGate](https://docs.dynatrace.com/docs/ingest-from/dynatrace-activegate)

Este componente combina a imagem oficial OneAgent para Docker, o Operator com um recurso `DynaKube` para Kubernetes e um exemplo de envio de evento de deploy para integrar CI/CD. Os artefatos não criam uma conta Dynatrace nem são iniciados pela stack padrão do repositório.

## Como relacionar deploy e saúde

1. OneAgent ou Dynatrace Operator coleta telemetria dos serviços e dependências. A instrumentação identifica taxas de erro, latência, throughput e relações entre serviços.
2. Use **Services** para acompanhar o estado e investigar falhas/latência; use **Problems** para analisar incidentes correlacionados e a causa provável. Configure SLOs para disponibilidade, taxa de sucesso ou latência de acordo com o serviço. [Services](https://docs.dynatrace.com/docs/observe/application-observability/services/services-app) · [SLOs](https://docs.dynatrace.com/docs/deliver/service-level-objectives)
3. Ao terminar um deploy, a pipeline executa [scripts/send-deployment-event.py](./scripts/send-deployment-event.py). O evento liga o horário, serviço, versão e commit do deploy às mudanças de telemetria observadas.
4. Opcionalmente, configure um Workflow para ouvir o evento `deployment finished` e disparar validação de um Site Reliability Guardian. A pipeline pode então promover ou bloquear a release conforme o resultado. [Validação automática de releases](https://docs.dynatrace.com/docs/deliver/quality-gates)

## Pré-requisitos

- Um ambiente Dynatrace SaaS ou Managed com permissão para configurar OneAgent/Operator e consultar telemetria.
- Docker Engine em host Linux para o modo OneAgent via container; Docker Desktop monitora sua VM Linux, não o host macOS/Windows subjacente.
- Para Kubernetes, acesso administrativo para instalar o Dynatrace Operator, seus CRDs e recursos de cluster.
- Token PaaS/installer apropriado para baixar OneAgent; tokens do Operator e de ingestão para Kubernetes; token de ingestão SDLC para o script de deploy. Consulte os escopos atuais na documentação oficial.

## Docker em host Linux

A configuração usa a imagem oficial `dynatrace/oneagent`; por isso, este componente não precisa de Dockerfile próprio. OneAgent via container requer acesso ao PID e à rede do host, filesystem raiz montado, armazenamento persistente e capacidades Linux específicas. O Compose concede somente as capabilities listadas no guia da Dynatrace e não usa `privileged`; ainda assim, a montagem `/:/mnt/root`, `SYS_ADMIN`, `SYS_PTRACE` e o perfil AppArmor ampliam o acesso do agente ao host. Revise as permissões e o perfil com a equipe de segurança antes de iniciar. [Instalar OneAgent como container Docker](https://docs.dynatrace.com/docs/ingest-from/setup-on-container-platforms/docker/set-up-dynatrace-oneagent-as-docker-container) · [Privilégios de container](https://docs.dynatrace.com/docs/ingest-from/setup-on-container-platforms/oneagent-privileges)

Obtenha a URL do instalador e o token na página **Dynatrace Hub → OneAgent → Set up → Linux**. A URL é específica do ambiente e contém parâmetros de instalação; trate-a como dado sensível. Copie o exemplo de ambiente, escolha uma tag OneAgent suportada e preencha os valores localmente:

```bash
cp dynatrace/.env.example dynatrace/.env
# Edite dynatrace/.env localmente; nunca versione o arquivo preenchido.
docker compose --env-file dynatrace/.env -f dynatrace/compose.yaml up -d
docker compose --env-file dynatrace/.env -f dynatrace/compose.yaml ps
docker compose --env-file dynatrace/.env -f dynatrace/compose.yaml logs -f oneagent
```

O `.env` é ignorado pelo Git. Variáveis de ambiente do container podem ser vistas por usuários com acesso ao daemon Docker; use host controlado e restrinja esse acesso. Para remover o agente:

```bash
docker compose --env-file dynatrace/.env -f dynatrace/compose.yaml down
```

O volume `oneagent-storage` mantém arquivos do OneAgent entre reinicializações. O host deve ter `/opt` e ser Linux. O modelo de OneAgent container é destinado a instrumentar o host Docker e seus containers; para uma imagem isolada de aplicação sem acesso ao host, veja [OneAgent application-only](https://docs.dynatrace.com/docs/ingest-from/setup-on-container-platforms/docker/set-up-oneagent-on-containers-for-application-only-monitoring).

## Kubernetes com Dynatrace Operator

O Operator é a forma recomendada de aplicar OneAgent e ActiveGate ao cluster. O exemplo usa `applicationMonitoring` e o ActiveGate com capacidades `routing` e `kubernetes-monitoring`; ele habilita instrumentação de workloads compatíveis. Confira escopo de namespaces, versões suportadas, compatibilidade da plataforma e sizing antes de usar em cluster compartilhado. [Guia oficial de application observability](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/deployment/application-observability)

Instale o chart do Operator (versão de exemplo fixada em 1.10.2; confirme a versão recomendada e suportada para seu cluster):

```bash
helm upgrade --install dynatrace-operator \
  oci://public.ecr.aws/dynatrace/dynatrace-operator \
  --version 1.10.2 \
  --create-namespace \
  --namespace dynatrace
```

Crie o Secret a partir de arquivos locais protegidos, sem colocar o conteúdo do token no histórico do shell ou em um manifesto versionado. Os arquivos devem conter os tokens requeridos pelo Operator com seus escopos adequados:

```bash
kubectl -n dynatrace create secret generic dynakube \
  --from-file=apiToken=/caminho-seguro/operator-token \
  --from-file=dataIngestToken=/caminho-seguro/data-ingest-token
```

Edite `kubernetes/dynakube.yaml` e troque `<environment-id>` pela URL base do seu ambiente. Depois aplique e acompanhe os recursos:

```bash
kubectl apply -f dynatrace/kubernetes/dynakube.yaml
kubectl get dynakube -n dynatrace
kubectl get pods -n dynatrace
```

O Operator instala CRDs, webhook e componentes de monitoramento com permissões de cluster. O manifesto acompanha a API `dynatrace.com/v1beta5`; verifique a versão do Operator e a API `DynaKube` suportada antes de atualizar. Não aplique o manifesto sem antes instalar o Operator e criar o Secret. A remoção do recurso `DynaKube` interrompe a instrumentação; desinstale o Operator somente depois de avaliar o impacto:

```bash
kubectl delete -f dynatrace/kubernetes/dynakube.yaml
helm uninstall dynatrace-operator -n dynatrace
```

## Enviar eventos de deploy do CI/CD

O script usa apenas Python padrão e exige um token API Dynatrace com permissão de ingestão SDLC (`openpipeline.events_sdlc` para o token Classic; consulte a configuração atual de ingestão se usar Platform token). Ele retorna sucesso apenas quando a API aceita o evento com HTTP 202. Armazene o token em variável protegida do CI ou secret manager.

Configure as variáveis no job que roda após o deploy:

```bash
export DT_ENVIRONMENT_URL="https://<environment-id>.live.dynatrace.com"
export DT_API_TOKEN="<injetado-pelo-secret-manager>"
export DT_DEPLOYMENT_ID="${CI_PIPELINE_ID}"
export DT_DEPLOYMENT_NAME="orders-api"
export DT_RELEASE_STAGE="staging"
export DT_DEPLOYMENT_STATUS="succeeded"
export DT_COMMIT_SHA="${CI_COMMIT_SHA}"
export DT_REPOSITORY_URL="${CI_PROJECT_URL}"
python3 dynatrace/scripts/send-deployment-event.py
```

O script envia `deployment finished` ao endpoint `/platform/ingest/v1/events.sdlc`. Na aplicação Dynatrace, configure um Workflow com filtro de evento, por exemplo `event.kind == "SDLC_EVENT" AND event.type == "deployment" AND event.status == "finished"`, e ligue-o a um Site Reliability Guardian com objetivos de saúde do serviço. [Ingest SDLC events](https://docs.dynatrace.com/docs/deliver/pipeline-observability-sdlc-events/sdlc-events) · [Modelo de eventos SDLC](https://docs.dynatrace.com/docs/semantic-dictionary/model/sdlc-events)

## Arquivos

```text
dynatrace/
├── compose.yaml
├── .env.example
├── kubernetes/dynakube.yaml
├── scripts/send-deployment-event.py
└── README.md
```

As opções do ambiente e o motivo para manter a instalação fora da stack padrão estão descritos em [ADR-0003](../docs/decisions/0003-dynatrace-agent-deployment.md).
