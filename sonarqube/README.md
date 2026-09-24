# SonarQube

## Objetivo

Avaliar qualidade e segurança do código dos serviços backend e frontend.

## Responsabilidades

- Detectar bugs, vulnerabilidades e problemas de manutenção.
- Aplicar quality gates nos pipelines de CI.
- Acompanhar cobertura e evolução da qualidade por projeto.

## Integrações

Jenkins executa o scanner apropriado para cada linguagem e publica os resultados no SonarQube. Configure tokens como credenciais protegidas e associe um quality gate aos pipelines antes de permitir a promoção de versões.

