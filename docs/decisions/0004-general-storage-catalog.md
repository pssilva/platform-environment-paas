# ADR-0004: Catálogo de bancos no componente Armazenamentos Gerais

- Status: Accepted
- Data: 2026-09-24

## Contexto

O repositório já fornece PostgreSQL na stack Compose e nos manifests Kubernetes. A demanda por documentação de vários bancos relacionais e NoSQL não implica que todos devam ser executados juntos em todo ambiente: cada banco tem requisitos de recursos, configuração, operação e licenciamento distintos.

## Decisão

Agrupar a documentação de PostgreSQL, Microsoft SQL Server, MySQL, Oracle Database 12c, MongoDB, Cassandra e Redis em `general-storage/`. Cada banco terá um guia e um wrapper para seu CLI nativo. Os wrappers conectam a servidores previamente provisionados; eles não instalam nem iniciam servidores. O guia PostgreSQL passa a residir em `general-storage/postgresql/README.md`.

A stack padrão continua iniciando PostgreSQL apenas. Servidores adicionais serão adicionados a topologias específicas somente quando houver requisito e configuração apropriados.

## Consequências

- Um índice único apresenta os bancos relacionais e os diferentes modelos NoSQL.
- O PostgreSQL permanece disponível no fluxo Compose/Kubernetes existente.
- Os wrappers requerem que o usuário instale os clientes e forneça a configuração da conexão sem versionar segredos.
- Cada implantação deve avaliar separadamente suporte, segurança, backup, restauração, recursos e termos de uso.

## Referências

- [Documentação da execução da plataforma](../deployment.md)
- [Componente Armazenamentos Gerais](../../general-storage/README.md)
