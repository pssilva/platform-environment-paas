# Platform Environment PaaS

Projeto de referência para uma plataforma PaaS que reúne ferramentas de CI/CD, qualidade, persistência, observabilidade e aplicações de exemplo.

Importante ter em mente que o presente projeto foi todo implementado usando IA-DLC e SDD (mais detalhes veja em [IA no ciclo de vida e SDD assistido por IA](./iadlc-sdd/README.md)).

## Componentes

- [GitLab](./gitlab/README.md)
- [Jenkins](./jenkins/README.md)
- [SonarQube](./sonarqube/README.md)
- [Armazenamentos Gerais: bancos relacionais e NoSQL](./general-storage/README.md)
- [Observabilidade](./observabilidade/README.md)
- [Aplicação Backend RESTful](./backend-restful/README.md)
- [Aplicações Frontend (Angular e React)](./frontend-angular-react/README.md)
- [IA no ciclo de vida e SDD assistido por IA](./iadlc-sdd/README.md)
- [Provedores de nuvem e toolbox de CLIs](./provedores-nuvem/README.md)

Cada pasta documenta a finalidade do componente, seu papel na plataforma e pontos de integração. Armazenamentos Gerais reúne guias e artefatos Compose/Kubernetes independentes para bancos relacionais e NoSQL; a stack padrão continua iniciando somente o PostgreSQL. A infraestrutura de referência pode ser iniciada localmente com Docker Compose ou aplicada em Kubernetes; veja [Execução da plataforma](./docs/deployment.md). Backend e frontends ainda são descrições sem código de aplicação. O componente Provedores de Nuvem oferece uma toolbox de linha de comando e documentação de estudo; Dynatrace é uma integração opcional com uma conta externa e monitora os workloads configurados.


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

Para executar a plataforma, instale Docker Engine com Docker Compose v2 ou um cluster Kubernetes compatível. Para instalar CLIs de nuvem no host, consulte os guias independentes em [Provedores de Nuvem](./provedores-nuvem/README.md); os scripts de instalação podem alterar o sistema e devem ser revisados antes da execução.
