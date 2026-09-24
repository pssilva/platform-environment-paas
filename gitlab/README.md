# GitLab

## Objetivo

Centralizar o código-fonte, o controle de versões e a colaboração dos projetos da plataforma.

## Responsabilidades

- Hospedar os repositórios do backend e dos frontends.
- Gerenciar branches, merge requests e permissões.
- Executar pipelines GitLab CI quando esse executor for adotado.
- Integrar commits e merge requests com Jenkins e SonarQube.

## Integrações

Jenkins pode buscar o código e publicar o resultado dos pipelines no GitLab. Os projetos devem manter seus arquivos de pipeline junto ao código e armazenar credenciais em variáveis protegidas, nunca no repositório.

