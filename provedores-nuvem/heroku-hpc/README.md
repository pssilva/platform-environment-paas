# Heroku Platform Cloud (HPC)

Heroku é uma plataforma PaaS para compilar, publicar e operar aplicações. O Heroku CLI (`heroku`) dá acesso a apps, pipelines, logs e configuração pelo terminal.

## Instalar e conferir

No host Linux Ubuntu/Debian, execute `bash provedores-nuvem/scripts/install-cli.sh heroku`. O instalador oficial standalone requer permissão para instalar em `/usr/local`. Na toolbox: `heroku --version`.

## Configurar acesso

```bash
heroku login
heroku auth:whoami
heroku apps
```

O login pode abrir o navegador. Para automação, use token de acesso protegido pelo mecanismo de secrets do CI, nunca um token versionado.

## Comandos de referência

```bash
heroku apps
heroku pipelines
heroku logs --app <app-name> --tail
heroku releases --app <app-name>
```

## Referências

- [Instalar e usar Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [Comandos do Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli-commands)
