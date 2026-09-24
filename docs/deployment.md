# Execução da plataforma

O Compose e os manifests Kubernetes deste repositório são uma base de avaliação. Não foram dimensionados nem endurecidos para produção. Os limites de CPU, memória e armazenamento do Kubernetes são valores iniciais para ajuste por medição.

## Docker Compose

Requisitos: Docker Engine e Docker Compose v2. O conjunto inclui PostgreSQL, GitLab CE, Jenkins, SonarQube Community Build, Grafana e OpenTelemetry Collector. GitLab e Jenkins, em particular, consomem bastante memória e disco; uma máquina pequena pode não conseguir executar todos simultaneamente.

```sh
cp .env.example .env
# Edite POSTGRES_PASSWORD em .env antes de iniciar.
docker compose up -d
docker compose ps
```

Interfaces locais padrão:

| Componente | Endereço |
|---|---|
| GitLab | http://localhost:8929 |
| Jenkins | http://localhost:8080 |
| SonarQube | http://localhost:9000 |
| Grafana | http://localhost:3000 |
| PostgreSQL | localhost:5432 |
| OTLP gRPC / HTTP | localhost:4317 / localhost:4318 |

Os volumes nomeados mantêm dados ao recriar containers. `docker compose down -v` remove os volumes e apaga esses dados. Os serviços publicam portas apenas no loopback do host. Configure senhas próprias antes de uso; a senha inicial do Jenkins é exibida nos logs. A imagem GitLab Omnibus executa serviços internos num único container e é apropriada aqui apenas para avaliação local.

Para validar a interpolação sem iniciar serviços:

```sh
docker compose --env-file .env.example config
```

## Kubernetes

Os manifests Kustomize implantam PostgreSQL, Jenkins, SonarQube, Grafana e o Collector no namespace `platform`. Eles pressupõem uma StorageClass padrão. Se o cluster não tiver uma, defina `storageClassName` nos PVCs de [workloads.yaml](../kubernetes/base/workloads.yaml). Recursos e tamanhos de PVC são pontos de partida.

Crie o Secret de banco fora do repositório, no mesmo namespace, e aplique a base:

```sh
kubectl create namespace platform
kubectl -n platform create secret generic postgresql-credentials --from-literal=password='substitua-por-um-segredo'
kubectl apply -k kubernetes/base
kubectl -n platform get pods
```

O comando de Secret acima coloca o valor no histórico do shell em algumas configurações; para uso real, injete-o por um secret manager ou um fluxo seguro de provisionamento. Objetos Secret do Kubernetes são codificados em base64 e não são criptografados no etcd por padrão. Configure criptografia em repouso e RBAC adequado no cluster.

GitLab usa o chart Helm oficial em Kubernetes. A documentação do GitLab alerta que a imagem Omnibus única cria ponto único de falha e não deve ser implantada como container Kubernetes; use o chart e defina valores de hostname, ingress, storage, registry e secrets para o cluster. Consulte [instalação do chart GitLab](https://docs.gitlab.com/charts/installation/deployment/) antes de instalar. Exemplo de preparação:

```sh
helm repo add gitlab https://charts.gitlab.io
helm repo update
# Revise um values.yaml próprio para o cluster antes de executar helm install.
```

Não há Service tipo LoadBalancer ou Ingress nesta base. Use `kubectl port-forward` para acesso local, por exemplo `kubectl -n platform port-forward svc/jenkins 8080:8080`.

## Aplicações e observabilidade

O backend e os frontends ainda não têm código, Dockerfile, dependências, portas ou endpoints de health; portanto, não há imagens ou workloads para eles. Quando os fontes existirem, cada aplicação deverá declarar o seu comando de execução, porta escutada, endpoint de health, configuração pública e forma de build. O frontend deve receber URL de API por configuração de build/runtime pública, sem segredos.

O Collector recebe OTLP em 4317/4318 e envia os sinais ao exporter `debug`, para inspeção em seus logs. Grafana é iniciado sem datasource e não armazena métricas ou traces. Escolha e configure backends compatíveis antes de tratar os dados exibidos como observabilidade persistente.

## Atualização de imagens

As imagens estão versionadas nos arquivos Compose e Kubernetes para tornar as referências reproduzíveis. Ao atualizar, escolha tags suportadas nos projetos upstream, avalie notas de release e compatibilidade de dados e altere Compose e Kubernetes juntos. Não reutilize volumes de dados entre versões sem seguir o procedimento de upgrade do produto.

O GitLab recomenda uma versão específica de imagem para instalações reais e documenta as três pastas persistentes e a configuração de portas para Compose: [GitLab em Docker](https://docs.gitlab.com/install/docker/installation/). Jenkins recomenda a imagem oficial `jenkins/jenkins`; em Kubernetes, seus dados ficam no volume persistente `/var/jenkins_home`: [Jenkins em Docker](https://www.jenkins.io/doc/book/installing/docker/). Consulte também [ADR-0001](./decisions/0001-compose-and-kubernetes.md).
