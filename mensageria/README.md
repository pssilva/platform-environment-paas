# Mensageria

Componente de referência para brokers e plataformas de mensageria. Mensageria permite que serviços troquem eventos e comandos de forma assíncrona, reduzindo dependências temporais entre produtores e consumidores. Cada subcomponente possui um Compose e manifests Kubernetes para laboratório; execute somente o broker escolhido.

Os exemplos são instalações de nó único, sem alta disponibilidade, autenticação forte, TLS, replicação ou dimensionamento para produção. Configure credenciais locais em `.env` (não versionado) e crie Secrets no Kubernetes por um fluxo seguro. Não publique portas de gerenciamento em redes compartilhadas.

## Subcomponentes

| Tecnologia | Modelo | Guia |
|---|---|---|
| Apache Kafka | Log distribuído de eventos, particionado e retido por período/tamanho | [kafka/README.md](./kafka/README.md) |
| RabbitMQ | Broker de filas e roteamento AMQP, com exchanges, bindings e acknowledgements | [rabbitmq/README.md](./rabbitmq/README.md) |
| Apache ActiveMQ Artemis | Broker multiprotocolo com filas e tópicos, incluindo AMQP, MQTT e OpenWire | [activemq-artemis/README.md](./activemq-artemis/README.md) |

O item ActiveMQ usa Artemis, a implementação de broker multiprotocolo do ecossistema Apache. ActiveMQ Classic é um projeto relacionado, com imagem e ciclo de release próprios; escolha Classic quando depender especificamente de compatibilidade com instalações existentes dele.

## Escolha rápida

Use Kafka para fluxos de eventos duráveis, alto volume, replay e múltiplos consumidores independentes. RabbitMQ atende filas de trabalho e roteamento flexível com confirmação de entrega. Artemis é uma opção quando a interoperabilidade entre protocolos ou compatibilidade com clientes JMS/OpenWire importa. A escolha deve considerar semântica de entrega, ordenação, retenção, throughput, latência, operação e suporte das bibliotecas usadas pelos serviços.

## Execução

Entre no diretório da tecnologia escolhida. Cada guia informa as portas, credenciais e comandos de inicialização. As imagens são fixadas em versões nos manifestos; revise notas de versão e requisitos antes de atualizar. O Compose raiz e a base Kubernetes da plataforma não iniciam esses brokers automaticamente.

No Kubernetes, os recursos usam o namespace `mensageria` e PVCs que dependem de uma StorageClass padrão. Esses manifests não substituem um operador, configuração de cluster, estratégia de backup ou práticas de produção. Para laboratórios, use apenas uma réplica e dados sem valor.
