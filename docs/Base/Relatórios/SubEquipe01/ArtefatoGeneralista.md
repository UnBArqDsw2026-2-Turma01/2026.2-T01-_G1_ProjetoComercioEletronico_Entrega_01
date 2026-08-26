# Artefato Generalista

Conforme decidido na [reunião de 24/08/2026](/Atas/subEquipe1/ata24_08.md), cada integrante da Subequipe 01 produz o **seu próprio** artefato generalista, escolhendo entre Rich Picture e Mapa Mental, e justificando a escolha. Esta página reúne os artefatos individuais.

---

## Mapa Mental — Pedro Luciano de Azevedo

### O que é o artefato

O **Mapa Mental** é uma técnica de representação gráfica radial na qual um conceito central é progressivamente refinado em ramos hierárquicos, com uso deliberado de palavras-chave curtas, cor e posição espacial para apoiar a memória e a associação de ideias (BUZAN; BUZAN, 1993). Diferentemente de um diagrama de fluxo, o mapa mental **não representa ordem temporal nem decisão**: ele representa *composição* — o que existe no domínio e como cada elemento se subordina a um agrupamento maior.

Na engenharia de software, esse tipo de representação se enquadra no que a literatura chama de artefato de **elicitação e organização de escopo**: um modelo informal, de baixo custo de produção e alta densidade de comunicação, cuja função é dar à equipe uma visão compartilhada do território antes de qualquer modelagem formal.

### O artefato

[![Mapa Mental do Mercado Livre](../../../assets/SubEquipe01/MapaMental_PedroLuciano.png)](../../../assets/SubEquipe01/MapaMental_PedroLuciano.png ':ignore')

<sub>*Clique no diagrama para abri-lo em tamanho real.*</sub>

> *Figura 1 — Mapa Mental do Mercado Livre, usado como base de inspiração para o projeto ([Projeto](/Projeto/Projeto.md)). Nó central: o sistema em estudo. Ramos de 1º nível: domínios funcionais (Descoberta do Produto, Decisão de Compra, Transação & Pagamento, Pós-venda), o contexto de atores, o subsistema de conta e acesso, e o ramo de qualidades (RNFs). Folhas: elementos efetivamente observados na interface durante a engenharia reversa.*

### Por que escolhi Mapa Mental (e não Rich Picture)

A escolha não foi por preferência estética, mas pelo **papel que o artefato precisava cumprir dentro desta entrega**. Três razões:

**1. O artefato precisava cobrir o sistema inteiro, não uma situação.**
O Rich Picture, na tradição da *Soft Systems Methodology* de Checkland (CHECKLAND, 1981; MONK; HOWARD, 1998), é forte exatamente onde o problema é *mal estruturado*: ele captura atores, preocupações, conflitos e o contexto de trabalho ao redor de uma situação. Seu poder está em mostrar tensão e ponto de vista. Só que o que a Subequipe 01 precisava neste momento era o oposto: um **inventário estruturado e navegável de todo o domínio**, para depois recortar dele o requisito não funcional do SIG e o fluxo do BPMN. Para inventariar composição, a hierarquia do mapa mental é mais direta do que a cena do Rich Picture.

**2. Precisava de rastreabilidade explícita para os outros dois artefatos.**
O ramo *Qualidades (RNFs)* do mapa aponta diretamente para o SIG de Usabilidade planejado, e o ramo *Descoberta do Produto* enumera exatamente os elementos (busca, autocompletar, filtros facetados, ordenação, breadcrumb) que devem reaparecer como **operacionalizações** no SIG e como **atividades** no BPMN quando esses artefatos forem construidos. A estrutura em ramos permite marcar esses elos ponto a ponto; em um Rich Picture, essa correspondência ficaria diluída na composição pictórica.

**3. Complementaridade dentro do grupo G1.**
A Subequipe 03 já produziu um Rich Picture da perspectiva do comprador. Fazer outro Rich Picture geraria redundância entre subequipes. Adotando o Mapa Mental, o grupo passa a ter as duas leituras — a situacional (Subequipe 03) e a composicional (esta) — sobre o mesmo domínio, o que é mais informativo do que duas versões da mesma técnica.

### Senso crítico sobre o artefato

O mapa mental tem limitações que reconheço e que motivaram os artefatos seguintes:

- **Não expressa ordem nem condição.** O mapa diz que "Filtros facetados" e "Ordenação" existem, mas não diz que o comprador só ordena *depois* de filtrar, nem o que acontece quando a busca não retorna resultados. Essa lacuna é precisamente o que o BPMN preenche.
- **Não expressa conflito.** No mapa, "Usabilidade" e "Desempenho" são dois nós irmãos, aparentemente independentes. Na prática, filtros facetados com contadores ajudam a usabilidade e **prejudicam** o tempo de resposta. Representar esse trade-off exige a notação do NFR Framework — e é por isso que o ramo de qualidades é um *ponteiro*, não uma resposta.
- **A hierarquia impõe uma classificação que nem sempre é única.** "Frete e prazo por CEP" foi colocado sob *Decisão de Compra*, mas poderia estar sob *Transação*. Escolhi manter sob Decisão porque, na interface observada, o frete é exibido **antes** do carrinho, e é essa antecipação que sustenta o softgoal *Prevenção de Erros* no SIG. A classificação, portanto, carrega uma decisão de projeto — o que é uma virtude do artefato, desde que documentada.

> **Nota de escopo:** o ramo *Qualidades (RNFs)* e o ramo *Descoberta do Produto* deste mapa são o ponto de partida planejado para o SIG de Usabilidade e para a modelagem BPMN, respectivamente — ambos ainda em elaboração. A tabela de elos ponto a ponto entre os três artefatos será adicionada aqui quando os três estiverem publicados.

---

## Referências

BUZAN, Tony; BUZAN, Barry. **The Mind Map Book**. London: BBC Books, 1993.

CHECKLAND, Peter. **Systems Thinking, Systems Practice**. Chichester: John Wiley & Sons, 1981.

MONK, Andrew; HOWARD, Steve. The Rich Picture: A Tool for Reasoning About Work Context. **Interactions**, v. 5, n. 2, p. 21–30, mar./abr. 1998.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 26/08/2026 | Adição do Mapa Mental e da justificativa da escolha | Pedro Luciano de Azevedo | -- |
