# Google Cloud Platform (GCP)

Google Cloud Platform oferece serviços de infraestrutura, dados e aplicações. O Google Cloud CLI, principalmente o comando `gcloud`, configura contextos de projeto e automatiza operações sobre recursos.

## Instalar e conferir

No host Ubuntu/Debian, execute `bash provedores-nuvem/scripts/install-cli.sh gcp`. Na toolbox: `gcloud version`.

## Configurar acesso

```bash
gcloud init
gcloud auth list
gcloud config set project <project-id>
gcloud config list
```

Para CI/CD, prefira Workload Identity Federation em vez de chaves permanentes de service account.

## Comandos de referência

```bash
gcloud projects list
gcloud services list --enabled
gcloud compute instances list
```

Esses exemplos consultam recursos do projeto configurado. Confira o projeto e as permissões antes de executar comandos que alteram a conta.

## Referências

- [Instalar o Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- [Referência do gcloud](https://cloud.google.com/sdk/gcloud/reference)
