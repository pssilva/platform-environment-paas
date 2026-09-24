# AWS

Amazon Web Services (AWS) oferece serviços de computação, armazenamento, rede e serviços gerenciados. A AWS CLI v2 permite consultar e operar esses recursos por terminal e automatizar rotinas de CI/CD.

## Instalar e conferir

No host, use `bash provedores-nuvem/scripts/install-cli.sh aws`. O script baixa o instalador oficial para x86-64 ou ARM64 e usa `sudo` quando não executado como root. Na toolbox: `aws --version`.

## Configurar acesso

```bash
aws configure sso
aws sso login --profile desenvolvimento
aws sts get-caller-identity --profile desenvolvimento
```

Use IAM Identity Center ou credenciais temporárias quando disponíveis. Não inclua chaves em scripts, imagens ou repositório.

## Comandos de referência

```bash
aws configure list-profiles
aws sts get-caller-identity --profile desenvolvimento
aws s3 ls --profile desenvolvimento
aws cloudformation list-stacks --profile desenvolvimento --region us-east-1
```

O último comando é somente leitura. Antes de criar ou remover recursos, confirme conta, região, perfil e custo.

## Referências

- [Instalar AWS CLI v2 no Linux](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
