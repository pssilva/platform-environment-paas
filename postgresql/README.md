# PostgreSQL

## Objetivo

Disponibilizar persistência relacional para aplicações que precisem armazenar dados estruturados.

## Diretrizes

- Usar banco e credenciais próprios por aplicação ou ambiente.
- Versionar migrações junto ao código da aplicação.
- Manter backups, retenção e procedimento de restauração documentados.
- Não incluir senhas ou dados sensíveis em arquivos versionados.

## Integração

O backend RESTful pode conectar-se ao PostgreSQL por configuração externa (host, porta, banco, usuário e segredo), com conexões TLS e permissões mínimas. Métricas e logs do banco podem ser integrados à observabilidade.

