# Engenharia Reversa e Modelagem de Processos

Este documento é a entrega conjunta da subequipe responsável pelos **Subsistemas de Identidade (Cadastro e Login)**. O levantamento consolida a análise de requisitos não funcionais (que originaram os SIGs do NFR Framework) e a modelagem do fluxo de negócio (BPMN). O trabalho integra a observação técnica da interface com a estruturação formal dos processos.

| Frente | Escopo | Foco do Levantamento |
| -- | -- | -- |
| **A** | Cadastro de Usuário | Aquisição, Progressive Profiling e Verificação de E-mail |
| **B** | Login e Gestão de Sessão | Autenticação por Credenciais, 2FA opcional e Retenção |
| **C** | Modelagem BPMN | Estruturação lógica e notação de processos |

Os recortes se encadeiam diretamente: as regras de negócio e os trade-offs de usabilidade levantados em A e B formam a base empírica estruturada no processo C.

---

## 1. Contexto e objeto de estudo

O foco deste estudo são os módulos de Autenticação e Gestão de Identidade (IAM) de uma plataforma de comércio eletrônico de referência. O sistema adota padrões modernos para balancear a conversão de novos usuários com a segurança das transações. A engenharia reversa foi aplicada sobre a interface web, analisando os fluxos desde o preenchimento de dados até os bloqueios de segurança.

## 2. Método aplicado

O levantamento combinou **recuperação de projeto** (*design recovery*) em nível de interface (caixa-preta) com o uso de ferramentas de IA para diagnóstico e refinamento de notação.

| # | Etapa | O que foi feito |
| -- | -- | -- |
| 1 | Delimitação | Separação dos domínios em Cadastro (aquisição) e Login (recorrência). |
| 2 | Percurso exploratório | Execução dos fluxos do início ao fim para mapear os caminhos felizes e alternativos (ex: login com senha vs. recuperação de acesso; cadastro nativo vs. conta já existente). |
| 3 | Inspeção de Rede/DOM | Análise do momento exato de envio de dados (ex: eventos `input` vs `focus_out`) e verificação de cookies. |
| 4 | Provocação de exceções | Inserção de senhas fracas, tentativas sucessivas de login para forçar o bloqueio de conta e testes de e-mails inválidos. |
| 5 | Modelagem Assistida | Estruturação das regras observadas em diagramas BPMN com apoio de IA para diagnóstico estrutural e refinamento visual. |

---

## 3. Recorte A — Cadastro de Usuário

Este recorte analisa o momento em que o usuário anônimo entra na base da plataforma. O foco da arquitetura observada é a redução drástica de fricção inicial (*Lazy Registration*).

### 3.1 Inventário de tela e DOM

| Estado | Elementos observados |
| -- | -- |
| **Formulário de Cadastro** | Cadastro nativo por formulário (nome, e-mail/celular, senha); campos divididos em múltiplas etapas (Wizard); ausência do campo de CPF/CNPJ no fluxo inicial. |
| **Validação de Senha** | Medidor de força de senha que atualiza dinamicamente a cada tecla digitada (evento `input`); sem necessidade de clicar em "avançar" para obter feedback. |
| **Verificação de E-mail** | Após o envio do formulário, a conta permanece em estado *pendente* até a confirmação de um código de verificação enviado por e-mail ou SMS. |

> *Nota de escopo: apesar de o login social (Google/Apple) ter sido idealizado nas discussões iniciais da equipe, ele **não foi contemplado na modelagem técnica do BPMN v3** e, portanto, não gera requisitos nesta entrega.*

### 3.2 Regras de negócio derivadas

| ID | Regra | Base |
| -- | -- | -- |
| RN-A01 | **Progressive Profiling:** O CPF não é exigido na criação da conta básica, sendo postergado para o momento do checkout com pagamento ou para a habilitação como vendedor. | Observado |
| RN-A02 | O medidor de força de senha é atualizado no *client-side* a cada caractere (feedback), mas a validação autoritativa de formato dos campos e da política de senha ocorre no servidor (gateway "Formato dos campos é válido?"). | DOM/Rede + BPMN |
| RN-A03 | **Verificação de E-mail Obrigatória:** O cadastro nativo cria a conta com status *pendente*; a ativação depende da validação de um código de verificação com **TTL de 10 minutos**, enviado por e-mail ou SMS, com reenvio limitado a um número máximo de tentativas. | BPMN (Raia Cadastro) |
| RN-A04 | O sistema verifica se o e-mail/telefone informado já está cadastrado antes de criar a conta (gateway "E-mail/telefone já cadastrado?"). | BPMN (Raia Cadastro) |

---

## 4. Recorte B — Login e Gestão de Sessão

Este recorte analisa como usuários existentes retornam à plataforma. A autenticação primária é feita por **credenciais (e-mail/usuário + senha)**, com consulta e comparação de hash no banco de dados; um segundo fator (2FA) é solicitado apenas quando a conta o tem habilitado.

### 4.1 Inventário de tela e DOM

| Estado | Elementos observados |
| -- | -- |
| **Identificação** | Tela de login solicitando "e-mail ou usuário" e "senha". |
| **Segundo Fator (2FA)** | Quando a conta tem 2FA habilitado, é solicitado um código OTP de 6 dígitos, enviado por SMS ou e-mail, com opção de reenvio. |
| **Bloqueio (Exceção)** | Após atingir o limite de tentativas falhas, a conta é marcada como bloqueada por 30 minutos e o usuário recebe uma notificação de bloqueio. |

### 4.2 Regras de negócio derivadas

| ID | Regra | Base |
| -- | -- | -- |
| RN-B01 | **Autenticação por Credenciais:** O login primário exige e-mail/usuário + senha; o sistema consulta a credencial no banco de dados e compara o hash da senha. Não existe login *passwordless*. | BPMN (Raia Autenticação) |
| RN-B02 | **2FA Opt-in:** O segundo fator (OTP de 6 dígitos, **TTL de 3 minutos**) é exigido somente quando a conta possui a flag "2FA habilitada" — é uma configuração da conta (opt-in), não há motor de risco adaptativo. | BPMN (Raia Autenticação) |
| RN-B03 | **Rate Limiting e Bloqueio:** A cada falha, o sistema incrementa um contador de tentativas mantido na sessão; ao atingir o limite configurado, marca a conta como bloqueada por **30 minutos** e envia notificação de bloqueio ao usuário. Não há CAPTCHA. | BPMN (Raia Autenticação/Segurança) |
| RN-B04 | **Ofuscação de Erros:** O sistema retorna um erro genérico de autenticação, sem confirmar se o identificador está ou não cadastrado, evitando enumeração de usuários. | Provocação |
| RN-B05 | **Redefinição de Senha:** O token de redefinição possui **TTL de 15 minutos** e é enviado por e-mail; a nova senha só é aceita mediante token válido e não expirado. | BPMN (Raia Segurança) |
| RN-B06 | A sessão autenticada é materializada por um token de sessão (JWT) que dispensa a reautenticação em retornos futuros enquanto permanecer válido. | BPMN (Raia Autenticação) |

---

## 5. Recorte C — Modelagem do Processo (BPMN)

Para transpor os achados dos Recortes A e B para um formato padronizado de processos de negócio, foi realizado um trabalho de modelagem profunda, apoiado por inteligência artificial, estruturado em três fases fundamentais:

1. **Diagnóstico Estrutural:** A análise inicial identificou que rascunhos prévios reaproveitavam, por engano, templates genéricos de processos de compra (*Order Fulfillment*), sem relação com o fluxo real de identidades. Foram mapeados erros de notação, como gateways mal colocados e ausência de conteúdo nas raias (*lanes*) planejadas.
2. **Engenharia Reversa Comportamental:** Como não existe uma especificação pública detalhada, a lógica do processo foi reconstruída puramente a partir da observação prática (Recortes A e B). Foram modelados os fluxos de verificação de e-mail e celular, autenticação em duas etapas (2FA), bloqueio por tentativas excedidas (*rate limiting*) e recuperação de acesso. 
3. **Construção e Refinamento Visual:** A aplicação estrita da notação BPMN oficial (pools, raias, gateways exclusivos tipo XOR, eventos de início/fim). Após uma primeira versão com excesso de poluição visual, o layout foi reorganizado, reduzindo o cruzamento de conectores e alinhando as etapas em colunas lógicas, inserindo pontos de interface para tornar a leitura clara.

> *Nota metodológica: Todo o processo de decisão sobre quais regras de negócio modelar e como as etapas se encadeiam partiu da análise humana, com a IA atuando estritamente como ferramenta de apoio ao diagnóstico técnico e refinamento da notação visual.*

---

## 6. Fluxos de Navegação (Estados Básicos)

O comportamento detalhado no BPMN v3 organiza-se em uma pool do usuário e três raias do sistema (**Autenticação**, **Segurança** e **Cadastro**):

**Fluxo de Login por Credenciais (Raia Autenticação):**

1. O usuário informa e-mail/usuário e senha.
2. O sistema consulta a credencial no banco e compara o hash da senha.
   - **Hash não confere:** incrementa o contador de tentativas na sessão. Se o contador atingir o limite configurado, a conta é bloqueada por 30 minutos e o usuário é notificado; caso contrário, retorna erro genérico de autenticação.
   - **Hash confere:** avalia se a conta tem 2FA habilitado.
     - **Sem 2FA:** gera o token de sessão (JWT) → *Fim: sessão autenticada*.
     - **Com 2FA:** gera um OTP de 6 dígitos (TTL de 3 minutos), enviado por SMS ou e-mail. Se o OTP for válido e estiver dentro do TTL, gera o token de sessão (JWT); se for inválido ou expirado, permite reenvio limitado a um número máximo de tentativas.

**Fluxo de Cadastro (Raia Cadastro):**

1. O usuário preenche o formulário nativo (nome, e-mail/celular, senha).
2. O sistema valida o formato dos campos; se válido, verifica se o e-mail/telefone já está cadastrado.
3. Não havendo conta prévia, gera o hash da senha e cria a conta com status *pendente*.
4. Envia um código de verificação (TTL de 10 minutos); com código válido dentro do prazo, atualiza o status da conta para *ativa* (*Fim: cadastro concluído*); caso contrário, permite reenvio limitado.

**Fluxo de Recuperação de Acesso (Raia Segurança):**

1. O usuário aciona "Esqueci minha senha".
2. O sistema gera um token de redefinição (TTL de 15 minutos) e o envia por e-mail.
3. Ao receber a nova senha, valida se o token é válido e não expirou; se sim, gera o novo hash e atualiza a senha no banco.

![alt text](image.png)

## 7. O que só aparece juntando as frentes

Lidos isoladamente, os SIGs mostram decisões arquiteturais isoladas e o BPMN mostra apenas os passos de um processo. Lidos em conjunto, revela-se a verdadeira estratégia do sistema:

**A conversão governa o design:** O modelo de processos (BPMN) prevê verificação em duas etapas (2FA) e bloqueio de conta, mas a análise de interface e rede (SIG) revela que a plataforma faz de tudo para que o usuário não caia nesses fluxos a menos que seja estritamente necessário. O 2FA opcional por conta (ver RN-B02) e o Progressive Profiling (RN-A01) comprovam que o sistema absorve o risco inicial de fraude para maximizar a entrada de usuários, empurrando as complexidades processuais para etapas posteriores (ex.: exigência de CPF no checkout).

---

## 8. Rastreabilidade

| Achado | Vai para | Papel |
| :--- | :--- | :--- |
| Contador de tentativas na sessão, bloqueio de conta e 2FA opt-in | BPMN | Define os gateways de decisão e laços de repetição (XOR) |
| Eventos de Input e Validação Contínua | NFR Framework | Origina a operacionalização de 'Facilidade de Aprendizado' no SIG de Cadastro |
| Sessão via token (JWT) e login por credenciais | NFR Framework | Origina as operacionalizações de eficiência e disponibilidade no SIG de Login |

---

## 9. Limites do levantamento

* **Antifraude fora do escopo do modelo:** O BPMN v3 não modela CAPTCHA nem motor de risco adaptativo; o único mecanismo de contenção representado é o contador de tentativas na sessão seguido do bloqueio temporário da conta. Eventuais análises comportamentais antifraude que a plataforma real execute no backend não são inspecionáveis via DOM e não foram incorporadas ao processo.
* **Limitações de Caixa-Preta:** As atividades mapeadas no BPMN como "Consulta credencial no banco de dados" e "Gera hash e atualiza senha no banco" representam caixas pretas lógicas; a arquitetura exata de microsserviços por trás dessas validações é uma aproximação baseada em padrões de mercado.
* **Escopo do BPMN v3:** O modelo cobre cadastro, login por credenciais, 2FA opt-in e recuperação de acesso. Encerramento de sessão (*logout*), reautenticação para operações sensíveis (*step-up*) e login social não estão no diagrama e, por isso, não são tratados como requisitos nesta entrega.

---

## 10. Requisitos Funcionais (Revisitados)

Esta seção consolida em requisitos funcionais (RF) as funcionalidades **efetivamente modeladas no BPMN v3**, que é a fonte de verdade da entrega. As declarações seguem a estrutura *"O sistema deve..."* / *"O [ator] deve ser capaz de..."*, com atores identificados e redação testável e independente. Os ajustes feitos para alinhar o texto ao diagrama estão descritos em 10.7.

### 10.1 Atores

| Ator | Descrição |
| :--- | :--- |
| **Usuário Não Autenticado** | Visitante anônimo, sem conta ou sem sessão ativa. |
| **Cliente** | Usuário autenticado que utiliza a plataforma para comprar. |
| **Vendedor** | Usuário autenticado habilitado a anunciar e vender. |
| **Sistema** | Plataforma de IAM e seus serviços de verificação, sessão e bloqueio. |

### 10.2 Cadastro e Perfil

| ID | Requisito Funcional | Ator | Base |
| :--- | :--- | :--- | :--- |
| RF01 | O Usuário Não Autenticado deve ser capaz de criar uma conta preenchendo um formulário nativo com nome, e-mail ou celular e senha. | Usuário Não Autenticado | BPMN (Raia Cadastro) / RN-A03 |
| RF02 | O sistema deve apresentar o formulário de cadastro em múltiplas etapas (wizard), solicitando em cada etapa apenas o subconjunto mínimo de dados necessário para avançar. | Sistema | 3.1 |
| RF03 | O sistema não deve exigir CPF/CNPJ para a criação da conta básica. | Sistema | RN-A01 |
| RF04 | O sistema deve solicitar e validar o CPF/CNPJ apenas quando o Cliente iniciar um checkout com pagamento ou quando o usuário solicitar habilitação como Vendedor (*Progressive Profiling*), bloqueando a conclusão dessas operações até o preenchimento. | Cliente / Vendedor | RN-A01 |
| RF05 | Durante a definição da senha, o sistema deve exibir um medidor de força atualizado dinamicamente a cada caractere digitado (evento `input`), sem exigir a submissão do formulário. | Sistema | RN-A02 / 3.1 |
| RF06 | Ao receber o formulário, o sistema deve validar no servidor o formato dos campos e a política de senha (gateway "Formato dos campos é válido?"), recusando o cadastro quando os critérios não forem atendidos. | Sistema | RN-A02 / BPMN |
| RF07 | O sistema deve verificar se o e-mail ou telefone informado já está cadastrado antes de criar a conta (gateway "E-mail/telefone já cadastrado?"). | Sistema | RN-A04 / BPMN |
| RF08 | Não havendo conta prévia, o sistema deve gerar o hash da senha e criar a conta com status *pendente*. | Sistema | RN-A03 / BPMN |
| RF09 | O sistema deve enviar um código de verificação com **TTL de 10 minutos** por e-mail ou SMS e ativar a conta (status *ativa*) somente após a validação correta do código dentro do prazo. | Sistema | RN-A03 / BPMN |
| RF10 | Quando o código de verificação for inválido ou estiver expirado, o sistema deve permitir o reenvio, limitado a um número máximo de tentativas. | Sistema | RN-A03 / BPMN |

### 10.3 Autenticação e Login

| ID | Requisito Funcional | Ator | Base |
| :--- | :--- | :--- | :--- |
| RF11 | A tela de login deve solicitar e-mail ou usuário e a respectiva senha. | Usuário Não Autenticado | RN-B01 / BPMN |
| RF12 | O sistema deve autenticar o usuário consultando a credencial no banco de dados e comparando o hash da senha informada; quando o hash não confere, deve retornar um erro genérico de autenticação. | Sistema | RN-B01 / RN-B04 / BPMN |
| RF13 | Quando o hash confere e a conta possui a opção de 2FA habilitada (opt-in), o sistema deve gerar um OTP de 6 dígitos com **TTL de 3 minutos**, enviado por SMS ou e-mail, e concluir o login somente após a validação do OTP dentro do prazo. Contas sem 2FA habilitado seguem direto para a emissão da sessão. | Sistema | RN-B02 / BPMN |
| RF14 | Quando o OTP de 2FA for inválido ou estiver expirado, o sistema deve permitir o reenvio, limitado a um número máximo de tentativas, sem oferecer troca dinâmica de canal. | Usuário Não Autenticado | RN-B02 / BPMN |
| RF15 | O sistema deve restringir o envio de códigos (verificação de cadastro e OTP de 2FA) aos canais SMS e e-mail. | Sistema | RN-A03 / RN-B02 |

### 10.4 Rate Limiting e Bloqueio de Conta

| ID | Requisito Funcional | Ator | Base |
| :--- | :--- | :--- | :--- |
| RF16 | A cada falha de autenticação, o sistema deve incrementar um contador de tentativas mantido na sessão. | Sistema | RN-B03 / BPMN |
| RF17 | Ao atingir o limite configurado de tentativas, o sistema deve marcar a conta como bloqueada por **30 minutos** e enviar uma notificação de bloqueio ao usuário. | Sistema | RN-B03 / BPMN |
| RF18 | O sistema deve retornar mensagens de erro genéricas nas falhas de cadastro e de autenticação, sem revelar se um identificador está ou não cadastrado (prevenção de enumeração de usuários). | Sistema | RN-B04 |

### 10.5 Recuperação de Acesso

| ID | Requisito Funcional | Ator | Base |
| :--- | :--- | :--- | :--- |
| RF19 | O Usuário Não Autenticado deve ser capaz de acionar a redefinição de senha ("Esqueci minha senha"); o sistema deve gerar um token de redefinição com **TTL de 15 minutos** e enviá-lo por e-mail. | Usuário Não Autenticado | RN-B05 / BPMN |
| RF20 | Ao receber a nova senha, o sistema deve validar se o token de redefinição é válido e não está expirado; sendo válido, deve gerar o novo hash e atualizar a senha no banco de dados. | Sistema | RN-B05 / BPMN |

### 10.6 Gestão de Sessão

| ID | Requisito Funcional | Ator | Base |
| :--- | :--- | :--- | :--- |
| RF21 | Após a autenticação bem-sucedida (e a validação do 2FA, quando aplicável), o sistema deve emitir um token de sessão (JWT) que dispensa a reautenticação em retornos futuros enquanto permanecer válido. | Sistema | RN-B06 / BPMN |

### 10.7 Ajustes de fidelidade ao BPMN v3

Durante a auditoria, o texto original foi confrontado com o BPMN v3 e as extrapolações abaixo foram corrigidas:

1. **Fim do "passwordless-first".** O texto descrevia o OTP como método primário de login e a senha como alternativa. O BPMN modela o oposto: identificação por e-mail/usuário **+ senha**, com "Consulta credencial no banco de dados" e comparação de hash. Reescritos RN-B01, a seção 6 e os requisitos de login (RF11–RF12).
2. **2FA por configuração, não por risco.** O 2FA deixou de ser descrito como decisão de "motor de risco adaptativo" e passou a refletir o gateway "Conta com 2FA habilitada?" — uma opção da conta (opt-in). Ajustados RN-B02, RF13 e RF14.
3. **Remoção do CAPTCHA.** O BPMN não possui CAPTCHA. A resposta ao excesso de tentativas foi unificada em: contador na sessão → bloqueio da conta por 30 minutos → notificação ao usuário (RN-B03, RF16, RF17). Removidos os antigos RF sobre CAPTCHA e sobre "motor de risco/reCAPTCHA invisível".
4. **Canais restritos a SMS e e-mail.** Removidas as menções ao canal WhatsApp e à alternância dinâmica de canais ("Despacho Multicanal"). O reenvio limitado permanece como único recurso (RF10, RF14, RF15).
5. **Remoção do OAuth / login social.** O BPMN prevê apenas cadastro nativo por formulário. Removidos os RF de criação de conta e verificação por OAuth; o assunto foi rebaixado a uma nota de escopo na seção 3.1.
6. **Enriquecimento com dados do diagrama.** Incorporados os TTLs (OTP 3 min, código de verificação 10 min, token de redefinição 15 min), a duração do bloqueio (30 min) com notificação explícita, o status *pendente* da conta recém-criada e o contador de tentativas mantido "na sessão".
7. **Escopo enxugado.** *Logout* manual e reautenticação (*step-up*) para operações sensíveis não estão no BPMN v3 e foram removidos da lista de requisitos, ficando registrados como limite do levantamento na seção 9.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 27/08/2026 | Estruturação inicial do documento de Engenharia Reversa e integração da modelagem BPMN | Pedro Henrique Gomes| José Joaquim da Silva Neto |
| 1.1 | 28/08/2026 | Extração e padronização dos Requisitos Funcionais (seção 10) a partir da engenharia reversa, com correção de incongruências do texto original | Júlia Santana Campos, João Paulo Barbosa Pereira Nunes e Pedro Henrique Gomes| José Joaquim da Silva Neto |
| 1.2 | 28/08/2026 | Refatoração de fidelidade ao BPMN v3: login por credenciais + 2FA opt-in, remoção de passwordless/CAPTCHA/OAuth/WhatsApp, inclusão dos TTLs e estados do diagrama e renumeração dos RF | Júlia Santana Campos | José Joaquim da Silva Neto |