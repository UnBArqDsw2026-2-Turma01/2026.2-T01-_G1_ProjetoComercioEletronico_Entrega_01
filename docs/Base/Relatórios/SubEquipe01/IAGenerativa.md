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

## Ponto de vista — Patrick Anderson Carvalho dos Santos

### Lições aprendidas

**Inspecionar é diferente de olhar.** Comecei anotando o que aparecia na tela e produzi uma lista correta e pouco útil. O material virou artefato quando abri as Ferramentas de Desenvolvedor e li os atributos dos campos: CEP com `maxlength="8"` e sem máscara, telefone com o mesmo limite de um nome de rua e, principalmente, nenhum campo declarando `required`. A obrigatoriedade existe, mas só no texto do rótulo. Nada disso apareceria percorrendo a tela mais dez vezes.

**Um SIG sem contribuição negativa não diz nada.** Minha primeira versão do grafo tinha seis operacionalizações e nenhuma aresta vermelha: cada decisão melhorava algo e não piorava nada, o que é falso. Refazendo com a pergunta "o que piora quando isto melhora?", `Tempo de Resposta` caiu para W⁻, `Facilidade de Uso` entrou em conflito e a raiz terminou em W⁺. O grafo ficou menos bonito e mais informativo.

**Escolher o recorte é metade do trabalho.** Peguei o carrinho e o checkout porque faziam fronteira com o recorte do Pedro e porque era onde as máscaras e mensagens de erro podiam ser observadas. Depois acrescentei o lado do vendedor, e foi ele que explicou o resto: a plataforma tenta vincular todo anúncio novo a um item de catálogo já existente, e é isso que produz as ofertas concorrentes na ficha do produto e o agrupamento por vendedor no carrinho.

**Saber onde parar também é resultado.** O percurso terminava no pagamento e eu não avancei, porque isso exigiria confirmar uma compra real. Em vez de esconder, marquei cada linha inferida como inferida.

**Notação tem regra.** No NFR Framework, nuvem fina é softgoal, nuvem grossa é operacionalização, tracejada é claim, e o claim se liga à ligação, não ao nó. No BPMN, fluxo de sequência não atravessa pool. Boa parte do tempo foi conferir isso na fonte, não desenhar.

### Uso da IA Generativa

Usei IA em toda a entrega, e o resultado foi desigual de um jeito que vale registrar, porque não é aleatório.

**Onde funcionou: conferir, não produzir.** O uso de maior retorno foi pedir que ela checasse a documentação contra as Diretrizes da disciplina. Foi assim que apareceu um problema que o grupo não tinha visto: as Diretrizes dizem, para todos os projetos, para não usar o nome real da fonte de inspiração, e a nossa documentação a nomeava em vários pontos. Uma leitura mecânica de um documento contra o outro é o tipo de tarefa em que a máquina ganha da atenção humana cansada. Também ajudou bastante na parte mecânica dos diagramas — sintaxe, geometria, alinhamento —, onde o erro é visível: ou renderiza, ou não.

**Onde falhou.** Duas falhas concretas. A primeira: ao sugerir que eu fizesse o mapa mental em Mermaid, afirmou que ele renderizaria no GitPages. Não renderizava — o `index.html` do grupo rodava Docsify sem o plugin. Só descobri porque fui verificar o arquivo. A segunda: pedi que apontasse o que eu poderia estar deixando passar no checkout, e vieram sugestões corretas e genéricas. Nenhum dos achados que sustentam o meu relatório veio dali; todos vieram de abrir o inspetor e olhar. Isso não é defeito de configuração — a IA não estava lá, e não pode observar o artefato.

**O que mudou no meu método.** Passei a tratar cada apontamento como pista a conferir na fonte. Rodei o parser do Mermaid para confirmar que os diagramas eram válidos em vez de supor, renderizei os SVGs e olhei antes de commitar, e conferi cada rótulo de contribuição contra Chung et al. (2000). Fica também um registro incômodo: a IA acertou uma diretriz que três pessoas tinham lido e não viram, e errou ao afirmar algo sobre uma página que não tinha aberto — as duas coisas com o mesmo tom de segurança. É o tipo de detalhe que só se percebe verificando.

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
| 1.2 | 27/08/2026 | Adição do ponto de vista do Patrick sobre lições aprendidas e uso da IA Generativa | Patrick Anderson Carvalho dos Santos | -- |
