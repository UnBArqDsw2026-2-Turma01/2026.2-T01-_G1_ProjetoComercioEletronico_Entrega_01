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

## Ponto de vista — Guilherme Costa Zanella

### Lições aprendidas

**Rich Picture não é diagrama.** Minha primeira tentativa foi pensar nele como um fluxograma informal — caixas, setas, um sistema no centro. Não funcionava, porque o método de Monk e Howard pede o oposto: o usuário no centro, não o sistema, e o que o desenho precisa capturar são tensões e preocupações, não apenas fluxos. Um Rich Picture bem-sucedido tem boneco palito, balão de fala e uma cara de rascunho — se ele parece formal demais, provavelmente errei o gênero.

**Desenhar à mão obriga a decidir o que importa.** Num fluxograma digital, é fácil colocar todos os elementos que existem. No papel, cada elemento custa espaço e tempo, e isso força uma triagem: o que realmente é uma tensão do usuário, e o que é só detalhe de tela que já está registrado em outro artefato. Foi um exercício de síntese antes de ser um exercício de desenho.

**Ata de reunião é rastreabilidade, não formalidade.** No começo eu tratava a ata como obrigação burocrática. Ela virou útil quando passou a registrar não só "o que foi decidido", mas também quem ficou responsável por qual parte — foi a ata do dia 24/08 que documentou a divisão de tarefas que sustenta boa parte da tabela de contribuições da subequipe.

**O SIG não é intuitivo na primeira leitura.** Entender a notação do NFR Framework — a diferença entre softgoal, operacionalização e claim, e por que o claim se liga à ligação e não ao nó — exigiu ir aos slides da professora várias vezes, não só ler uma vez e aplicar. É uma notação com regras específicas, parecida nisso com o BPMN.

### Uso da IA Generativa

Usei IA principalmente em três frentes: entender conceitos que eu não dominava (NFR Framework), estruturar artefatos de coordenação (atas, templates de wiki) e tentar gerar o Rich Picture. O resultado foi bem diferente entre essas frentes.

**Onde funcionou: explicar e estruturar.** Pedir para a IA explicar o NFR Framework do zero, com exemplos, foi mais eficiente do que tentar entender só pelos slides isoladamente — ela servia como um segundo professor para tirar dúvidas pontuais, não como substituto da fonte. Da mesma forma, gerar os templates de markdown da Wiki (estrutura do index, das páginas de subequipe, da página de participações) e formatar a ata a partir da transcrição da reunião foram tarefas mecânicas de estruturação onde a IA economizou bastante tempo sem risco de perder informação.

**Onde falhou: gerar o Rich Picture.** Tentei pedir que a IA gerasse o Rich Picture diretamente como um canvas/SVG. O resultado saiu estruturado demais — mais parecido com um diagrama técnico do que com o desenho informal que o método pede. Fazia sentido em retrospecto: a IA tende a organizar elementos em grade e hierarquia, que é exatamente o oposto do que um Rich Picture precisa comunicar. Tive que abandonar essa abordagem e em vez desenhar à mão.

**O que mudou no meu método.** Passei a usar a IA de dois jeitos diferentes dependendo da tarefa: para artefatos estruturados (atas, templates, explicações de conceito), aceito o resultado como ponto de partida direto. Para artefatos que dependem de julgamento visual ou informalidade — como o Rich Picture —, uso a IA só para me orientar sobre o processo, e faço a execução eu mesmo. Foi um caso claro de a ferramenta certa depender do tipo de saída esperada, não só da tarefa.

---

## Ponto de vista — Patrick Anderson

### Lições aprendidas

**Inspecionar é diferente de olhar.** Comecei anotando o que aparecia na tela e produzi uma lista correta e pouco útil: "tem um campo de CEP", "tem um botão Continuar". O material só virou artefato quando abri as Ferramentas de Desenvolvedor e li os atributos dos campos. Foi ali que apareceu o que sustenta o meu recorte: CEP com `maxlength="8"` e sem máscara, telefone com o mesmo limite de caracteres de um nome de rua e, principalmente, **nenhum campo declarando `required`**. A obrigatoriedade existe, mas mora só no texto do rótulo, e por negação — o único campo marcado é o opcional. Nada disso apareceria percorrendo a tela mais dez vezes.

**Um SIG sem contribuição negativa não informa nada.** A primeira versão do meu galho só tinha `+` e `++`: cada decisão melhorava algo e não piorava nada, o que é obviamente falso. O grafo só passou a dizer alguma coisa quando forcei a pergunta inversa — o que piora quando isto melhora? Aí `Reversibilidade` recebeu o `−−` da rolagem infinita e o galho terminou em W⁻. Ficou menos bonito e muito mais informativo.

**Saber onde parar também é resultado.** Meu recorte terminava no pagamento, e eu não percorri o pagamento, porque isso exigiria confirmar uma compra real. Foi frustrante parar no ponto mais rico do fluxo. O que aprendi é que a resposta certa não era esconder: foi marcar cada linha inferida como inferida nas tabelas e explicar a decisão. Um relatório que apresentasse as últimas transições como observadas seria mais completo e menos verdadeiro.

**Olhar o outro lado explicou o lado que eu já tinha olhado.** Levantei também o fluxo do vendedor, que a entrega não exigia. Foi ele que deu causa a dois achados que, do lado do comprador, apareciam soltos: a plataforma tenta vincular todo anúncio novo a um item de catálogo já existente, e é esse vínculo que produz as ofertas concorrentes na ficha do produto e o agrupamento por vendedor no carrinho. O que parecia decisão de layout do carrinho é consequência de uma decisão tomada lá no cadastro do anúncio.

**Notação tem regra, e conferir a regra custa tempo.** No NFR Framework, o claim se liga à ligação e não ao nó. No BPMN, fluxo de sequência não atravessa pool. Boa parte do trabalho foi conferir esses detalhes na fonte, não desenhar.

### Uso da IA Generativa (senso crítico)

Usei IA generativa na maior parte da minha entrega, e o resultado foi desigual de um jeito que vale registrar, porque o padrão não é aleatório.

**Onde funcionou: conferir, não produzir.** O uso de maior retorno foi pedir que ela checasse a documentação contra as Diretrizes da disciplina. Foi assim que apareceu um problema que ninguém do grupo tinha visto: as Diretrizes determinam, para todos os projetos, não usar o nome real da fonte de inspiração, e a nossa documentação a nomeava em vários pontos. É o tipo de tarefa em que a leitura mecânica de um documento contra o outro ganha da atenção humana cansada. O mesmo valeu para verificação de consistência interna — foi conferindo referência por referência que apareceu que a página do SIG citava identificadores de requisito que tinham deixado de existir quando a engenharia reversa mudou de numeração.

**Onde falhou.** Duas falhas concretas. A primeira: ao sugerir uma ferramenta de diagramação, afirmou que o resultado renderizaria no GitPages do grupo. Não renderizava — a página não tinha o plugin necessário. Só descobri porque fui verificar o arquivo, e não porque ela sinalizou incerteza. A segunda: pedi que apontasse o que eu poderia estar deixando passar no fluxo de checkout, e vieram sugestões corretas e genéricas. **Nenhum** dos achados que sustentam o meu recorte veio dali; todos vieram de abrir o inspetor e olhar. Isso não é defeito de configuração — a IA não estava lá, e não pode observar o artefato.

**O que mudou no meu método.** Passei a tratar cada apontamento como pista a conferir na fonte, e não como resposta. Renderizei os diagramas e olhei o resultado antes de publicar, e conferi cada rótulo de contribuição do SIG contra Chung et al. (2000). Fica também um registro incômodo: a IA acertou uma diretriz que três pessoas tinham lido e não viram, e errou ao afirmar algo sobre uma página que não tinha aberto — as duas coisas com exatamente o mesmo tom de segurança. É esse detalhe, mais do que qualquer ganho de produtividade, que eu levo desta entrega.

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
| 1.2 | 27/08/2026 | Adição do ponto de vista individual sobre lições aprendidas e uso da IA Generativa | Guilherme Costa Zanella | -- |
| 1.3 | 27/08/2026 | Adição do ponto de vista individual sobre lições aprendidas e uso da IA Generativa | Patrick Anderson | -- |
