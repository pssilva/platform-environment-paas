# Python

Esta pasta reúne scripts Python para automações e tarefas auxiliares do
ambiente PaaS. Prefira manter cada ferramenta pequena, documentar seus
argumentos e evitar dependências externas quando a biblioteca padrão for
suficiente.

## Pré-requisitos

- Python 3 instalado e disponível no `PATH` (`python3 --version` para conferir).

## Executar

Na raiz do repositório:

```sh
python3 scripts/src/main/automation/PaaSScriptsUteis/python/hello_world.py
```

O exemplo imprime uma saudação no terminal.

## PaaSScriptsUteis

`paas_scripts_uteis.py` traduz as rotinas do script Bash principal. Na raiz do
repositório, rode `python3 scripts/src/main/automation/PaaSScriptsUteis/python/paas_scripts_uteis.py --help`.
Os comandos disponíveis incluem `create-structure <caminho>`, `process-csv
<arquivo.csv>`, `menu`, as rotinas de instalação e `provider-<provedor>`. As
instalações só executam comandos externos quando chamadas. As rotinas de SDK
dos provedores e `make-all-tools` permanecem não implementadas, como no Bash.
