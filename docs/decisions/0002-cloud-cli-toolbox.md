# ADR-0002: Toolbox de CLIs para provedores de nuvem

## Status

Aceita

## Data

2026-09-24

## Contexto

O repositório `provedor-nuvem-certifications` organiza uma POC de aprendizado e rotinas operacionais multicloud, mas não fornece uma aplicação que possa ser empacotada como serviço. Este componente precisa reunir sete trilhas de CLI e permitir sua execução local em Docker e Kubernetes. Credenciais de nuvem também não devem compor imagens nem manifests versionados.

## Decisão

Entregar uma toolbox interativa com os CLIs AWS, Azure, Google Cloud, Heroku, OCI, OpenShift e Spring Boot, mais documentação independente para cada subcomponente. O container não expõe porta nem cria recursos cloud automaticamente. Docker Compose inicia sessões descartáveis; o manifesto Kubernetes cria um Pod sem Service e sem credenciais.

As instalações são reunidas em um script com seleção por CLI para que os guias possam instalar ferramentas isoladamente. Spring Cloud é documentado como ecossistema para aplicações Spring distribuídas; a ferramenta de terminal é o Spring Boot CLI, pois Spring Cloud não possui um CLI universal de administração.

## Alternativas consideradas

### Criar um serviço de aplicação

Rejeitada porque a origem é material de estudo/scripts e não define servidor, porta, endpoint ou processo de aplicação.

### Criar uma imagem diferente para cada CLI

Adiada. Imagens específicas seriam menores, mas repetiriam artefatos e dificultariam uma sessão de estudo que compara provedores. Os READMEs continuam oferecendo instalação seletiva no host.

### Inserir credenciais na imagem ou no manifesto

Rejeitada porque expõe segredos em camadas, histórico de build ou controle de versão. Credenciais precisam ser providas fora dos artefatos; no Kubernetes, deve-se preferir identidade federada da plataforma.

## Consequências

- A imagem reúne ferramentas de fornecedores diferentes e tende a ser maior e exigir atualizações coordenadas.
- Instaladores upstream acompanham versões atuais e, portanto, uma reconstrução posterior pode trazer versões diferentes; registre a imagem aprovada pelo digest antes de usá-la em automação.
- O home temporário evita persistir estado de autenticação, mas cada sessão requer novo login ou mecanismo externo de identidade.
- O Pod é uma toolbox de desenvolvimento/estudo, não uma carga de aplicação de produção.
