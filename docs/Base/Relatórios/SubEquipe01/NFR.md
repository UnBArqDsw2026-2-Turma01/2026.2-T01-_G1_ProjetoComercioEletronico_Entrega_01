# NFR Framework

Conforme decidido na [reunião de 24/08/2026](/Atas/Subequipe1/ata24_08.md), no SIG cada integrante da Subequipe 01 assume um galho da árvore — um requisito não funcional — para consolidação posterior. Esta página registra o grafo consolidado e a divisão dos galhos.

---

## O que é o artefato

O NFR Framework (CHUNG et al., 2000) trata requisitos não funcionais como *softgoals*: objetivos sem critério de satisfação binário, que não são simplesmente atendidos ou não, mas satisfeitos em grau, dentro de um conjunto de compromissos assumidos. O artefato do framework é o SIG (*Softgoal Interdependency Graph*), um grafo que registra três coisas que uma lista de requisitos não registra:

- **a decomposição** de um softgoal em subgoals, por tipo ou por tópico, com refinamento AND ou OR;
- **as contribuições** das decisões de projeto (as *operacionalizações*) sobre esses softgoals, rotuladas em `++` (MAKE), `+` (HELP), `−` (HURT) e `−−` (BREAK);
- **as correlações**, que são efeitos não intencionais de uma decisão sobre um softgoal que não era o alvo dela.

A avaliação se dá por propagação de rótulos: partindo das operacionalizações escolhidas, os rótulos sobem até a raiz, e o resultado ali é o veredito sobre o quanto aquele conjunto de decisões atende ao requisito. Os *claims*, desenhados em nuvem tracejada, se ligam às **ligações** e não aos nós: registram por que aquela contribuição tem o peso que tem.

---

## O artefato

[![SIG de Usabilidade](../../../assets/SubEquipe01/SIG_Usabilidade.svg)](../../../assets/SubEquipe01/SIG_Usabilidade.svg ":ignore")

<sub>Clique na imagem para abrir o visualizador em tela cheia, com zoom e arraste.</sub>

> _Figura 5 — SIG de Usabilidade do G1\_ProjetoComercioEletronico. Nuvem de borda fina: softgoal NFR. Nuvem azul de borda grossa: operacionalização. Nuvem tracejada âmbar: claim. Aresta verde: contribuição positiva. Aresta vermelha: contribuição negativa. Fonte: Autor, 2026._

### Por que Usabilidade é a raiz do grafo do grupo

O senso crítico do [mapa mental](/Base/Relatórios/SubEquipe01/ArtefatoGeneralista.md) já apontava a lacuna que motivou este artefato: no mapa, "Usabilidade" e "Desempenho" aparecem como nós irmãos, aparentemente independentes, quando na prática filtros facetados com contadores **ajudam** a usabilidade e **prejudicam** o tempo de resposta. Representar esse trade-off exige a notação do NFR Framework.

Usabilidade foi escolhida como raiz única porque é o softgoal que os três recortes de engenharia reversa da subequipe alcançam ao mesmo tempo — busca, checkout e a leitura situacional do Rich Picture — o que permite um grafo só, com galhos que se cruzam, em vez de três grafos isolados que não conversariam na consolidação.

### Como o grafo foi montado

| Passo | O que foi feito |
| -- | -- |
| 1 | Softgoal raiz `Usabilidade [G1_ProjetoComercioEletronico]` |
| 2 | Decomposição AND de 1º nível em quatro softgoals de tipo, atribuídos aos integrantes |
| 3 | Segundo nível, também AND: cada galho refinado em dois softgoals por tópico |
| 4 | Operacionalizações derivadas dos achados registrados na engenharia reversa e no Rich Picture |
| 5 | Correlações negativas: o que cada decisão piora, e não só o que melhora |
| 6 | *Claims* nas duas ligações que precisavam de justificativa |
| 7 | Propagação dos rótulos, do nível das operacionalizações até a raiz |

### Divisão dos galhos

| Galho de 1º nível | Softgoals de 2º nível | Responsável | Base de evidência |
| -- | -- | -- | -- |
| `Facilidade de Aprendizado [Comprador novo]` e `Eficiência de Uso [Busca de produto]` | Consistência, Reconhecimento, Poucos Passos, Tempo de Resposta | Pedro Luciano de Azevedo | [Engenharia reversa do fluxo de busca e escolha de produto](/Base/Relatórios/SubEquipe01/EngenhariaReversa.md) |
| `Prevenção de Erros [Decisão de compra]` | Feedback Imediato, Reversibilidade | Patrick Anderson Carvalho dos Santos | Recorte de carrinho, endereço e checkout; [BPMN](/Base/Relatórios/SubEquipe01/BPMN.md) do mesmo fluxo |
| `Satisfação [Comprador]` | Estética Minimalista, Confiança Percebida | Guilherme Costa Zanella | [Rich Picture](/Base/Relatórios/SubEquipe01/ArtefatoGeneralista.md) do fluxo de compra |

As operacionalizações não respeitam essa divisão, e isso é deliberado: `Filtros facetados` contribui para um softgoal do Pedro e um do Patrick; `Rolagem infinita` toca os três galhos. É justamente onde os galhos se cruzam que o grafo diz algo que uma lista de requisitos não diria.

---

## Referências

CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-Functional Requirements in Software Engineering**. Boston: Kluwer Academic Publishers, 2000.

MONK, Andrew; HOWARD, Steve. The Rich Picture: A Tool for Reasoning About Work Context. **Interactions**, v. 5, n. 2, p. 21–30, mar./abr. 1998.

MYLOPOULOS, John; CHUNG, Lawrence; NIXON, Brian. Representing and using nonfunctional requirements: a process-oriented approach. **IEEE Transactions on Software Engineering**, v. 18, n. 6, p. 483–497, jun. 1992.

NIELSEN, Jakob. Enhancing the explanatory power of usability heuristics. In: **Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '94)**. Boston: ACM, 1994. p. 152–158.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Adição da parte geral sobre o SIG | Patrick Anderson Carvalho dos Santos, Pedro Luciano de Azevedo, Guilherme Costa Zanella | -- |
