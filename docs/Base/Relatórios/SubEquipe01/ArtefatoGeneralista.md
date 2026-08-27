# Artefato Generalista

Conforme decidido na [reunião de 24/08/2026](/Atas/subEquipe1/ata24_08.md), cada integrante da Subequipe 01 produz o **seu próprio** artefato generalista, escolhendo entre Rich Picture e Mapa Mental, e justificando a escolha. Esta página reúne os artefatos individuais.

---

## Mapa Mental — Pedro Luciano de Azevedo

### O que é o artefato

O **Mapa Mental** é uma técnica de representação gráfica radial na qual um conceito central é progressivamente refinado em ramos hierárquicos, com uso deliberado de palavras-chave curtas, cor e posição espacial para apoiar a memória e a associação de ideias (BUZAN; BUZAN, 1993). Diferentemente de um diagrama de fluxo, o mapa mental **não representa ordem temporal nem decisão**: ele representa _composição_ — o que existe no domínio e como cada elemento se subordina a um agrupamento maior.

Na engenharia de software, esse tipo de representação se enquadra no que a literatura chama de artefato de **elicitação e organização de escopo**: um modelo informal, de baixo custo de produção e alta densidade de comunicação, cuja função é dar à equipe uma visão compartilhada do território antes de qualquer modelagem formal.

### O artefato

[![Mapa Mental do Mercado Livre](../../../assets/SubEquipe01/MapaMental_PedroLuciano.png)](../../../assets/SubEquipe01/MapaMental_PedroLuciano.png ":ignore")

<sub>_Clique no diagrama para abri-lo em tamanho real._</sub>

> _Figura 1 — Mapa Mental do Mercado Livre, usado como base de inspiração para o projeto ([Projeto](/Projeto/Projeto.md)). Nó central: o sistema em estudo. Ramos de 1º nível: domínios funcionais (Descoberta do Produto, Decisão de Compra, Transação & Pagamento, Pós-venda), o contexto de atores, o subsistema de conta e acesso, e o ramo de qualidades (RNFs). Folhas: elementos efetivamente observados na interface durante a engenharia reversa._

### Por que escolhi Mapa Mental (e não Rich Picture)

A escolha não foi por preferência estética, mas pelo **papel que o artefato precisava cumprir dentro desta entrega**. Três razões:

**1. O artefato precisava cobrir o sistema inteiro, não uma situação.**
O Rich Picture, na tradição da _Soft Systems Methodology_ de Checkland (CHECKLAND, 1981; MONK; HOWARD, 1998), é forte exatamente onde o problema é _mal estruturado_: ele captura atores, preocupações, conflitos e o contexto de trabalho ao redor de uma situação. Seu poder está em mostrar tensão e ponto de vista. Só que o que a Subequipe 01 precisava neste momento era o oposto: um **inventário estruturado e navegável de todo o domínio**, para depois recortar dele o requisito não funcional do SIG e o fluxo do BPMN. Para inventariar composição, a hierarquia do mapa mental é mais direta do que a cena do Rich Picture.

**2. Precisava de rastreabilidade explícita para os outros dois artefatos.**
O ramo _Qualidades (RNFs)_ do mapa aponta diretamente para o SIG de Usabilidade planejado, e o ramo _Descoberta do Produto_ enumera exatamente os elementos (busca, autocompletar, filtros facetados, ordenação, breadcrumb) que devem reaparecer como **operacionalizações** no SIG e como **atividades** no BPMN quando esses artefatos forem construidos. A estrutura em ramos permite marcar esses elos ponto a ponto; em um Rich Picture, essa correspondência ficaria diluída na composição pictórica.

**3. Complementaridade dentro do grupo G1.**
A Subequipe 03 já produziu um Rich Picture da perspectiva do comprador. Fazer outro Rich Picture geraria redundância entre subequipes. Adotando o Mapa Mental, o grupo passa a ter as duas leituras — a situacional (Subequipe 03) e a composicional (esta) — sobre o mesmo domínio, o que é mais informativo do que duas versões da mesma técnica.

### Senso crítico sobre o artefato

O mapa mental tem limitações que reconheço e que motivaram os artefatos seguintes:

- **Não expressa ordem nem condição.** O mapa diz que "Filtros facetados" e "Ordenação" existem, mas não diz que o comprador só ordena _depois_ de filtrar, nem o que acontece quando a busca não retorna resultados. Essa lacuna é precisamente o que o BPMN preenche.
- **Não expressa conflito.** No mapa, "Usabilidade" e "Desempenho" são dois nós irmãos, aparentemente independentes. Na prática, filtros facetados com contadores ajudam a usabilidade e **prejudicam** o tempo de resposta. Representar esse trade-off exige a notação do NFR Framework — e é por isso que o ramo de qualidades é um _ponteiro_, não uma resposta.
- **A hierarquia impõe uma classificação que nem sempre é única.** "Frete e prazo por CEP" foi colocado sob _Decisão de Compra_, mas poderia estar sob _Transação_. Escolhi manter sob Decisão porque, na interface observada, o frete é exibido **antes** do carrinho, e é essa antecipação que sustenta o softgoal _Prevenção de Erros_ no SIG. A classificação, portanto, carrega uma decisão de projeto — o que é uma virtude do artefato, desde que documentada.

> **Nota de escopo:** o ramo _Qualidades (RNFs)_ e o ramo _Descoberta do Produto_ deste mapa são o ponto de partida planejado para o SIG de Usabilidade e para a modelagem BPMN, respectivamente — ambos ainda em elaboração. A tabela de elos ponto a ponto entre os três artefatos será adicionada aqui quando os três estiverem publicados.

---

## Rich Picture — Guilherme Costa Zanella

### O que é o artefato

O **Rich Picture** é um artefato informal, desenhado à mão, originado na _Soft Systems Methodology_ de Checkland (1981) e sistematizado como ferramenta de projeto por Monk e Howard (1998). Sua função é reunir em uma única folha os dados sobre uma situação complexa e mal estruturada, retratando os principais _stakeholders_, suas inter-relações e suas **preocupações** (_concerns_).

Para Monk e Howard, _concerns_ são os objetivos de alto nível que restringem significativamente o modo como o trabalho é feito — e sistemas efetivos só podem ser projetados considerando os _concerns_ divergentes dos envolvidos.

### O artefato

[![Rich Picture do fluxo de compra](../../../assets/SubEquipe01/rich-picture-Guilherme.jpg)](../../../assets/SubEquipe01/rich-picture-Guilherme.jpg ":ignore")

<sub>_Clique na imagem para abri-la em tamanho real._</sub>

> _Figura 2 — Rich Picture do fluxo de compra da Jenny no G1_ProjetoComercioEletronico. Contorno laranja: vendedores. Contorno azul: fronteira do sistema. Nuvens: preocupações. Espadas cruzadas: tensão. Fonte: Autor, 2026._

O nome fictício **Jenny** referencia o exemplo conduzido por Monk e Howard na Figura 3 do artigo. A compradora foi posicionada ao centro seguindo a orientação dos autores: começar o desenho pela figura do usuário principal evita a tendência de assumir uma visão orientada ao sistema.

### Por que Rich Picture (e não Mapa Mental)

O Mapa Mental produzido nesta subequipe entrega um inventário do domínio e reconhece, em seu próprio senso crítico, que **não expressa conflito**. O Rich Picture ataca essa lacuna: ele registra pontos de vista divergentes e tensões.

### Leitura pelo modelo de Monk e Howard

Os autores Monk e Howard estabelecem que os três componentes mais importantes de um Rich Picture são **estrutura, processo e _concerns_**.

#### Estrutura

Aspectos que mudam lentamente, incluindo todas as pessoas que usarão ou poderão ser afetadas pelo sistema.

Registrados: Jenny (compradora), loja oficial, vendedor autônomo, atendimento, transportadora, operadora de pagamento, catálogo de produtos, e as duas fronteiras (vendedores e plataforma).

#### Processo

As transformações que ocorrem no processo do trabalho. Três fluxos foram registrados:

1. **Compra** — vendedores anunciam, plataforma expõe, Jenny paga, plataforma retém comissão e repassa ao vendedor
2. **Produto** — do vendedor à transportadora, e da transportadora até Jenny
3. **Reclamação** — Jenny reclama, atendimento media com o vendedor, e retorna com resposta ou reembolso

#### Preocupações/Concerns

Capturam as motivações particulares de um usuário ao usar o sistema, caricaturado em balões de pensamento:

| Stakeholder       | Preocupações/Concerns                             |
| ----------------- | ------------------------------------------------- |
| Jenny             | "o produto é confiável? quando chega?"            |
| Loja oficial      | "eu pago mais, então apareço mais"                |
| Vendedor autônomo | "por que meu anúncio nunca aparece na 1ª página?" |
| Atendimento       | "quem tem razão?"                                 |

#### Tensões

A tensão registrada opõe **loja oficial e vendedor autônomo**, que competem pela mesma vitrine sob regras que favorecem quem investe em anúncio.

### Senso crítico

- **A subequipe não aparece no desenho.** Monk e Howard recomendam incluir os analistas na estrutura, para lembrar que também têm ponto de vista e possível viés. Lacuna reconhecida.
- **Apenas uma tensão foi grafada.** Outras tensões poderiam ter sido registradas como por exemplo atendimento x vendedor x jenny (cliente) e operadora de pagamento (comissão) x vendedor (lucro)
- **O artefato não expressa ordem nem condição.** O fluxo de reclamação mostra que há mediação e dois desfechos possíveis, mas não sob quais condições. Limitação intrínseca do rich Picture isso pode ser melhor explorado no BPMN
- **O desenho revelou algo não previsto.** Jenny não tem ligação direta com os vendedores: produto, dinheiro, informação e reclamação passam todos pela plataforma. Essa centralidade emergiu ao ligar os fluxos.

---

## Referências

BUZAN, Tony; BUZAN, Barry. **The Mind Map Book**. London: BBC Books, 1993.

CHECKLAND, Peter. **Systems Thinking, Systems Practice**. Chichester: John Wiley & Sons, 1981.

MONK, Andrew; HOWARD, Steve. The Rich Picture: A Tool for Reasoning About Work Context. **Interactions**, v. 5, n. 2, p. 21–30, mar./abr. 1998.

---

## Histórico de Versões

| Versão | Data       | Descrição                                           | Autor(es)                  | Revisor(es)          |
| ------ | ---------- | --------------------------------------------------- | -------------------------- | -------------------- |
| 1.0    | 24/08/2026 | Estruturação inicial                                | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1    | 26/08/2026 | Adição do Mapa Mental e da justificativa da escolha | Pedro Luciano de Azevedo   | --                   |
| 1.2    | 26/08/2026 | Adição do Rich Picture e dos textos explicativos    | Guilherme Costa Zanella    | --                   |
