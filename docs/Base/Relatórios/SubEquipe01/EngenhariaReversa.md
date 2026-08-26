# Engenharia Reversa

Conforme decidido na [reunião de 24/08/2026](/Atas/subEquipe1/ata24_08.md), a engenharia reversa é feita registrando **por escrito** cada elemento observado na tela, para então derivar fluxos, regras de negócio e requisitos — as perguntas do material da professora foram divididas entre os integrantes. Esta página reúne os registros individuais da Subequipe 01.

---

## Fluxo de Busca e Escolha de Produto — Pedro Luciano de Azevedo

> **Nota de escopo:** este recorte é a base para o SIG de Usabilidade e para a [Modelagem BPMN](/Base/Relatórios/SubEquipe01/BPMN.md) do mesmo fluxo, ambos ainda em elaboração.

### 1. Contexto da engenharia reversa

**Objeto de estudo.** O G1_ProjetoComercioEletronico se inspira no Mercado Livre, com modelo misto B2C/C2C (múltiplos vendedores anunciando no mesmo catálogo).

**Recorte.** Fluxo de **busca e escolha de produto**: do momento em que o comprador digita um termo até o momento em que decide que aquele produto é o que ele quer. Escolhi este recorte por três razões: (i) é integralmente observável sem conta autenticada e sem realizar compra; (ii) é o fluxo com maior densidade de decisões de usabilidade, o que o conecta diretamente ao SIG de Usabilidade planejado; e (iii) é o fluxo em que o comprador desiste, quando desiste.

### 2. Processo aplicado

O que foi feito se enquadra no que Chikofsky e Cross (1990) definem como **engenharia reversa**: o processo de analisar um sistema para identificar seus componentes e inter-relações, e criar representações do sistema em outra forma ou em nível mais alto de abstração — sem alterá-lo. Trata-se, mais especificamente, de **recuperação de projeto** (*design recovery*), em que se combina a observação do artefato com conhecimento de domínio para reconstruir abstrações que o artefato não expõe.

Como não há acesso ao código-fonte, o método é de **caixa-preta, a partir da interface** — abordagem análoga à do *GUI ripping* descrito por Memon, Banerjee e Nagarajan (2003), em que a estrutura do sistema é inferida percorrendo sistematicamente os estados da interface e registrando os widgets, eventos e transições de cada estado.

**Etapas executadas:**

| # | Etapa | O que foi feito |
| -- | -- | -- |
| 1 | Delimitação | Definição do recorte (busca → escolha) e do ator principal (comprador não autenticado) |
| 2 | Percurso exploratório | Execução do fluxo do início ao fim, sem registro, para reconhecer os estados de tela |
| 3 | Inventário de tela | Segundo percurso, registrando **por escrito** cada elemento visível por estado: campos, controles, dados exibidos, feedbacks |
| 4 | Provocação de exceções | Busca com termo sem resultado, filtro que zera a listagem, uso do botão "voltar" do navegador |
| 5 | Inferência de fluxo | Derivação da sequência de atividades, pontos de decisão e trocas de mensagem entre comprador e plataforma |
| 6 | Inferência de regras e requisitos | Extração de regras de negócio e requisitos a partir do que o inventário e as exceções evidenciam |

**Ferramentas.** Navegador (inspeção visual e observação da URL) e planilha compartilhada do grupo para o inventário escrito.

### 3. Achados — inventário do que está na tela

| Estado de tela | Elementos observados |
| -- | -- |
| **Vitrine / campo de busca** | Campo de busca com foco automático; lista de sugestões que surge **ao digitar**, antes de submeter; histórico de buscas recentes |
| **Listagem de resultados** | Contador de resultados; facetas de filtro (categoria, preço, condição, frete, localização) **com contador por opção**; seletor de ordenação (relevância, menor preço, maior preço); breadcrumb de categorias; cartões de produto; carregamento de novos resultados **por rolagem**, sem paginação clicável; filtros e página refletidos como **parâmetros na URL** |
| **Cartão de produto (na listagem)** | Imagem; título; preço e parcelamento; selo de frete; **nota, número de avaliações** e indicação de reputação do vendedor |
| **Ficha do produto** | Carrossel de imagens com zoom; preço e parcelamento; **campo de CEP que recalcula frete e prazo na própria página**; dados do vendedor com reputação; bloco de avaliações; perguntas e respostas; produtos relacionados |
| **Estado vazio** | Mensagem de "nenhum resultado"; sugestão de termos alternativos; sugestão de remover filtros |
| **Retorno pelo botão "voltar"** | Os filtros são preservados (vêm da URL); a **posição de rolagem não é** — a listagem reinicia do topo |

### 4. Achados — regras de negócio inferidas

| ID | Regra de negócio |
| -- | -- |
| RN01 | A listagem só é exibida se a consulta retornar ao menos um resultado; caso contrário, o sistema apresenta estado vazio com termos alternativos. |
| RN02 | A ordenação padrão da listagem é por relevância, não por preço. |
| RN03 | Filtros são cumulativos e cada faceta exibe antecipadamente a quantidade de resultados que restará ao ser aplicada. |
| RN04 | O frete e o prazo dependem do CEP informado e são calculados na ficha do produto, **antes** do carrinho. |
| RN05 | Todo produto de marketplace exibe reputação do vendedor junto ao preço, já na listagem. |
| RN06 | O estado da consulta (termo, filtros, ordenação, página) é carregado na URL, o que torna a busca compartilhável e reproduzível. |

### 5. Achados — requisitos derivados

| ID | Requisito | Tipo |
| -- | -- | -- |
| RF01 | O sistema deve sugerir termos enquanto o comprador digita, antes da submissão. | Funcional |
| RF02 | O sistema deve permitir filtrar a listagem por facetas cumulativas, exibindo a contagem prévia de resultados. | Funcional |
| RF03 | O sistema deve permitir reordenar a listagem por relevância e por preço. | Funcional |
| RF04 | O sistema deve calcular frete e prazo por CEP na ficha do produto. | Funcional |
| RF05 | O sistema deve apresentar, para cada oferta, nota, número de avaliações e reputação do vendedor. | Funcional |
| RF06 | Em consulta sem resultados, o sistema deve oferecer termos alternativos. | Funcional |
| RNF01 | O comprador deve alcançar a ficha do produto em poucos passos a partir da busca. | Não funcional — Eficiência de Uso |
| RNF02 | O retorno à listagem deve preservar filtros **e posição**. | Não funcional — Reversibilidade |
| RNF03 | A aplicação de uma faceta deve produzir feedback imediato na listagem. | Não funcional — Feedback Imediato |

> **RNF02 é um requisito que o sistema observado não satisfaz.** Ele foi derivado justamente da etapa de provocação de exceções (etapa 4): o retorno pelo botão "voltar" preserva os filtros (carregados na URL), mas reinicia a posição de rolagem da listagem. Esse achado é o ponto de partida para o SIG de Usabilidade e para a modelagem BPMN deste fluxo, ainda não adicionados.

### 6. Senso crítico

- **Os achados são uma hipótese sobre o interior, não uma descrição dele.** As atividades internas inferidas (como "consultar índice do catálogo" e "ranquear e paginar resultados") foram derivadas do comportamento observável, não observadas diretamente. Elas são plausíveis e suficientes para explicar o que se vê, mas a implementação real pode ser bastante diferente. Chikofsky e Cross (1990) são explícitos quanto a isso: recuperação de projeto produz abstrações **coerentes com** o sistema, não necessariamente **idênticas ao** projeto original.
- **O nível de detalhe do inventário foi escolhido, não dado.** Registrei o suficiente para sustentar as regras de negócio e os requisitos listados acima, e deliberadamente **não** persegui chamadas de serviço, cache ou paginação técnica, que não são observáveis pelo método usado.
- **Limitações do método de caixa-preta.** Sem conta autenticada, ficam fora do inventário a personalização por histórico, as recomendações e qualquer variação por teste A/B — que, se existirem, alteram o fluxo real de descoberta.

---

## Referências

CHIKOFSKY, Elliot J.; CROSS II, James H. Reverse engineering and design recovery: a taxonomy. **IEEE Software**, v. 7, n. 1, p. 13–17, jan. 1990.

MEMON, Atif; BANERJEE, Ishan; NAGARAJAN, Adithya. GUI Ripping: Reverse Engineering of Graphical User Interfaces for Testing. In: **Proceedings of the 10th Working Conference on Reverse Engineering (WCRE '03)**. Victoria: IEEE, 2003. p. 260–269.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 26/08/2026 | Criação da página; registro da engenharia reversa do fluxo de busca e escolha de produto (contexto, processo, inventário de tela, regras de negócio e requisitos derivados) | Pedro Luciano de Azevedo | -- |
