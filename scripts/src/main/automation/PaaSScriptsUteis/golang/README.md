# Go (Golang)

Esta pasta reúne scripts e pequenos utilitários escritos em Go para automações
relacionadas ao ambiente PaaS. Cada programa deve ter seu próprio arquivo ou
subdiretório, com uma descrição de suas entradas e de como executá-lo.

## Pré-requisitos

- Go instalado e disponível no `PATH` (`go version` para conferir).

## Executar

Na raiz do repositório, execute o exemplo inicial:

```sh
go run ./scripts/src/main/automation/PaaSScriptsUteis/golang/hello_world.go
```

O exemplo imprime uma saudação no terminal. Para compilar um programa:

```sh
go build ./scripts/src/main/automation/PaaSScriptsUteis/golang/hello_world.go
```

## PaaSScriptsUteis

`paas_scripts_uteis.go` traduz as rotinas do script Bash principal. Na raiz do
repositório, rode `go run ./scripts/src/main/automation/PaaSScriptsUteis/golang/paas_scripts_uteis.go --help`.
Os comandos disponíveis incluem `create-structure <caminho>`, `process-csv
<arquivo.csv>`, `menu`, as rotinas de instalação e `provider-<provedor>`. As
instalações só executam comandos externos quando chamadas. As rotinas de SDK
dos provedores e `make-all-tools` permanecem não implementadas, como no Bash.
