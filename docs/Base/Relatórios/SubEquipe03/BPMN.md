# Modelagem BPMN


<iframe
  width="100%"
  height="600"
  src="https://miro.com/welcomeonboard/MkRtVElRSE5UM2wxNk10NFk5MVV3TDlqbGp0Mno1ZE9UMGNGUzR6bVk2WkU4TlZOZDREWkl6bGtmb0VGNnh0YTFMWkgwSzI1SDRHRENUZWVTOEJhNXEvR1BFYTNIOUJWejBpUFFnbjdIaHd6cmRmVFl3dVhoVnRUdHJqQWxRMnNnbHpza3F6REdEcmNpNEFOMmJXWXBBPT0hdjE=?share_link_id=683326639749"
  frameborder="0"
  scrolling="no"
  allowfullscreen>
</iframe>


## 1. Objetivo do Documento

Este relatório descreve e analisa o diagrama BPMN referente ao processo de **Login, Cadastro, Autenticação em Duas Etapas (2FA) e Recuperação de Senha** da plataforma Mercado Livre, produzido pela subequipe 3 como artefato de modelagem de processos de negócio no âmbito da engenharia de requisitos.

## 2. Visão Geral do Processo

O diagrama modela o ponto de entrada de um usuário no sistema, cobrindo três macro-fluxos que partem de uma decisão inicial:

- **Login** (usuário já possui conta), incluindo o tratamento de credenciais inválidas, bloqueio por tentativas excedidas e autenticação de dois fatores (2FA);
- **Cadastro** (usuário não possui conta), incluindo validação de dados, criação de conta em status pendente e verificação por código;
- **Recuperação de senha**, acionada a partir da tela de login quando o usuário esquece a senha.

O processo é disparado por um evento de início (círculo verde) e possui múltiplos eventos de fim (círculos vermelhos), representando os diferentes desfechos possíveis: **acesso concedido**, **acesso bloqueado** e **cadastro concluído**.

## 3. Raias (Lanes) e Responsabilidades

O diagrama está organizado em raias (pools/lanes) que separam claramente as responsabilidades entre os elementos do sistema:

| Raia | Responsabilidade |
|---|---|
| **(Cliente/Ator)** | Interações do usuário: informar credenciais, preencher formulário, informar códigos recebidos, definir nova senha. |
| **Interface** | Exibição de telas e mensagens ao usuário (tela de login/cadastro, mensagens de erro, opções de reenvio de código). |
| **Autenticação** | Regras de validação de credenciais, controle de tentativas, verificação de 2FA. |
| **Segurança** | Geração de tokens/códigos, bloqueio temporário de conta, atualização de senha. |
| **Cadastro** | Validação de dados de cadastro, criação da conta, ativação da conta. |

Essa separação em raias evidencia uma arquitetura conceitual em camadas, na qual a Interface apenas exibe/coleta dados, enquanto as regras de negócio ficam concentradas nas raias de Autenticação, Segurança e Cadastro — um bom indício de separação de responsabilidades (útil, inclusive, para derivar requisitos não funcionais de segurança).

## 4. Descrição Detalhada dos Fluxos

### 4.1 Decisão Inicial
O processo começa com o evento de início e a pergunta de gateway **"Possui conta?"**:
- **Sim** → segue para o fluxo de **Login**;
- **Não** → segue para o fluxo de **Cadastro**.

### 4.2 Fluxo de Login
1. Usuário informa e-mail/celular e senha.
2. Gateway **"Credenciais válidas?"**:
   - **Inválidas** → incrementa o contador de tentativas → gateway **"Excedeu limite de tentativas?"**
     - **Sim** → sistema **bloqueia a conta temporariamente** → **Fim: acesso bloqueado**;
     - **Não** → exibe mensagem de credenciais inválidas → retorna à tela de login.
   - **Válidas** → gateway **"2FA habilitado?"**
     - **Não** → **concede acesso ao usuário** → **Fim: acesso concedido**;
     - **Sim** → gera código de verificação 2FA → envia o código → sistema solicita o código ao usuário → usuário informa o código → gateway **"Código 2FA válido?"**
       - **Válido** → concede acesso → **Fim: acesso concedido**;
       - **Inválido** → exibe opção de reenviar código 2FA → repete a verificação.

### 4.3 Fluxo de Recuperação de Senha
Acionado a partir da tela de login:
1. Usuário solicita recuperação de senha.
2. Sistema gera token de redefinição de senha e envia link de redefinição.
3. Usuário acessa o link, define nova senha.
4. Sistema atualiza a senha e retorna o usuário para a tela de login.

### 4.4 Fluxo de Cadastro
1. Usuário preenche o formulário de cadastro.
2. Gateway **"Dados válidos e disponíveis?"**:
   - **Válidos** → cria conta em **status pendente** → gera código de verificação de conta → envia código → sistema solicita o código → usuário informa o código de verificação → gateway **"Código de verificação válido?"**
     - **Válido** → **ativa a conta do usuário** → **Fim: cadastro concluído**;
     - **Inválido** → exibe opção de reenviar código de cadastro → repete a verificação.
   - **Inválidos** → (fluxo retorna para correção dos dados no formulário).

## 5. Eventos de Fim Identificados

| Evento | Condição de disparo |
|---|---|
| Fim: acesso concedido | Login bem-sucedido (com ou sem 2FA) |
| Fim: acesso bloqueado | Excesso de tentativas de login inválidas |
| Fim: cadastro concluído | Conta criada e verificada com sucesso |

## 6. Observações e Pontos de Atenção

- **Controle de tentativas de login**: o modelo já prevê um mecanismo de bloqueio temporário por excesso de tentativas, o que é positivo do ponto de vista de segurança, mas o diagrama não explicita o **tempo de bloqueio** nem a **quantidade máxima de tentativas** — pontos que devem ser detalhados em requisitos funcionais/regras de negócio complementares.
- **2FA condicional**: a verificação em duas etapas só ocorre se estiver habilitada para a conta, sugerindo que essa é uma configuração opcional do usuário (não obrigatória por padrão).
- **Reenvio de código**: tanto no fluxo de 2FA quanto no de cadastro há a opção de reenviar o código em caso de valor inválido, mas o diagrama não define um **limite de reenvios**, o que pode ser um ponto a esclarecer com os stakeholders.
- **Status pendente no cadastro**: a conta é criada com status "pendente" antes da verificação, e só é ativada após a confirmação do código — modelagem alinhada com boas práticas de cadastro seguro (evita contas fantasmas/ativas sem verificação de contato).
- **Reutilização de componentes de mensageria**: os elementos "Envia link de redefinição de senha", "Envia código de verificação 2FA", "Envia notificação de bloqueio" e "Envia código de verificação de cadastro" parecem compor um subprocesso ou serviço comum de notificação, o que pode indicar uma oportunidade de modelar um componente de envio de mensagens reutilizável no BPMN ou na arquitetura do sistema.
- **Rastreabilidade com o NRF Framework**: os pontos de bloqueio, expiração de token e reenvio de código são bons candidatos a se conectar com requisitos não funcionais de segurança e usabilidade já levantados no NRF Framework do projeto.

## 7. Conclusão

O diagrama representa de forma consistente o fluxo unificado de **login, cadastro, 2FA e recuperação de senha** do Mercado Livre, com boa separação de responsabilidades entre interface, autenticação, segurança e cadastro. Os principais desfechos do processo (acesso concedido, acesso bloqueado, cadastro concluído) estão claramente mapeados. Recomenda-se complementar o modelo com anotações textuais (ou um documento de regras de negócio) detalhando limites numéricos (tentativas, tempo de bloqueio, validade de código/token) que hoje não são visíveis apenas no diagrama.


## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Modelagem do BPMN | João Paulo Barbosa Pereira Nunes e Júlia Santana Campos | José Joaquim da Silva Neto e Pedro Henrique Gomes |
| 1.2 | 27/08/2026 | Adiciona BPMN | José Joaquim da Silva Neto | Pedro Henrique Gomes |
