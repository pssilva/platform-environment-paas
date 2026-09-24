# Provedores de Nuvem

Componente de estudo e automação de linha de comando inspirado no repositório [provedor-nuvem-certifications](https://github.com/pssilva/provedor-nuvem-certifications). O projeto de referência descreve uma POC para aplicar conhecimentos de certificação a rotinas operacionais de desenvolvimento full stack em ambientes multicloud, com foco em SaaS, PaaS/FaaS e fluxos de CI/CD. Este componente organiza esses temas por provedor e oferece uma toolbox local para praticar comandos; ele não provisiona infraestrutura por conta própria.

## Subcomponentes

| Subcomponente | Escopo e CLI principal |
|---|---|
| [AWS](./aws/README.md) | Amazon Web Services; `aws` (AWS CLI v2) |
| [Azure](./azure/README.md) | Microsoft Azure; `az` (Azure CLI) |
| [GCP](./gcp/README.md) | Google Cloud; `gcloud` (Google Cloud CLI) |
| [Heroku Platform Cloud (HPC)](./heroku-hpc/README.md) | Plataforma Heroku; `heroku` (Heroku CLI) |
| [OCI](./oci/README.md) | Oracle Cloud Infrastructure; `oci` (OCI CLI) |
| [Red Hat OpenShift](./redhat-openshift/README.md) | Plataforma de aplicações Kubernetes; `oc` e `kubectl` |
| [Spring Cloud](./spring-cloud/README.md) | Ecossistema para aplicações distribuídas Java; `spring` (Spring Boot CLI) e ferramentas de build |

Spring Cloud é um conjunto de projetos/frameworks para sistemas distribuídos, não um provedor de nuvem público. O `spring` instalado pela toolbox é o CLI do Spring Boot, útil para criar e executar aplicações que podem usar Spring Cloud; não há um CLI único de administração do Spring Cloud.

## Toolbox Docker

A imagem inclui os sete CLIs, Java 21, Git e ferramentas básicas. Ela é destinada a sessões interativas e a exercícios locais. Os instaladores dos CLIs de nuvem acompanham as versões atuais dos respectivos repositórios; o Spring Boot CLI fica fixado em 4.1.1 no script. Reconstrua a imagem de forma controlada e registre o resultado no seu ambiente antes de usá-la em CI.

```bash
docker compose -f provedores-nuvem/compose.yaml build
docker compose -f provedores-nuvem/compose.yaml run --rm toolbox
```

Dentro do shell, por exemplo:

```bash
aws --version
az version
gcloud version
heroku --version
oci --version
oc version --client
spring --version
```

A pasta do projeto é montada como somente leitura em `/workspace`. O diretório pessoal da sessão fica em `tmpfs` e desaparece ao encerrar o container. Faça login somente em ambiente confiável; não grave chaves ou tokens na imagem, no repositório ou em argumentos de build. O estado de autenticação local não persiste depois que a sessão termina.

## Toolbox Kubernetes

Construa a imagem e disponibilize-a no runtime do cluster (por exemplo, carregando-a em um cluster local, ou usando um registry privado). O Pod de exemplo não cria Service nem monta credenciais:

```bash
docker build -t provedores-nuvem:dev -f provedores-nuvem/Dockerfile provedores-nuvem
# Disponibilize provedores-nuvem:dev ao cluster antes de aplicar o manifesto.
kubectl apply -f provedores-nuvem/kubernetes/pod.yaml
kubectl exec -it cloud-cli-toolbox -- bash
kubectl delete -f provedores-nuvem/kubernetes/pod.yaml
```

Em clusters locais, carregue a imagem no runtime antes de aplicar o Pod, por exemplo com `kind load docker-image provedores-nuvem:dev` ou `minikube image load provedores-nuvem:dev`.

O Pod executa como usuário sem privilégios, sem escalonamento, e mantém o diretório pessoal em `emptyDir` na memória. Ele não recebe credenciais por padrão. Para uso em cluster, prefira identidade federada/workload identity suportada pela plataforma; se precisar de arquivos de configuração, injete-os por Secret/secret manager e RBAC restrito, fora deste manifesto. Remover o Pod apaga o estado temporário.

Em clusters remotos, use o endereço de uma imagem publicada em um registry que o cluster possa acessar. Publique somente após revisar a imagem e suas versões de ferramentas, e substitua o campo `image` em `kubernetes/pod.yaml` pelo endereço e tag imutável do registry antes do `kubectl apply`. O repositório não publica imagens automaticamente.

## Instalação dos CLIs no host

O script comum oferece instalações independentes em Linux Ubuntu/Debian para os CLIs de nuvem; alguns provedores têm requisitos próprios. Leia o README do subcomponente antes de instalar. Os scripts usam repositórios e instaladores oficiais e podem instalar pacotes ou alterar arquivos do sistema; revise-os antes da execução.

```bash
bash provedores-nuvem/scripts/install-cli.sh aws
bash provedores-nuvem/scripts/install-cli.sh azure
bash provedores-nuvem/scripts/install-cli.sh gcp
bash provedores-nuvem/scripts/install-cli.sh heroku
bash provedores-nuvem/scripts/install-cli.sh oci
bash provedores-nuvem/scripts/install-cli.sh openshift
bash provedores-nuvem/scripts/install-cli.sh spring-cloud
```

`all` instala todos os CLIs de uma vez. A toolbox Docker executa essas mesmas rotinas durante o build.

## Organização

```text
provedores-nuvem/
├── aws/README.md
├── azure/README.md
├── gcp/README.md
├── heroku-hpc/README.md
├── oci/README.md
├── redhat-openshift/README.md
├── spring-cloud/README.md
├── scripts/install-cli.sh
├── kubernetes/pod.yaml
├── Dockerfile
└── compose.yaml
```

O conteúdo de certificações, trilhas de estudo e projetos de referência permanece no repositório de origem. Aqui ficam as instruções práticas de CLI e execução em containers.

O motivo para usar uma toolbox sem credenciais em vez de um serviço de aplicação está registrado em [ADR-0002](../docs/decisions/0002-cloud-cli-toolbox.md).
