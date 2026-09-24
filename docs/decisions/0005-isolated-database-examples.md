# ADR-0005: Artefatos isolados de execução dos bancos

- Status: Accepted
- Data: 2026-09-24

## Contexto

O catálogo Armazenamentos Gerais reúne bancos distintos que não compartilham os mesmos requisitos de configuração, licença, recursos ou operação. Incluir todos na stack Compose/Kubernetes principal faria os serviços iniciarem juntos e ampliaria o consumo local, além de misturar exemplos de laboratório com a plataforma base.

## Decisão

Cada subcomponente mantém um Compose independente e um Kustomize independente com StatefulSet, Service e armazenamento persistente apropriados ao exemplo. Cada banco é iniciado sob demanda. A base da plataforma permanece com PostgreSQL.

Os manifests representam instâncias únicas para estudo; não prometem HA, backup automatizado, upgrade sem interrupção ou prontidão para produção. Credenciais chegam por ambiente local ignorado pelo Git ou Secret fornecido externamente, sem valores sensíveis nos manifests.

Oracle Database 12c é construído localmente a partir dos Dockerfiles de exemplo Oracle e da mídia de instalação obtida/licenciada pelo usuário; sua imagem não é distribuída pelo repositório.

## Consequências

- Serviços e volumes são iniciados isoladamente e não consomem recursos quando não selecionados.
- Cada diretório documenta suas variáveis, portas, PVC, Secret e comandos de remoção.
- O usuário precisa revisar as limitações de laboratório, o suporte e o licenciamento antes de qualquer uso além de desenvolvimento.
- Imagens locais devem ser carregadas no cluster ou publicadas em registry antes da execução Kubernetes.

## Referências

- [Armazenamentos Gerais](../../general-storage/README.md)
- [ADR-0004: catálogo de bancos](0004-general-storage-catalog.md)
