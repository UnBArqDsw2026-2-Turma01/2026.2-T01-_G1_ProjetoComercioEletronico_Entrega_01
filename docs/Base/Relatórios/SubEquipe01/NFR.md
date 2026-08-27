# NFR Framework

Conforme decidido na [reunião de 24/08/2026](/Atas/Subequipe1/ata24_08.md), no SIG cada integrante da Subequipe 01 assume um galho da árvore — um requisito não funcional — para consolidação posterior. Esta página reúne os galhos.

---

## SIG de Segurança do Checkout — Patrick Anderson Carvalho dos Santos

### O que é o artefato

O NFR Framework (CHUNG et al., 2000) trata requisitos não funcionais como *softgoals*: objetivos sem critério de satisfação binário, que não são simplesmente atendidos ou não, mas satisfeitos em grau, dentro de um conjunto de compromissos assumidos. O artefato do framework é o SIG (*Softgoal Interdependency Graph*), um grafo que registra três coisas que uma lista de requisitos não registra:

- **a decomposição** de um softgoal em subgoals, por tipo ou por tópico, com refinamento AND ou OR;
- **as contribuições** das decisões de projeto (as *operacionalizações*) sobre esses softgoals, rotuladas em `++` (MAKE), `+` (HELP), `−` (HURT) e `−−` (BREAK);
- **as correlações**, que são efeitos não intencionais de uma decisão sobre um softgoal que não era o alvo dela.

A avaliação se dá por propagação de rótulos: partindo das operacionalizações escolhidas, os rótulos sobem até a raiz, e o resultado ali é o veredito sobre o quanto aquele conjunto de decisões atende ao requisito. Os *claims*, desenhados em nuvem tracejada, se ligam às **ligações** e não aos nós: registram por que aquela contribuição tem o peso que tem.

### O artefato

[![SIG de Segurança do Checkout](../../../assets/SubEquipe01/SIG_Seguranca_Patrick.svg)](../../../assets/SubEquipe01/SIG_Seguranca_Patrick.svg ":ignore")

<sub>Clique na imagem para abrir o visualizador em tela cheia, com zoom e arraste.</sub>

> _Figura 5 — SIG de Segurança do checkout. Nuvem azul de borda fina: softgoal NFR. Nuvem verde de borda grossa: operacionalização. Nuvem tracejada: claim. Nuvem laranja, no painel à direita: softgoal que não é de segurança e que foi atingido por correlação. Fonte: Autor, 2026._

O diagrama é gerado por [`sig_seguranca_patrick.py`](https://github.com/UnBArqDsw2026-2-Turma01/2026.2-T01-_G1_ProjetoComercioEletronico_Entrega_01/blob/main/docs/assets/SubEquipe01/src/sig_seguranca_patrick.py), com nós, ligações e rótulos declarados no topo do arquivo. Para reproduzir:

```bash
python3 docs/assets/SubEquipe01/src/sig_seguranca_patrick.py
```

### Por que assumi o galho de Segurança

O Pedro Luciano sinalizou o galho de Usabilidade, e Segurança foi a escolha natural para mim por dois motivos que se reforçam.

O primeiro é que é o galho que a minha parte da engenharia reversa sustenta com evidência. O recorte que levantei — carrinho, endereço e entrada do checkout — é justamente o trecho em que o comprador entrega dado pessoal ao sistema. Cada operacionalização deste grafo tem origem rastreável em um achado registrado, e não em conhecimento geral sobre segurança.

O segundo é que Segurança e Usabilidade são o par clássico de softgoals concorrentes. Como os dois galhos existem dentro da mesma subequipe, o conflito não fica no plano teórico: `Facilidade de Uso [Checkout]` aparece neste grafo em estado de conflito, e é o mesmo softgoal que ancora o galho do Pedro. Na consolidação, é ali que os dois se costuram. Some-se a isso que Chung et al. (2000) tratam explicitamente da decomposição de Segurança em Integridade, Confidencialidade e Disponibilidade, o que dá base de literatura à decomposição de primeiro nível.

### Como o grafo foi montado

| Passo | O que foi feito |
| -- | -- |
| 1 | Softgoal raiz `Segurança [Checkout]` |
| 2 | Decomposição AND em `Confidencialidade [Dados do Comprador]` e `Integridade [Pedido]` |
| 3 | Segundo nível, também AND: Confidencialidade por tópico (`Endereço`, `Meio de Pagamento`); Integridade em `Validade [Dados do Formulário]` e `Autenticidade [Comprador]` |
| 4 | Operacionalizações derivadas dos achados da engenharia reversa |
| 5 | Correlações sobre `Tempo de Resposta`, `Facilidade de Uso` e `Acessibilidade` |
| 6 | *Claims* nas duas ligações que precisavam de justificativa |
| 7 | Propagação dos rótulos até a raiz |

### Operacionalizações e sua origem

| Operacionalização | Contribui para | Rótulo | Origem na [Engenharia Reversa](/Base/Relatórios/SubEquipe01/EngenhariaReversa.md) |
| -- | -- | -- | -- |
| Manter o contexto de retorno como token opaco na URL | `Confidencialidade [Endereço]` | `+` | T-B03 e T-B04 — destino de retorno e contexto viajam como parâmetro legível entre subdomínios (RNF-B05) |
| Tokenizar o meio de pagamento | `Confidencialidade [Meio de Pagamento]` | `++` | Ramo *Pontos de Confiança* do mapa mental; **não observado**, assumido como decisão de projeto |
| Validar no servidor | `Validade [Dados do Formulário]` | `++` | RN-B05 — nenhum campo declara `required`; a validação é delegada a script no cliente |
| Validar no cliente ao perder o foco | `Validade [Dados do Formulário]` | `+` | RN-B06 e T-B05 — a validação só ocorre na submissão |
| Reautenticar antes de confirmar | `Autenticidade [Comprador]` | `++` | Sessão autenticada persistente durante todo o percurso, sem nova verificação de identidade |
| Declarar obrigatoriedade com `required` | `Validade [Dados do Formulário]` | `+` | RN-B05 e RNF-B01 — a obrigatoriedade só existe no rótulo, e por negação |

### Correlações — o que piora

| Operacionalização | Softgoal atingido | Rótulo | Por quê |
| -- | -- | -- | -- |
| Validar no servidor | `Tempo de Resposta [Checkout]` | `−` | Cada validação passa a exigir ida ao servidor, somando latência a um fluxo que hoje responde localmente |
| Validar no cliente ao perder o foco | `Facilidade de Uso [Checkout]` | `+` | Feedback imediato por campo reduz retrabalho |
| Reautenticar antes de confirmar | `Facilidade de Uso [Checkout]` | `−−` | Insere uma etapa de identidade no momento de maior intenção de compra |
| Declarar obrigatoriedade com `required` | `Acessibilidade [Formulário]` | `++` | A obrigatoriedade passa a ser exposta programaticamente e alcança tecnologia assistiva |

### Propagação dos rótulos

| Softgoal | Contribuições recebidas | Resultado |
| -- | -- | -- |
| `Confidencialidade [Endereço]` | um `+` | **W⁺** |
| `Confidencialidade [Meio de Pagamento]` | um `++` | **✓** |
| `Confidencialidade [Dados do Comprador]` | AND (W⁺, ✓) → mínimo | **W⁺** |
| `Validade [Dados do Formulário]` | `++`, `+`, `+` | **✓** |
| `Autenticidade [Comprador]` | um `++` | **✓** |
| `Integridade [Pedido]` | AND (✓, ✓) | **✓** |
| **`Segurança [Checkout]`** | **AND (W⁺, ✓) → mínimo** | **W⁺** |
| `Tempo de Resposta [Checkout]` | um `−` | **W⁻** |
| `Facilidade de Uso [Checkout]` | um `+` e um `−−` | **conflito** |
| `Acessibilidade [Formulário]` | um `++` | **✓** |

O grafo não termina em "Segurança satisfeita". Termina em **W⁺**, e o motivo é localizável: `Confidencialidade [Endereço]` recebe uma única contribuição fraca, porque a única operacionalização que consegui derivar de evidência para ela — trocar o parâmetro legível por token opaco — reduz a exposição, mas não a elimina; o dado continua saindo do domínio de origem. Como a decomposição é AND, o elo mais fraco define o resultado do pai, e a dívida sobe até a raiz.

O conflito em `Facilidade de Uso` recebe `+` de uma decisão e `−−` de outra. A notação não resolve isso: marca o conflito e devolve a decisão a quem projeta. A minha decisão, registrada no claim C2, é aceitar o `−−` de forma condicionada — reautenticar só quando o meio de pagamento for novo, e não em toda compra, o que restringe a fricção a parte das transações. Com essa condição, o resultado assumido passa a **W⁻**. É uma decisão, não um cálculo, e por isso precisa aparecer no grafo como claim.

### Elos com os outros artefatos

| Elemento do SIG | Vem de | Vai para |
| -- | -- | -- |
| Softgoal raiz `Segurança [Checkout]` | Ramo *Qualidades (RNF)* do [mapa mental](/Base/Relatórios/SubEquipe01/ArtefatoGeneralista.md) | — |
| Decomposição de 1º nível | Mesmo ramo, mais o catálogo de Chung et al. (2000) | — |
| Todas as operacionalizações | RN-B05, RN-B06, RNF-B01, RNF-B05, T-B03 a T-B05 | — |
| Correlação `−` em Tempo de Resposta | Decisão de validar no servidor | Anotação de texto no [BPMN](/Base/Relatórios/SubEquipe01/BPMN.md) |
| `Facilidade de Uso [Checkout]` em conflito | Este grafo | Ponto de costura com o galho de Usabilidade |

### Limites do grafo

- **Disponibilidade ficou de fora.** O catálogo clássico decompõe Segurança em Integridade, Confidencialidade e Disponibilidade. Não modelei a terceira porque não consegui derivar dela nenhuma operacionalização a partir do que observei — disponibilidade não é observável por inspeção de interface em uma sessão. Incluí-la sem operacionalização a deixaria indecisa e, pela regra do AND, arrastaria a raiz inteira para indeciso, o que diria menos e não mais.
- **A tokenização é a operacionalização mais fraca do grafo.** Ela não vem de observação: o percurso parou antes do pagamento. Recebe `++` porque, se implementada, resolve o softgoal — mas o rótulo é sobre a decisão hipotética, não sobre o sistema observado. É a única linha da tabela cuja origem não aponta para um achado.
- **A regra do elo mais fraco no AND é uma convenção.** Adotei o mínimo entre os filhos por ser a leitura mais conservadora. Um avaliador poderia argumentar que vazar um endereço e vazar um cartão não têm o mesmo peso e que o grafo deveria priorizar. O framework permite; eu não usei, e o efeito é tratar os dois como igualmente críticos.
- **A primeira versão do grafo não tinha nenhuma aresta vermelha.** Ela listava só o que cada decisão melhora, e nesse formato o SIG não informa nada que uma tabela de requisitos já não informe. Ele só passou a ter função quando perguntei o que piora — e aí apareceram `Tempo de Resposta` em W⁻ e `Facilidade de Uso` em conflito.

---

## Referências

CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-Functional Requirements in Software Engineering**. Boston: Kluwer Academic Publishers, 2000.

MYLOPOULOS, John; CHUNG, Lawrence; NIXON, Brian. Representing and using nonfunctional requirements: a process-oriented approach. **IEEE Transactions on Software Engineering**, v. 18, n. 6, p. 483–497, jun. 1992.

NIELSEN, Jakob. Enhancing the explanatory power of usability heuristics. In: **Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '94)**. Boston: ACM, 1994. p. 152–158.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Adição do galho de Segurança: SIG do checkout, operacionalizações, correlações, claims e propagação de rótulos | Patrick Anderson Carvalho dos Santos | -- |
