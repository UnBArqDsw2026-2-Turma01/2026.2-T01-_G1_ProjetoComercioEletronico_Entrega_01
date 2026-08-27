# IA Generativa

Conforme decidido na [reunião de 24/08/2026](/Atas/Subequipe1/ata24_08.md), o relato sobre o uso de IA Generativa é **individual e obrigatório**: cada integrante escreve o seu próprio ponto de vista. Esta página reúne os relatos da Subequipe 01.

---

## Ponto de vista — Pedro Luciano de Azevedo

### Lições aprendidas

O que eu levo desta entrega, em ordem de impacto:

**A engenharia reversa é um método, não um olhar.** Eu entrei nesta entrega achando que "engenharia reversa da interface" significava descrever o que aparece na tela. Só depois de ler Chikofsky e Cross (1990) entendi a diferença entre *engenharia reversa* e *recuperação de projeto*: o que produzo não é uma descrição do sistema, é uma **abstração coerente com o que ele demonstra**, construída com conhecimento de domínio para preencher o que a caixa-preta não expõe. Essa distinção mudou o artefato: passei a marcar explicitamente, no relatório, quais atividades da pool da plataforma foram inferidas e não observadas. O que mais rendeu resultado, na prática, foi a etapa de **provocar exceções** — buscar termo sem resultado, zerar a listagem com filtro, apertar "voltar". Foi ali, e não no percurso feliz, que apareceu o achado central da minha parte: os filtros voltam, a posição de rolagem não.

**O NFR Framework serve para registrar o conflito, não para elogiar a solução.** Minha primeira versão do SIG estava cheia de `++` e sem nenhum `-`. Estava errada, e de um jeito específico: eu tinha modelado as intenções do sistema em vez das consequências das decisões. Quando forcei a pergunta "o que **piora** quando isso melhora?", o grafo passou a dizer algo — `Tempo de Resposta` acabou **fracamente negado (W⁻)** por receber três contribuições negativas e nenhuma positiva, e essa dívida propagou até a raiz, que terminou em W⁻. É exatamente o tipo de custo que uma lista de requisitos esconde. Aprendi que o valor do SIG está na propagação de rótulos, que obriga a assumir o preço, e nos *claims*, que obrigam a justificar por que o preço foi aceito.

**Os três artefatos só funcionam encadeados.** O Mapa Mental me deu o inventário do domínio; o inventário me deu o recorte do fluxo; a engenharia reversa do fluxo me deu as operacionalizações do SIG; e o conflito do SIG voltou como anotação de texto no BPMN. Se eu tivesse produzido os três em paralelo, teria três artefatos bonitos e desconexos. Produzi-los em cadeia foi mais lento e é a razão de haver rastreabilidade ponto a ponto entre eles.

**Notação tem regra, e regra custa tempo.** BPMN não aceita fluxo de sequência atravessando pool — comunicação entre pools é fluxo de mensagem, com seta vazada. NFR Framework distingue nuvem fina (softgoal), nuvem grossa (operacionalização) e nuvem tracejada (claim), e o arco sobre os links significa decomposição AND. Nada disso é decorativo, e boa parte do meu tempo foi conferir a notação contra a fonte, não desenhar.

### Uso da IA Generativa (senso crítico)

Usei IA generativa em três frentes, com resultados bem diferentes:

**Onde ajudou de verdade — organizar e questionar.** A IA foi útil para me ajudar a estruturar o relatório, a transformar as anotações soltas da observação de tela, e — o uso mais produtivo — para funcionar como **contraditor**: pedir que apontasse o que estava frouxo no meu SIG foi o que expôs que eu não tinha modelado nenhuma contribuição negativa. Esse tipo de uso, em que a IA critica um trabalho que já existe, rendeu muito mais do que pedir que ela produzisse o trabalho.

**Onde precisei corrigir o que ela apontou.** As falhas nos apontamentos não foram aleatórias, foram sistemáticas e vale registrá-las:

- **Referências.** Pedi à IA que conferisse as referências que eu já tinha levantado. Vários apontamentos vinham com autor, ano e veículo trocados entre obras próximas do mesmo tema, então precisei checar cada um direto na fonte antes de aceitar qualquer correção sugerida. Não usei nenhuma referência que eu não tenha verificado por conta própria.
- **Achados genéricos.** Pedi à IA que apontasse o que eu poderia estar deixando passar no fluxo de busca. Os pontos que ela levantou foram genéricos — sugestões, filtros, ordenação — e nenhum dos achados que efetivamente valeram a pena veio dali: o comportamento do botão "voltar", o contador por faceta e o cálculo de frete antes do carrinho vieram de eu olhar a tela e provocar o sistema. **A IA aponta o óbvio; não substitui a observação, porque não estava lá.**

**Como isso mudou meu método.** Passei a usá-la principalmente onde o custo do erro é baixo e o ganho é de organização: tabelar, revisar redação, listar o que faltou, atacar meu próprio texto. A conclusão que fica é menos sobre a ferramenta e mais sobre a divisão de trabalho: **a IA acelera quem já sabe verificar, e acelera na direção errada quem não sabe.** Nesta entrega, a parte que exigiu conhecimento — decidir o recorte, provocar as exceções e escolher a decomposição do softgoal.

---

## Referências

CHIKOFSKY, Elliot J.; CROSS II, James H. Reverse engineering and design recovery: a taxonomy. **IEEE Software**, v. 7, n. 1, p. 13–17, jan. 1990.

CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-Functional Requirements in Software Engineering**. Boston: Kluwer Academic Publishers, 2000.

OBJECT MANAGEMENT GROUP. **Business Process Model and Notation (BPMN), Version 2.0**. OMG Document formal/2011-01-03. Needham: OMG, 2011.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 26/08/2026 | Adição do ponto de vista individual sobre lições aprendidas e uso da IA Generativa | Pedro Luciano de Azevedo | -- |
