# Microsoft Azure

Azure é a plataforma de nuvem da Microsoft. O Azure CLI (`az`) permite gerenciar assinaturas, grupos de recursos e serviços e automatizar rotinas operacionais.

## Instalar e conferir

No host Ubuntu/Debian, execute `bash provedores-nuvem/scripts/install-cli.sh azure`. Para outras distribuições, siga o método oficial correspondente. Na toolbox: `az version`.

## Configurar acesso

```bash
az login
az account list --output table
az account set --subscription "<subscription-id>"
az account show --output table
```

Em automação, prefira federação de identidade ou identidade gerenciada. Evite salvar credenciais de service principal em texto puro.

## Comandos de referência

```bash
az group list --output table
az resource list --output table
az webapp list --output table
```

Os exemplos consultam recursos. Verifique a assinatura ativa antes de qualquer comando que crie ou altere recursos.

## Referências

- [Instalar Azure CLI no Linux](https://learn.microsoft.com/cli/azure/install-azure-cli-linux)
- [Referência de comandos Azure CLI](https://learn.microsoft.com/cli/azure/reference-index)
