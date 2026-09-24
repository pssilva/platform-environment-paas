# Red Hat OpenShift

OpenShift é uma plataforma de aplicações baseada em Kubernetes, com recursos de desenvolvimento, operação e segurança integrados. O CLI `oc` administra projetos e workloads; também inclui os comandos Kubernetes usuais disponíveis em `kubectl`.

## Instalar e conferir

No host Ubuntu/Debian, execute `bash provedores-nuvem/scripts/install-cli.sh openshift`. A rotina baixa a versão estável publicada pela Red Hat para x86-64 ou ARM64. Para compatibilidade previsível, baixe a versão indicada pelo cluster na página oficial de downloads. Na toolbox: `oc version --client`.

## Conectar a um cluster

Obtenha a URL e o token de acesso no console do cluster:

```bash
oc login https://api.<cluster>.<dominio>:6443 --token='<token>'
oc whoami
oc project
oc get projects
```

Não grave tokens em arquivos versionados ou argumentos persistentes do shell. O acesso ao cluster deve ser concedido pelo administrador com RBAC apropriado.

## Comandos de referência

```bash
oc get pods --all-namespaces
oc get deployments -n <projeto>
oc logs deployment/<deployment> -n <projeto>
oc rollout status deployment/<deployment> -n <projeto>
```

## Referências

- [Instalar o OpenShift CLI (`oc`)](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)
- [Referência de comandos `oc`](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/openshift-cli-commands.html)
