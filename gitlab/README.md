# GitLab

## Objetivo

Oferecer hospedagem de código-fonte, controle de versões e colaboração para os projetos da plataforma. O GitLab também pode executar pipelines CI/CD e disponibilizar um Container Registry.

## Responsabilidades e integrações

- Hospedar os repositórios do backend e dos frontends.
- Gerenciar branches, merge requests, usuários e permissões.
- Integrar commits e merge requests com Jenkins e SonarQube.
- Armazenar credenciais de pipeline em variáveis protegidas, nunca no repositório.

## Execução com Docker Compose

O arquivo [compose.yaml](./compose.yaml) executa a imagem oficial GitLab Community Edition (`gitlab/gitlab-ce:19.4.1-ce.0`) para avaliação local. Ele persiste configuração, logs e dados em volumes nomeados e publica portas somente no loopback do host.

Requisitos: Docker Engine e Docker Compose v2. O GitLab consome bastante memória, CPU e disco; dimensione a máquina conforme a documentação oficial antes de iniciar.

```sh
cp gitlab/.env.example gitlab/.env
docker compose --env-file gitlab/.env -f gitlab/compose.yaml up -d
docker compose --env-file gitlab/.env -f gitlab/compose.yaml ps
```

Acesse <http://localhost:8929>. A senha inicial do usuário `root` é gerada pelo GitLab e pode ser consultada nos logs:

```sh
docker compose --env-file gitlab/.env -f gitlab/compose.yaml logs gitlab
```

O SSH para operações Git fica publicado em `localhost:2224`. Os valores podem ser alterados em `gitlab/.env`. `docker compose ... down` preserva os volumes; `docker compose ... down -v` apaga a configuração, os logs e os dados persistidos.

O serviço GitLab também está incluído na [stack Compose da plataforma](../compose.yaml), com os mesmos valores padrão de imagem e portas. Escolha uma das duas formas de execução; não inicie ambas ao mesmo tempo, pois usam as mesmas portas do host.

## Execução em Kubernetes com Helm

Para Kubernetes, este componente usa o [Helm chart oficial do GitLab](https://docs.gitlab.com/charts/installation/deployment/), em vez de executar a imagem Omnibus como um Pod. O chart requer PostgreSQL, Redis e armazenamento de objetos externos. Essas dependências não são implantadas pelo chart nas versões recentes; o cluster deve fornecê-las antes da instalação. Para avaliação local, a documentação oficial descreve uma opção de provisionamento de dependências externas.

O arquivo [kubernetes/values.yaml](./kubernetes/values.yaml) contém os valores iniciais: edição Community, nome DNS, acesso HTTP local, referências aos serviços externos e nomes dos Secrets. Edite os hosts e ajuste o tamanho do armazenamento conforme o cluster. Os Secrets devem ser criados no namespace da instalação, fora do repositório.

### Pré-requisitos

- Cluster Kubernetes acessível por `kubectl` e Helm compatível com os requisitos atuais do chart.
- PostgreSQL com banco e usuário dedicados ao GitLab.
- Redis/Valkey acessível pelo cluster.
- Armazenamento de objetos compatível com S3, com buckets para os dados do GitLab e do Container Registry.
- StorageClass com provisionamento dinâmico e capacidade adequada aos PVCs do chart.
- DNS/rede configurados para o hostname definido em `global.hosts.gitlab.name`. Para acesso de avaliação local, o padrão `gitlab.localhost` pode ser usado com port-forward.

O chart padrão usado aqui é a versão `10.4.1`, correspondente ao GitLab `19.4.1`. A documentação atual do chart requer Helm 4; consulte o [mapeamento oficial de versões](https://docs.gitlab.com/charts/installation/version_mappings/) antes de atualizar qualquer uma delas.

### Instalação

Crie o namespace e os Secrets a partir de arquivos locais protegidos. Os arquivos de senha e configuração do armazenamento não devem ser versionados.

```sh
kubectl create namespace gitlab
kubectl -n gitlab create secret generic gitlab-postgres \
  --from-file=psql-password=/caminho-seguro/senha-postgres
kubectl -n gitlab create secret generic gitlab-redis \
  --from-file=redis-password=/caminho-seguro/senha-redis
kubectl -n gitlab create secret generic gitlab-object-storage \
  --from-file=connection=/caminho-seguro/rails-object-storage.yml
kubectl -n gitlab create secret generic gitlab-registry-storage \
  --from-file=config=/caminho-seguro/registry-storage.yml
```

Os arquivos versionados [rails-object-storage.yml.example](./kubernetes/rails-object-storage.yml.example) e [registry-storage.yml.example](./kubernetes/registry-storage.yml.example) mostram o formato esperado para AWS S3. Copie-os para um local seguro, preencha as credenciais e os endpoints do provedor e use os arquivos resultantes nos comandos acima. Crie previamente os buckets indicados nos arquivos e em `kubernetes/values.yaml`. Consulte a [configuração oficial de armazenamento externo](https://docs.gitlab.com/charts/advanced/external-object-storage/) para outros provedores S3 compatíveis ou armazenamento em nuvem.

Copie os valores de referência para um arquivo local ignorado pelo Git, configure nele os endpoints, adicione o repositório Helm oficial e instale o chart:

```sh
cp gitlab/kubernetes/values.yaml gitlab/kubernetes/values.local.yaml
# Ajuste hosts e endpoints externos em gitlab/kubernetes/values.local.yaml.
helm repo add gitlab https://charts.gitlab.io/
helm repo update
helm upgrade --install gitlab gitlab/gitlab \
  --namespace gitlab \
  --version 10.4.1 \
  --timeout 600s \
  --values gitlab/kubernetes/values.local.yaml
```

Verifique os recursos e acompanhe a instalação, que pode levar vários minutos:

```sh
helm status gitlab --namespace gitlab
kubectl get pods,pvc --namespace gitlab
```

Para acessar localmente, liste os Services com `kubectl get services --namespace gitlab`, encaminhe a porta 8181 do Service webservice e abra `http://gitlab.localhost:8181` (ou o hostname que você configurou):

```sh
kubectl port-forward --namespace gitlab service/gitlab-webservice-default 8181:8181
```

Consulte a senha inicial de `root` no Secret criado pelo chart, conforme o procedimento da [documentação oficial](https://docs.gitlab.com/charts/installation/deployment/#initial-login).

> Esta configuração é uma base de avaliação, não uma arquitetura de produção. Em produção, configure TLS, DNS e ingress apropriados, dimensione os componentes, proteja os Secrets no etcd e estabeleça backup e restauração para banco, repositórios e armazenamento de objetos.

## Atualização

Atualize a versão do chart de forma deliberada e verifique a compatibilidade com a versão do GitLab e com as migrações de dados. Siga as [instruções oficiais de upgrade](https://docs.gitlab.com/charts/installation/upgrade/); não atualize imagens isoladamente nem reutilize dados sem revisar o procedimento de upgrade.
