# Shell (Bash)

Esta pasta concentra os scripts Shell (Bash) usados nas automações do ambiente
PaaS. O arquivo `PaaSScriptsUteis_main.sh` reúne funções de apoio à instalação
de ferramentas, configuração de SDKs e criação de estruturas de projeto. A
pasta `templates/` guarda modelos usados por esses scripts.

## Pré-requisitos

- Bash 4 ou superior (`bash --version` para conferir).
- As dependências adicionais variam conforme a função executada. Algumas
  funções de instalação usam `sudo`, `dnf`, `curl` ou ferramentas como SDKMAN.

## Executar

O exemplo inicial é independente das rotinas de instalação:

```sh
bash scripts/src/main/automation/PaaSScriptsUteis/shell/hello_world.sh
```

Para ver a ajuda do script principal:

```sh
bash scripts/src/main/automation/PaaSScriptsUteis/shell/PaaSScriptsUteis_main.sh --help
```

