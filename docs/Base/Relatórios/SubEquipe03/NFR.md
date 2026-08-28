# NFR Framework

---

## O que é o artefato

O NFR Framework (CHUNG et al., 2000) trata requisitos não funcionais como *softgoals*: objetivos sem critério de satisfação binário, que não são simplesmente atendidos ou não, mas satisfeitos em grau, dentro de um conjunto de compromissos assumidos. O artefato do framework é o SIG (*Softgoal Interdependency Graph*), um grafo que registra três coisas que uma lista de requisitos não registra:

*   **A decomposição** de um softgoal em subgoals, por tipo ou por tópico, com refinamento AND ou OR;
*   **As contribuições** das decisões de projeto (as *operacionalizações*) sobre esses softgoals, rotuladas em `++` (MAKE), `+` (HELP), `−` (HURT) e `−−` (BREAK);
*   **As correlações**, que são efeitos não intencionais de uma decisão sobre um softgoal que não era o alvo dela (os *trade-offs*).

A avaliação se dá por propagação de rótulos: partindo das operacionalizações escolhidas, os rótulos sobem até a raiz, e o resultado ali é o veredito sobre o quanto aquele conjunto de decisões atende ao requisito. Os *claims*, desenhados em nuvem tracejada, se ligam às **ligações** e não aos nós, registrando o embasamento empírico da contribuição.

### Legenda dos Símbolos (NFR Framework)

* ☁️ **Nuvem de borda fina:** Softgoal (Requisito Não Funcional).
* ☁️ **Nuvem de borda grossa:** Operacionalização (Decisão de design ou solução técnica).
* ☁️ **Nuvem com borda tracejada:** Claim (Justificativa ou argumento empírico).
* ➔ **Seta contínua:** Decomposição (Refina um softgoal em partes menores).
* ⇢ **Seta tracejada:** Link de Contribuição (Impacto de uma decisão sobre um softgoal).
* **[ ++ ] Make:** Contribuição positiva forte (Resolve o requisito).
* **[ + ] Help:** Contribuição positiva parcial (Ajuda o requisito).
* **[ − ] Hurt:** Contribuição negativa parcial (Prejudica o requisito).
* **[ −− ] Break:** Contribuição negativa forte (Inviabiliza o requisito).

---

## Como os grafos foram montados

A modelagem foi construída estritamente por **engenharia reversa (black-box)**, analisando o tráfego de rede e o comportamento da interface do Mercado Livre, em vez de partir de uma documentação interna. 

| Passo | O que foi feito |
| :--- | :--- |
| 1 | Separação dos fluxos temporais em dois grafos distintos: **Cadastro** e **Login**, respeitando a arquitetura de microsserviços. |
| 2 | Decomposição de 1º nível definindo os *softgoals* raiz (Usabilidade, Segurança, Correção, Acessibilidade e Performance). |
| 3 | Mapeamento de operacionalizações baseadas em padrões da indústria confirmados via inspeção HTTP/DOM (ex: interceptação de eventos `input` e cookies persistentes). |
| 4 | Identificação de correlações negativas (trade-offs), destacando onde a plataforma sacrifica um requisito em prol de outro (ex: sacrificar Confidencialidade por Eficiência). |
| 5 | Ancoragem de *Claims* documentando a lógica de negócio por trás das escolhas de design. |
| 6 | Propagação dos rótulos do nível das soluções até a raiz de cada subsistema. |

---

## 1. Subsistema de Cadastro

O foco do cadastro inicial na plataforma é a aquisição acelerada de usuários. O grafo evidencia que a arquitetura posterga validações complexas para reduzir a fricção de entrada, introduzindo o padrão de *Progressive Profiling*.


<p align="center">
  <img src="assets/Subequipe3/cadastro2.0Diagram.svg" alt="SIG Cadastro NFR Framework">
  <br>
  <em>Figura 1 — SIG do Subsistema de Cadastro.</em>
  <br>
  <small>Autores: José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes.</small>
</p>

### Operacionalizações e sua origem

| Operacionalização | Contribui para | Rótulo | Origem / Claim |
| :--- | :--- | :--- | :--- |
| Validação Contínua de Input em Tempo Real | `Facilidade de Aprendizado` | `++` | O feedback visual atômico a cada tecla funciona como um tutor, guiando a criação de senha sem exigir manuais[cite: 1]. |
| Validação Contínua de Input em Tempo Real | `Eficiência [Cadastro]` | `+` | O usuário corrige erros instantaneamente, antes de submeter o formulário[cite: 1]. |
| Adiar coleta de dados complexos (Lazy Reg.) | `Eficiência [Cadastro]` | `++` | Postergar a validação do CPF para a etapa de Vendedor remove a fricção inicial do funil. |
| Adiar coleta de dados complexos (Lazy Reg.) | `Usabilidade [Cadastro]` | `++` | Formulários menores reduzem a carga cognitiva da etapa de conversão. |
| Cadastro via Terceiros (OAuth) | `Eficiência [Cadastro]` | `++` | Contorna o preenchimento manual de formulários, criando a conta em segundos[cite: 1]. |
| Cadastro via Terceiros (OAuth) | `Verificação [Identidade]` | `++` | Assume o e-mail validado pelo Google/Facebook como fonte de verdade confiável. |

### Correlações — o que piora (Trade-offs)

| Operacionalização | Softgoal atingido | Rótulo | Por quê (Claim) |
| :--- | :--- | :--- | :--- |
| Cadastro via Terceiros (OAuth) | `Confidencialidade [Senha]` | `−` | Atrelar o acesso a um provedor externo aumenta a superfície de ataque; se o Google vazar, a conta do ML fica vulnerável. |
| Verificação por SMS / e-mail | `Eficiência [Cadastro]` | `−` | Introduz uma interrupção forçada no fluxo e dependência de latência de terceiros (operadoras). |
| Cadastro em múltiplas etapas (Wizard) | `Eficiência [Cadastro]` | `−` | Embora ajude na aprendizagem, aumenta o número absoluto de cliques e transições de tela. |

### Propagação neste galho

| Softgoal | Entradas | Rótulo |
| :--- | :--- | :--- |
| `Facilidade de Aprendizado [Cadastro]` | um `++`, um `+` | **✓** |
| `Eficiência [Cadastro]` | três `++`, dois `−` | **W⁺** |
| `Unicidade / Verificação` | um `++`, um `+` | **✓** |
| `Confidencialidade [Senha]` | um `++`, um `+`, um `−` | **W⁺** |
| **`Usabilidade [Cadastro]`** | **AND (✓, W⁺)** | **W⁺** |
| **`Segurança [Cadastro]`** | **AND (✓, W⁺)** | **W⁺** |

O subsistema de Cadastro possui um equilíbrio notável. A decisão de fragmentar o formulário (Lazy Registration) compensa fortemente as penalidades de tempo causadas pelas etapas obrigatórias de verificação de identidade.

---

## 2. Subsistema de Login e Gestão de Sessão

O grafo de login revela uma clara priorização da conversão e retenção (compra por impulso) sobre a segurança estrita. A arquitetura adota o modelo *Passwordless* e sessões persistentes de alto risco local.

<p align="center">
  <img src="assets/Subequipe3/login2Diagram.svg" alt="SIG Login NFR Framework">
  <br>
  <em>Figura 1 — SIG do Subsistema de Login.</em>
  <br>
  <small>Autores: José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes.</small>
</p>


### Operacionalizações e sua origem

| Operacionalização | Contribui para | Rótulo | Origem / Claim |
| :--- | :--- | :--- | :--- |
| Autenticação Passwordless via OTP | `Eficiência [Login]` | `++` | Remove a fricção e a necessidade de fluxos de "esqueci minha senha", maximizando retenção. |
| Sessão Persistente (Long-Lived Cookie) | `Usabilidade [Login]` | `+` | A autenticação sobrevive ao desligamento do SO, eliminando a barreira de login em visitas futuras. |
| Filas de Mensageria Express Lane | `Tempo de Resposta` | `++` | Isolamento de filas de mensageria garante que o SMS de login chegue com latência quase zero. |
| Autenticação Multicanal Dinâmica | `Disponibilidade [Login]` | `++` | Oferecer SMS, E-mail e WhatsApp em paralelo evita o bloqueio da conta caso uma operadora falhe. |

### Correlações — o que piora (Trade-offs)

| Operacionalização | Softgoal atingido | Rótulo | Por quê (Claim) |
| :--- | :--- | :--- | :--- |
| Autenticação Passwordless via OTP | `Confidencialidade [Conta]` | `−−` | Transfere a segurança da conta inteiramente para a operadora de telefonia, assumindo o risco severo de *SIM Swap*. |
| Sessão Persistente (Long-Lived Cookie) | `Confidencialidade [Conta]` | `−` | Amplia drasticamente a janela de exposição para ataques de *Account Takeover* local caso o dispositivo seja compartilhado/roubado. |
| Erro de e-mail ofuscado | `Clareza na Comunicação` | `−` | Ao mascarar erros para proteger contra testes de enumeração de contas, o usuário legítimo não sabe o que precisa corrigir. |

### Propagação neste galho

| Softgoal | Entradas | Rótulo |
| :--- | :--- | :--- |
| `Tempo de Resposta [Login]` | um `++` | **✓** |
| `Disponibilidade [Login]` | um `++`, um `+` | **✓** |
| `Eficiência [Login]` | um `++` | **✓** |
| `Clareza na Comunicação de Erros` | um `−` | **W⁻** |
| `Confidencialidade [Credenciais]` | um `+`, um `−`, um `−−` | **W⁻** |
| **`Usabilidade [Login]`** | **AND (✓, W⁻)** | **W⁻** |
| **`Segurança [Login]`** | **AND (✓, W⁻)** | **W⁻ — Crítico** |

A propagação revela que `Segurança [Login]` é o galho crítico. A adoção massiva de conveniência (Passwordless e Sessões Persistentes) arrasta a confidencialidade para baixo. A arquitetura aceita essa dívida intencionalmente, mitigando-a apenas *a posteriori* com padões de *Step-Up Authentication* (re-pedir a senha) durante ações financeiras sensíveis (Checkout).

---

## Limites dos Grafos

*   **A abordagem Black-Box:** O grau de impacto (MAKE vs. HELP) é inferido pelo comportamento externo da aplicação e medições de rede. Mecanismos internos de mitigação, como motores de análise de risco baseados em IA que bloqueiam atividades anômalas antes de comprometer a confidencialidade, não estão representados por não serem inspecionáveis no frontend.
*   **Omitida a mitigação no Checkout:** O SIG de Login isola a gestão de sessão. A dívida em Segurança (marcada como crítica) não significa que o Mercado Livre seja inseguro, mas sim que a proteção foi empurrada para outro subsistema (Pagamentos), que exige a re-autenticação para quebrar a persistência do cookie antes de efetivar transações.
*   **Avaliação do Elo Mais Fraco:** Utilizou-se a convenção estrita de propagação mínima no relacionamento AND, fazendo com que a nota geral da raiz seja fortemente penalizada por decisões locais de design (como ofuscar a mensagem de erro).

---

## Referências

CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-Functional Requirements in Software Engineering**. Boston: Kluwer Academic Publishers, 2000.

Observações e inspeções empíricas realizadas diretamente na plataforma Mercado Livre, validadas através de análise de payloads HTTP e telemetria de DOM (Agosto, 2026).


## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Refinamento dos SIGs de Cadastro e Login (adição de trade-offs, Progressive Profiling e Autenticação Passwordless) | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.2 | 27/08/2026 |Adição de legendas da figura| José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.2 | 27/08/2026 |Correção dos caminhos das figuras| Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
