# Platform Environment PaaS

Projeto de referência para uma plataforma PaaS que reúne ferramentas de CI/CD, qualidade, persistência, observabilidade e aplicações de exemplo.

Importante ter em mente que o presente projeto foi todo implementado usando IA-DLC e SDD (mais detalhes veja em [IA no ciclo de vida e SDD assistido por IA](./iadlc-sdd/README.md)).

## Componentes

- [GitLab](./gitlab/README.md)
- [Jenkins](./jenkins/README.md)
- [SonarQube](./sonarqube/README.md)
- [PostgreSQL](./postgresql/README.md)
- [OpenTelemetry](./opentelemetry/README.md)
- [Grafana](./grafana/README.md)
- [Aplicação Backend RESTful](./backend-restful/README.md)
- [Aplicações Frontend (Angular e React)](./frontend-angular-react/README.md)
- [IA no ciclo de vida e SDD assistido por IA](./iadlc-sdd/README.md)

Cada pasta documenta a finalidade do componente, seu papel na plataforma e pontos de integração. A infraestrutura de referência pode ser iniciada localmente com Docker Compose ou aplicada em Kubernetes; veja [Execução da plataforma](./docs/deployment.md). O backend RESTful e os frontends ainda são apenas descrições e não têm código para gerar imagens.


## 🚀 Começando

### 🔧 Instalação

Para obter o presente projeto use os seguintes comandos:

```bash
export ARTIFACT_ID="platform-environment-paas"
export WORK_PATH="${HOME}/projetos"
mkdir -p "${WORK_PATH}"
cd "${WORK_PATH}"
git clone https://github.com/pssilva/platform-environment-paas.git
cd "${ARTIFACT_ID}"
source ~/.bash_profile
idea .
```

#### 📋 Pré-requisitos

Depois de baixar o projeto: De que coisas precisamos para atuar no projeto `platform-environment-paas` e executá-lo?

Para isso, use os comandos do script de automação:

```bash

export ARTIFACT_ID="platform-environment-paas"
export TOOL_NAME="PaaSScriptsUteis"
export SCRIPT_PATH="${HOME}/projetos${ARTIFACT_ID}/scripts"
export AUTOMATION_PATH="${SCRIPT_PATH}/src/main/automation"
export TOOL_PATH="${AUTOMATION_PATH}/${TOOL_NAME}"

source "${TOOL_PATH}/PaaSScriptsUteis_main.sh"

PaaSScriptsUteis.installAllTools

```
