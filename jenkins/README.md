# Jenkins

## Objetivo

Automatizar integração contínua e entrega dos serviços da plataforma por meio de pipelines.

## Responsabilidades

- Buscar código nos repositórios GitLab.
- Executar build, verificações e testes automatizados.
- Enviar análise estática ao SonarQube.
- Empacotar e publicar artefatos ou imagens de contêiner.

## Integrações

Os pipelines devem ser versionados como `Jenkinsfile` nos repositórios. Credenciais e tokens devem ser mantidos no gerenciador de credenciais do Jenkins. Definir agentes de build isolados e restringir permissões por projeto.

