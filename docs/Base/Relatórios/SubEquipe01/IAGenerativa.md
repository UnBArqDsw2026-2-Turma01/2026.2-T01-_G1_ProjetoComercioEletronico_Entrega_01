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

**Inspecionar é diferente de olhar.** Eu comecei a minha parte da engenharia reversa fazendo o que o enunciado parecia pedir: percorrer as telas e anotar o que aparece. Produzi uma lista correta e inútil — "tem um campo de CEP", "tem um botão Continuar". A lista só virou artefato quando eu abri as Ferramentas de Desenvolvedor e li os **atributos** dos campos. Foi ali que apareceu tudo o que sustenta o meu relatório: o CEP com `maxlength="8"` e sem máscara, o telefone com o mesmo limite de 120 caracteres de um nome de rua, e — o achado que mais me surpreendeu — **nenhum campo do formulário declara `required`**. A obrigatoriedade existe, mas mora só no texto do rótulo, e por negação: o único campo marcado é o opcional. Nada disso é visível a olho nu, e nenhuma dessas coisas eu teria encontrado percorrendo a tela mais dez vezes.

**Um requisito não funcional só vira artefato quando aponta para o que ele custa.** A primeira versão do meu SIG de Segurança tinha seis operacionalizações e nenhuma aresta vermelha. Cada decisão melhorava alguma coisa e não piorava nada — o que é obviamente falso, e o desenho não denunciava a falsidade porque eu tinha modelado *intenções*, não *consequências*. Quando refiz o grafo perguntando "o que piora quando isto melhora?", `Tempo de Resposta` caiu para W⁻ e `Facilidade de Uso` entrou em conflito, e a raiz terminou em W⁺ e não em ✓. O grafo ficou pior de olhar e muito melhor de ler. A lição que eu levo é que o NFR Framework não serve para defender a solução: serve para registrar o preço dela e obrigar alguém a assinar embaixo — que é o papel do *claim*.

**Escolher o recorte é metade do trabalho.** Eu peguei o fluxo de carrinho e endereço porque ele fazia fronteira exata com o recorte que o Pedro já tinha registrado, e porque era onde o método da professora — máscaras, obrigatoriedade, mensagens de erro — podia de fato ser exercido. Só depois percebi o efeito colateral: como ele observou o sistema **deslogado** e eu observei **logado**, os dois registros divergem no mesmo ponto da tela — onde ele viu campo de CEP, eu vi "Enviar para \<endereço salvo\>". Não é contradição, são dois estados condicionados pela autenticação, e isso só ficou visível porque duas pessoas observaram em condições diferentes. Dividir engenharia reversa por pessoa, e não só por tela, produz informação que a divisão por tela não produz.

**Saber onde parar também é resultado.** O meu recorte terminava no pagamento, e eu não percorri o pagamento — avançar exigiria confirmar uma compra real, com cobrança real. Foi frustrante parar exatamente no ponto mais rico do fluxo. O que aprendi é que a resposta certa não era esconder isso: foi marcar cada linha inferida como inferida nas tabelas, e explicar a decisão. Um relatório que apresentasse as duas últimas transições como observadas seria mais completo e menos verdadeiro.

**Notação tem regra, e a regra custa tempo.** No NFR Framework, nuvem fina é softgoal, nuvem grossa é operacionalização, nuvem tracejada é *claim*, o arco sobre as ligações marca decomposição AND, e o *claim* se liga à **ligação** que ele justifica — não ao nó. Cada um desses detalhes eu tive de conferir na fonte, e mais de um estava errado na minha primeira versão.

### Uso da IA Generativa (senso crítico)

Usei IA generativa em toda a entrega e o resultado foi desigual de um jeito que vale registrar com precisão, porque o padrão não é aleatório.

**Onde ela foi genuinamente útil: como leitora, não como autora.** O uso de maior retorno foi pedir que ela **conferisse a entrega contra as Diretrizes da disciplina**, e não que produzisse conteúdo. Foi assim que apareceu um problema que ninguém do grupo tinha visto: as Diretrizes dizem, para todos os oito projetos, "não usar o nome real da fonte de inspiração", e a nossa documentação nomeava a plataforma de referência em vários pontos. É um descumprimento explícito de diretriz que estava lá havia dias, à vista de três pessoas. Uma leitura mecânica de um documento contra outro é exatamente o tipo de tarefa em que a máquina ganha da atenção humana cansada.

O segundo uso produtivo foi **escrever código de diagrama**. Meu Mapa Mental é Mermaid e meu SIG é um SVG gerado por script Python — nos dois casos, a IA acelerou muito a parte mecânica: sintaxe, geometria das nuvens, marcadores de seta. Aqui o ganho é real e o risco é baixo, porque **código de diagrama falha de forma visível**: ou renderiza, ou não.

**Onde ela falhou, e como eu descobri.** Duas falhas concretas:

*Ela não sabia que o diagrama não ia aparecer.* A sugestão de fazer o mapa mental em Mermaid veio acompanhada da afirmação de que ele renderizaria no GitPages. Não renderizava: o `docs/index.html` do grupo rodava Docsify **sem** o plugin do Mermaid, então o bloco de código apareceria como texto cru. Isso só foi descoberto porque eu fui verificar o arquivo — e a correção (habilitar o Mermaid no Docsify) acabou virando uma [iniciativa extra](/Base/1.3.IniciativasExtras.md) que beneficia as três subequipes. A afirmação estava errada e foi feita com a mesma segurança de todas as outras.

*Ela aponta o óbvio quando o assunto é observação.* Pedi que listasse o que eu poderia estar deixando passar no fluxo de checkout. Vieram sugestões corretas e genéricas — "verifique o cálculo do frete", "observe o resumo do pedido". **Nenhum** dos achados que sustentam o meu relatório veio dali: o `maxlength` de oito dígitos, a ausência de `required`, o `inputmode` inconsistente e o comportamento da validação na perda de foco vieram de eu abrir o inspetor e olhar. Isso não é defeito de configuração: **a IA não estava lá**. Ela não pode observar o artefato; só pode falar sobre o gênero de coisa que artefatos desse tipo costumam ter.

**O padrão que eu extraí disso.** A qualidade do que eu recebi dependeu quase inteiramente do **verbo do pedido**. Pedidos de *produzir* ("escreva a análise do checkout") renderam texto plausível e genérico, que eu teria de refazer inteiro. Pedidos de *verificar* ("isto contradiz as diretrizes?", "esta contribuição existe no catálogo do NFR Framework?") renderam os achados mais valiosos da entrega. É uma assimetria útil: a IA é fraca em gerar o conteúdo que depende de eu ter estado presente, e forte em cruzar dois documentos que eu já tenho.

**O que mudou no meu método.** Passei a tratar todo apontamento dela como **pista a conferir na fonte**, nunca como resposta. Rodei o *parser* do Mermaid para confirmar que o mapa mental era sintaticamente válido em vez de aceitar que era; renderizei o SVG do SIG e olhei o resultado antes de commitar; conferi cada rótulo de contribuição contra Chung et al. (2000). E fica um registro incômodo, mas honesto: a IA acertou uma diretriz que três estudantes tinham lido e não viram, e errou ao afirmar que um diagrama renderizaria em uma página que ela não tinha aberto. As duas coisas foram ditas com o mesmo tom de certeza. **O tom não é sinal de nada** — e é isso, mais do que qualquer ganho de produtividade, que eu levo desta entrega.

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
| 1.2 | 27/08/2026 | Adição do ponto de vista individual sobre lições aprendidas e uso da IA Generativa | Patrick Anderson Carvalho dos Santos | -- |
