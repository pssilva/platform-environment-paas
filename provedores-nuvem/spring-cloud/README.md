# Spring Cloud

Spring Cloud é um conjunto de bibliotecas e projetos para padrões comuns de aplicações distribuídas construídas com Spring Boot, incluindo configuração externa, descoberta de serviços, roteamento e tolerância a falhas. É um ecossistema de desenvolvimento, não uma nuvem pública nem uma plataforma de hospedagem.

## Ferramentas e instalação

Não existe um CLI único de administração do Spring Cloud. Esta toolbox disponibiliza Java 21 e instala o Spring Boot CLI (`spring`) usando SDKMAN!, além de Git. Para os projetos, use também o wrapper do Maven (`./mvnw`) ou do Gradle (`./gradlew`) incluído no repositório da aplicação.

No host, execute `bash provedores-nuvem/scripts/install-cli.sh spring-cloud`. Na toolbox, confira `java --version`, `spring --version` e `git --version`.

## Exemplos

```bash
spring init --build=maven --java-version=21 --dependencies=web,actuator exemplo-spring
cd exemplo-spring
./mvnw spring-boot:run
```

Spring Cloud é normalmente adicionado à aplicação pela BOM compatível com sua versão do Spring Boot e pelos starters Maven/Gradle. Consulte a matriz de compatibilidade antes de atualizar versões.

## Referências

- [Spring Boot CLI: instalação e uso](https://docs.spring.io/spring-boot/cli/installation.html)
- [Documentação Spring Cloud](https://spring.io/projects/spring-cloud)
- [Compatibilidade entre Spring Cloud e Spring Boot](https://spring.io/projects/spring-cloud#overview)
