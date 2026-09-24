# Oracle Cloud Infrastructure (OCI)

OCI oferece serviços de computação, rede, armazenamento, banco de dados e aplicações. O OCI CLI (`oci`) é a interface de terminal para consultar e operar serviços da Oracle Cloud.

## Instalar e conferir

No host Linux, execute `bash provedores-nuvem/scripts/install-cli.sh oci`; o instalador oficial configura o CLI para o usuário atual. Na toolbox: `oci --version`.

## Configurar acesso

```bash
oci setup config
oci iam region list
oci iam compartment list --compartment-id <tenancy-ocid>
```

`oci setup config` orienta a criação do perfil e das chaves de API. Proteja a chave privada e restrinja as políticas IAM ao mínimo necessário. A toolbox Kubernetes não configura automaticamente autenticação OCI.

## Comandos de referência

```bash
oci iam region list
oci iam availability-domain list --compartment-id <tenancy-ocid>
oci os bucket list --compartment-id <compartment-ocid>
```

## Referências

- [Quickstart e instalação do OCI CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm)
- [Referência do OCI CLI](https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/)
