# Modelagem BPMN


<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVHtT2bao=/?embedMode=view_only_without_ui&moveToViewport=381,-46,3450,1885&embedId=952961417771" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>


## 1. Objetivo do Documento

Este relatório descreve e analisa o diagrama BPMN referente ao processo de Login, Cadastro, Autenticação em Duas Etapas (2FA) e Recuperação de Senha da plataforma Mercado Livre, produzido pela subequipe 3 como artefato de modelagem de processos de negócio no âmbito da engenharia de requisitos.

Esta versão do relatório (v3) reflete a reformulação do diagrama realizada em 28/08/2026, que corrigiu dois pontos identificados em revisão: a existência de uma raia de "Interface" que não representa um ator ou processo real, e o nível de abstração das atividades, que estava genérico demais (descrevia telas, não regras de negócio).

## 2. Visão Geral do Processo

O diagrama modela o ponto de entrada de um usuário no sistema, cobrindo três macro fluxos que partem de uma decisão inicial:

- Login (usuário já possui conta), incluindo o tratamento de credenciais inválidas, bloqueio por tentativas excedidas e autenticação de dois fatores (2FA);
- Cadastro (usuário não possui conta), incluindo validação de dados, criação de conta em status pendente e verificação por código;
- Recuperação de senha, acionada a partir da tela de login quando o usuário esquece a senha.

O processo é disparado por um evento de início (círculo verde) e possui múltiplos eventos de fim (círculos vermelhos), representando os diferentes desfechos possíveis: acesso concedido, acesso bloqueado e cadastro concluído.

## 3. Raias (Lanes) e Responsabilidades

A raia de "Interface" presente na versão anterior do diagrama foi removida. Interface não é um ator nem um processo que executa atividades, é o meio pelo qual o usuário interage com o sistema. As interações de tela (exibir formulário, solicitar um código, mostrar mensagem de erro) hoje são representadas implicitamente pelos fluxos de mensagem entre o pool Usuário e a raia do backend responsável por aquela regra, e não mais como atividades isoladas em uma raia própria.

O diagrama está organizado em um pool Usuário, um pool Mercado Livre com três raias, e um pool Provedor de Email/SMS:

| Raia/Pool | Responsabilidade |
|---|---|
| Usuário | Interações do usuário: informar credenciais, preencher formulário, clicar em "esqueci minha senha", informar códigos recebidos, submeter nova senha. |
| Autenticação | Consulta e comparação de hash de credencial, controle de contador de tentativas, verificação de 2FA (geração e validação de OTP), emissão de token de sessão (JWT). |
| Segurança | Bloqueio temporário de conta, geração de token de redefinição de senha, validação do token e atualização do hash de senha no banco. |
| Cadastro | Validação de formato e de duplicidade de email/celular, geração de hash de senha, criação de conta em status pendente, geração e validação de código de verificação, ativação da conta. |
| Provedor de Email/SMS | Envio de OTP, link de redefinição de senha, notificação de bloqueio e código de verificação de cadastro. |

Essa separação evidencia uma arquitetura conceitual em camadas, na qual as regras de negócio ficam concentradas nas raias de Autenticação, Segurança e Cadastro, cada uma tratando exclusivamente da lógica que lhe compete, sem misturar responsabilidade de apresentação com regra de negócio.

## 4. Descrição Detalhada dos Fluxos

### 4.1 Decisão Inicial
O processo começa com o evento de início e a pergunta de gateway "Possui conta cadastrada?":
- Sim → segue para o fluxo de Login;
- Não → segue para o fluxo de Cadastro.

### 4.2 Fluxo de Login
1. Usuário informa email/celular e senha.
2. Autenticação consulta a credencial no banco de dados e compara o hash da senha informada. Gateway "Hash da senha confere?":
   - Não confere → incrementa o contador de tentativas na sessão → gateway "Contador maior ou igual ao limite configurado?"
     - Sim → Segurança marca a conta como bloqueada (TTL de 30 minutos) → Fim: acesso bloqueado;
     - Não → retorna erro de autenticação (401) e o usuário tenta novamente.
   - Confere → gateway "Conta com 2FA habilitado?"
     - Não → gera token de sessão (JWT) → Fim: sessão autenticada;
     - Sim → gera OTP de 6 dígitos (TTL de 5 minutos) → envia o OTP via Provedor → usuário informa o código recebido → gateway "OTP confere e dentro do TTL?"
       - Válido → gera token de sessão (JWT) → Fim: sessão autenticada;
       - Inválido/expirado → permite reenvio (máximo de 3 tentativas) e repete a geração do OTP.

### 4.3 Fluxo de Recuperação de Senha
Acionado a partir da tela de login:
1. Usuário clica em "Esqueci minha senha".
2. Segurança recebe a solicitação e gera um token de redefinição único (TTL de 15 minutos), enviado ao usuário via Provedor.
3. Usuário submete a nova senha.
4. Gateway "Token válido e não expirado?":
   - Válido → Segurança gera novo hash e atualiza a senha no banco → usuário retorna à tela de login;
   - Expirado/inválido → usuário é informado e pode solicitar um novo link.

### 4.4 Fluxo de Cadastro
1. Usuário preenche o formulário (nome, email/celular, senha).
2. Gateway "Formato dos campos é válido?":
   - Inválido → usuário corrige os dados no formulário;
   - Válido → gateway "Email/celular já cadastrado?"
     - Já existe → usuário é informado e pode tentar login ou recuperação de senha;
     - Não existe → Cadastro gera o hash da senha e cria a conta em status pendente → gera código de verificação (TTL de 10 minutos) → envia o código via Provedor → usuário informa o código recebido → gateway "Código confere e dentro do TTL?"
       - Válido → atualiza o status da conta para ativa → Fim: cadastro concluído;
       - Inválido/expirado → permite reenvio (máximo de 3 tentativas) e repete a geração do código.

## 5. Eventos de Fim Identificados

| Evento | Condição de disparo |
|---|---|
| Fim: sessão autenticada | Login bem sucedido (com ou sem 2FA) |
| Fim: acesso bloqueado | Excesso de tentativas de login inválidas |
| Fim: cadastro concluído | Conta criada e verificada com sucesso |

## 6. Observações e Pontos de Atenção

- Limites numéricos explicitados: diferente da versão anterior, este diagrama já especifica os valores de TTL e limite de tentativas diretamente nas atividades (OTP: 5 minutos; token de redefinição: 15 minutos; bloqueio de conta: 30 minutos; código de verificação de cadastro: 10 minutos; reenvio de OTP e de código de verificação: máximo de 3 tentativas). Esses valores são hipóteses de modelagem obtidas por engenharia reversa e devem ser validados com os stakeholders antes de serem tratados como regra de negócio definitiva.
- 2FA condicional: a verificação em duas etapas só ocorre se estiver habilitada para a conta, sugerindo que essa é uma configuração opcional do usuário, não obrigatória por padrão.
- Status pendente no cadastro: a conta é criada com status pendente antes da verificação, e só é ativada após a confirmação do código, modelagem alinhada com boas práticas de cadastro seguro (evita contas ativas sem verificação de contato).
- Reutilização do Provedor de Email/SMS: os quatro pontos de envio (OTP, link de redefinição, notificação de bloqueio, código de verificação de cadastro) continuam modelados como um único pool externo, reforçando a leitura de que se trata de um serviço de mensageria compartilhado entre as raias de Autenticação, Segurança e Cadastro.
- Rastreabilidade com o NRF Framework: os pontos de bloqueio, expiração de token e reenvio de código são bons candidatos a se conectar com requisitos não funcionais de segurança e usabilidade já levantados no NRF Framework do projeto.
- Organização visual: o diagrama foi reorganizado em colunas alinhadas por etapa do processo, com um corredor dedicado para as mensagens de maior distância entre o Provedor e o Usuário, para evitar que essas linhas cruzassem por cima de gateways de outras raias.

## 7. Conclusão

O diagrama representa de forma consistente o fluxo unificado de login, cadastro, 2FA e recuperação de senha do Mercado Livre, agora em um nível de abstração mais próximo da implementação real (consulta a banco de dados, geração de hash e de token de sessão, TTLs explícitos) e sem a raia de Interface, que não correspondia a um ator do processo. Os principais desfechos do processo (sessão autenticada, acesso bloqueado, cadastro concluído) continuam claramente mapeados. Os valores numéricos incluídos nesta versão (TTLs e limites de tentativa) foram obtidos por engenharia reversa do comportamento observado na plataforma e devem ser validados formalmente com os stakeholders.

## 8. Ferramentas Utilizadas

Esta seção descreve as ferramentas empregadas na construção e documentação deste artefato, da concepção inicial até a versão final.

| Ferramenta | Uso no processo |
| Mermaid.js | Rascunho inicial do fluxo corrigido de Login/Cadastro, em formato de código (flowchart), usado como referência textual antes da modelagem gráfica definitiva. |
| Miro (via API) |	Ferramenta principal de modelagem gráfica. O diagrama foi construído diretamente no board (pools, raias, gateways exclusivos com marcador X, eventos de início/fim, fluxos de sequência e de mensagem), passando por três versões até a atual (v3). | 
| Material de referência da disciplina | PDF de apoio da Profa. Milene Serrano (Notação BPMN), usado como base normativa para aplicar corretamente pool, raia, gateway exclusivo e a distinção entre fluxo de sequência e fluxo de mensagem. | 
| GitHub Pages + Markdown	| Publicação da documentação do processo (este relatório, o documento de engenharia reversa e o de uso de IA generativa), com elos de rastreabilidade entre as decisões do diagrama e as reuniões/metodologia do projeto.|

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Modelagem do BPMN | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.2 | 27/08/2026 | Adiciona BPMN | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.3 | 28/08/2026 | Remoção da raia de Interface, redução do nível de abstração das atividades e explicitação de TTLs/limites de tentativa | João Paulo Barbosa Pereira Nunes | Julia Santana Campos |