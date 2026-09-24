# IA-LCD e SDD assistido por IA

## Objetivo

Este componente descreve como usar inteligência artificial ao longo do ciclo de vida de desenvolvimento de software (IA-LCD) e como aplicar o desenvolvimento orientado a especificações (Specification-Driven Development, SDD) com assistência de IA. A IA apoia o trabalho da equipe; decisões, validação e responsabilidade pela entrega continuam sendo humanas.

## Conceitos

- **IA-LCD**: uso deliberado de ferramentas de IA em atividades das diferentes etapas do ciclo de vida do software, como descoberta, análise, desenho, implementação, testes, documentação e manutenção.
- **SDD assistido por IA**: abordagem em que requisitos explícitos são elaborados e revisados antes da implementação. A especificação serve como referência compartilhada para pessoas e ferramentas de IA e é atualizada quando os requisitos mudam.

SDD não significa aceitar automaticamente o conteúdo produzido por uma IA. A equipe define o problema, confirma os requisitos, escolhe as soluções e revisa os resultados.

## Fluxo de trabalho

1. **Entender o problema** — registrar objetivo, usuários, contexto, restrições e critérios de sucesso. Usar IA para explorar perguntas em aberto e resumir informações fornecidas, conferindo as conclusões com as fontes originais.
2. **Especificar** — escrever requisitos observáveis, regras de negócio, casos de uso, critérios de aceitação e requisitos não funcionais relevantes. Identificar explicitamente dúvidas e premissas.
3. **Revisar e aprovar a especificação** — verificar escopo, consistência, testabilidade, segurança, privacidade e acessibilidade conforme o domínio. Obter concordância das pessoas responsáveis antes de tratar a especificação como base de implementação.
4. **Planejar a solução** — decompor o trabalho em módulos e entregas pequenas. Registrar decisões arquiteturais importantes, interfaces, dependências e riscos; consultar documentação oficial quando a implementação depender de bibliotecas ou serviços.
5. **Implementar com assistência** — fornecer à IA apenas o contexto necessário, incluindo os requisitos relevantes e convenções do repositório. Trabalhar em mudanças revisáveis e manter o código alinhado à especificação.
6. **Verificar** — relacionar critérios de aceitação a testes e outras evidências. Executar as verificações apropriadas, revisar as alterações e corrigir divergências antes de integrar.
7. **Documentar e manter** — atualizar especificações, instruções de uso e decisões quando o comportamento mudar. Usar IA para apoiar análise de impacto e investigação, validando as respostas no código, nos dados e nas fontes confiáveis.

## Artefatos úteis

Conforme o tamanho e o risco da mudança, o trabalho pode incluir:

- problema, objetivos e limites de escopo;
- requisitos funcionais e não funcionais;
- critérios de aceitação e exemplos de comportamento;
- mapa de módulos, contratos e dependências;
- plano de implementação e estratégia de verificação;
- decisões arquiteturais (ADRs), quando houver escolhas significativas;
- resultados das verificações e documentação atualizada.

Nem toda alteração precisa de um documento separado para cada item. O importante é que requisitos e critérios relevantes sejam claros, rastreáveis e proporcionais ao risco.

## Uso responsável de IA

- Não envie credenciais, segredos, dados pessoais ou código confidencial a ferramentas sem autorização e controles adequados.
- Trate respostas, código, testes e referências gerados por IA como sugestões a verificar; confirme fatos em fontes confiáveis e valide o comportamento no ambiente do projeto.
- Revise segurança, licenças, qualidade, acessibilidade e compatibilidade antes de incorporar conteúdo gerado.
- Não considere texto produzido, testes gerados ou uma execução bem-sucedida como prova suficiente de que os requisitos foram atendidos.
- Registre decisões e limitações importantes de forma que outra pessoa consiga entender e manter a solução.

## Aplicação neste repositório

O projeto declara ter sido desenvolvido com IA-LCD e SDD. Para mudanças futuras, este fluxo ajuda a manter o vínculo entre intenção, especificação, implementação e verificação. A documentação de implantação está em [Execução da plataforma](../docs/deployment.md), e decisões arquiteturais são registradas em [docs/decisions](../docs/decisions/).
