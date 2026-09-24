# ADR-0003: Instrumentação Dynatrace para Docker e Kubernetes

## Status

Aceita

## Data

2026-09-24

## Contexto

O projeto precisa documentar como acompanhar saúde de microsserviços e relacionar mudanças de CI/CD com alterações de desempenho após deploy. Dynatrace é uma plataforma externa: a coleta exige integração de agente e acesso a uma conta/ambiente Dynatrace. O repositório não deve armazenar tokens nem tentar iniciar integrações automaticamente na stack local padrão.

## Decisão

Para Docker em host Linux, fornecer um Compose que executa a imagem oficial OneAgent segundo o modelo de container suportado pela Dynatrace. Para Kubernetes, documentar a instalação do Dynatrace Operator via Helm e fornecer um `DynaKube` configurado para application monitoring e Kubernetes monitoring. Para associar deploys à telemetria, fornecer um script que envia evento SDLC ao endpoint de ingestão da Dynatrace.

As imagens pertencem ao fornecedor; não há Dockerfile personalizado. Os manifests deixam tokens fora do repositório e exigem que o usuário configure conta, permissões, versões e ambiente antes da implantação.

## Alternativas consideradas

### ActiveGate standalone como workload principal

Rejeitada porque ActiveGate roteia ou coleta dados de tecnologias por APIs, enquanto OneAgent/Operator é necessário para instrumentar serviços e obter visibilidade de aplicação.

### Incluir Dynatrace na stack Compose/Kubernetes padrão

Rejeitada porque exige conta externa, tokens, permissões no host/cluster e pode aplicar instrumentação ampla. A ativação deve ser deliberada pelo operador.

## Consequências

- O OneAgent Docker precisa de Linux, modo PID/network do host, mount do filesystem raiz e capacidades específicas; o operador do host Docker pode inspecionar essas permissões antes de iniciar o Compose.
- O Dynatrace Operator instala CRDs e recursos de cluster e precisa de privilégios administrativos no cluster.
- Os exemplos não criam uma conta Dynatrace, não geram tokens e não aplicam configuração na plataforma externa.
- O uso de eventos SDLC e Site Reliability Guardian depende de recursos/permissões habilitados no ambiente Dynatrace.
