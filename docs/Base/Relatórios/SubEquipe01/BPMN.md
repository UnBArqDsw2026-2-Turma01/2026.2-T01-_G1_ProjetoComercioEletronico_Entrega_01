# Modelagem BPMN

Conforme decidido na [reunião de 24/08/2026](/Atas/Subequipe1/ata24_08.md), o modelo BPMN parte de um dos fluxos identificados pela [Engenharia Reversa](/Base/Relatórios/SubEquipe01/EngenhariaReversa.md), e cada integrante ficou responsável por uma parte do diagrama. Esta página reúne os modelos da Subequipe 01.

---

## Fluxo de Carrinho, Endereço e Entrada de Checkout — Patrick Anderson Carvalho dos Santos

> **Nota de escopo:** este modelo cobre o recorte que eu registrei na engenharia reversa. O modelo consolidado do fluxo de **busca e escolha de produto**, construído em conjunto pela subequipe no Miro, é complementar a este e cobre o trecho anterior da jornada.

### O que é a notação

**BPMN** (*Business Process Model and Notation*) é o padrão da OMG para modelagem de processos de negócio (OMG, 2011). A escolha da notação para este artefato não é neutra: entre os diagramas disponíveis, o BPMN é o único que distingue **quem faz** (*pools* e *lanes*) de **o que é trocado entre os participantes** (*fluxo de mensagem*) — e essa distinção é exatamente o que a engenharia reversa de caixa-preta precisa expressar, porque tudo que eu observei foi **troca**, e o que acontece dentro da plataforma é inferência.

Três regras da notação são estruturais e foram respeitadas com atenção:

1. **Fluxo de sequência não atravessa *pool*.** Comunicação entre participantes é sempre **fluxo de mensagem** — linha tracejada, com círculo vazado na origem e ponta de seta aberta no destino. Todas as ligações entre a raia do Comprador e a da plataforma neste modelo são fluxos de mensagem.
2. **Gateway não é decisão do sistema, é bifurcação do fluxo.** O gateway exclusivo (losango com X) marca que exatamente um caminho é seguido. A condição fica no rótulo do fluxo de saída (`sim` / `não`), não dentro do losango.
3. **Cada *pool* com fluxo de sequência tem início e fim próprios.** As duas raias abertas deste modelo têm o seu evento de início e o seu evento de fim.

### O artefato

[![BPMN do fluxo de carrinho, endereço e checkout](../../../assets/SubEquipe01/BPMN_Checkout_Patrick.svg)](../../../assets/SubEquipe01/BPMN_Checkout_Patrick.svg ":ignore")

<sub>_Clique no diagrama para abri-lo em tamanho real._</sub>

> _Figura 6 — Modelo BPMN do fluxo de carrinho, endereço de entrega e entrada de checkout do G1_ProjetoComercioEletronico. Fonte: Autor, 2026._

Como o Mapa Mental e o SIG, o diagrama é **gerado por script** — o código está em [`bpmn_checkout_patrick.py`](https://github.com/UnBArqDsw2026-2-Turma01/2026.2-T01-_G1_ProjetoComercioEletronico_Entrega_01/blob/main/docs/assets/SubEquipe01/src/bpmn_checkout_patrick.py), com tarefas, gateways, fluxos e anotações declarados em estruturas de dados:

```bash
python3 docs/assets/SubEquipe01/src/bpmn_checkout_patrick.py
```

### Recursos da notação utilizados

As Diretrizes pedem explicitamente "usar os vários recursos de modelagem […] da notação BPMN". O modelo emprega:

| Recurso | Onde aparece | Por que estava lá |
| -- | -- | -- |
| *Pool* aberta | `Comprador`, `G1_ProjetoComercioEletronico` | Dois participantes com processo próprio observável |
| *Pool* colapsada | `Vendedor` | Participa do processo — recebe o pedido — mas seu processo interno está fora do recorte; colapsar é a forma correta de dizer isso |
| Evento de início / fim | Um par por *pool* aberta | Fecha o ciclo de vida de cada processo |
| Tarefa de usuário | Toda a raia do Comprador | Atividades executadas por pessoa na interface |
| Tarefa de serviço | Toda a raia da plataforma | Atividades automatizadas, **todas inferidas** |
| Gateway exclusivo | `Endereço definido?`, `Dados válidos?` | As duas únicas bifurcações que a observação sustenta |
| Fluxo de mensagem | 7 ligações entre *pools* | Cada troca observada entre comprador e plataforma |
| Anotação de texto | Sobre `Validar dados na submissão` | Registra o conflito herdado do SIG |

### Rastreabilidade — de onde vem cada elemento

| Elemento do modelo | Origem |
| -- | -- |
| `Adicionar item ao carrinho` → `Agrupar itens por vendedor` | T01 e T02; RN-P01 — o carrinho agrupa por vendedor |
| `Calcular frete e prazo por CEP` → `Revisar itens do carrinho` | RN-P04 e ficha do produto; o frete é conhecido antes do checkout |
| `Cadastrar endereço de entrega` e o gateway que leva a ele | T03 e T04 — o endereço é escolhido em tela própria, fora do carrinho |
| Fluxo de mensagem `CEP e endereço` | Formulário de endereço, seção 5 da engenharia reversa |
| Gateway `Dados do formulário válidos?` e `Corrigir o campo apontado` | RN-P06 e T05 — a validação ocorre **na submissão**, e é isso que justifica o laço de correção existir *depois* do envio, e não durante o preenchimento |
| Anotação sobre `Validar dados na submissão` | Correlação `−` do [SIG de Segurança](/Base/Relatórios/SubEquipe01/NFR.md) sobre `Tempo de Resposta [Checkout]` |
| `Confirmar a compra`, `Registrar o pedido`, `Notificar o vendedor` | **Inferidos** — o percurso foi interrompido antes do pagamento |

### Senso crítico

- **O laço de correção é a parte mais informativa do modelo, e ele existe por causa de um defeito.** Em um sistema que validasse campo a campo na perda de foco, esse laço seria curto e local. Como a validação só acontece na submissão (RN-P06), o comprador percorre o formulário inteiro, envia, e só então descobre o erro — o que no modelo aparece como um retorno que atravessa o gateway. **O desenho torna visível o custo de uma decisão de implementação**, e é o melhor argumento que eu tenho a favor de modelar antes de propor requisito.
- **A raia da plataforma é hipótese, e o diagrama não sinaliza isso graficamente.** Todas as seis tarefas de serviço foram inferidas do comportamento observável; nenhuma foi observada. A notação BPMN não tem um recurso próprio para marcar "atividade inferida", e eu optei por registrar a distinção **no texto** — nesta tabela e no relatório de engenharia reversa — em vez de inventar uma convenção gráfica que ninguém mais leria. É uma limitação assumida, não resolvida.
- **Modelei um caminho feliz com duas exceções, e o processo real tem mais.** Ficaram de fora: item que sai de estoque enquanto está no carrinho, pagamento recusado, CEP fora de área de entrega. Nenhum deles foi observado, e adicioná-los por dedução encheria o diagrama de caminhos que eu não posso sustentar. Preferi um modelo menor e verificável — o que é coerente com a orientação das Diretrizes de que a ideia não é quantidade, e sim qualidade.
- **Modelar depois do SIG mudou o diagrama.** A anotação de texto sobre `Validar dados na submissão` só está ali porque o SIG já tinha registrado que validar no servidor cobra em `Tempo de Resposta`. Se eu tivesse desenhado o BPMN primeiro, ele seria só uma sequência de caixas. Os três artefatos em cadeia — mapa mental, engenharia reversa, SIG, BPMN — foram mais lentos de produzir nessa ordem, e é a razão de haver rastro entre eles em vez de quatro desenhos independentes.

---

## Referências

OBJECT MANAGEMENT GROUP. **Business Process Model and Notation (BPMN), Version 2.0**. OMG Document formal/2011-01-03. Needham: OMG, 2011.

CHIKOFSKY, Elliot J.; CROSS II, James H. Reverse engineering and design recovery: a taxonomy. **IEEE Software**, v. 7, n. 1, p. 13–17, jan. 1990.

CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-Functional Requirements in Software Engineering**. Boston: Kluwer Academic Publishers, 2000.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Adição do modelo BPMN do fluxo de carrinho, endereço e entrada de checkout, gerado por script, com 3 pools, 2 gateways, 7 fluxos de mensagem, anotação de texto e tabela de rastreabilidade | Patrick Anderson Carvalho dos Santos | -- |
