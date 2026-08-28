# Léxico Ampliado da Linguagem (LAL) — Domínio Mercado Livre

> Técnica de Léxico Ampliado da Linguagem, aplicada ao domínio de comércio eletrônico do Mercado Livre. Cada símbolo é definido por uma **Noção** (denotação, sem julgamento) e um **Impacto** (conotação, consequências/ações no universo de discurso).

Este documento de Domínio Léxico do objeto de estudo Mercado Livre foi desenvolvido na fase entender da [Design Sprint](/Base/Relatórios/SubEquipe03/DesignSprint.md#fase-entender-240826), a partir do [Brainstorming](/Base/Relatórios/SubEquipe03/DesignSprint.md#brainstorming), servindo como base padronizada de vocabulário para a construção do *Rich Picture*, do *BPMN* de Login/Cadastro e dos SIGs do *NFR Framework*.

## Sumário

- [Atores](#atores)
- [Objetos do Domínio](#objetos-do-domínio)
- [Processos e Estados](#processos-e-estados)
- [Serviços da Plataforma](#serviços-da-plataforma)
- [Pós-venda e Conflitos](#pós-venda-e-conflitos)

---

## Atores

### 1. Usuário (Comprador)

| Campo | Descrição |
|---|---|
| **Noção** | Usuário da plataforma que busca, seleciona e adquire produtos. No **Rich Picture**, é o ator central que percorre tanto o fluxo de sucesso quanto o de insatisfação. |
| **Impacto** | 1. Passa obrigatoriamente pela "porta de entrada" (disparando o fluxo de **Login** ou **Cadastro** no **BPMN**) antes de comprar.<br>2. Segue o fluxo das *setas verdes* (Compra e Pagamento) no **Rich Picture**.<br>3. Expressa insatisfação (*ícone de polegar para baixo*) e aciona o fluxo das *setas vermelhas* caso o produto chegue errado/estragado. |

### 2. Vendedor

| Campo | Descrição |
|---|---|
| **Noção** | Usuário, pessoa física ou jurídica, que cadastra Anúncios de Produtos para comercialização na plataforma. |
| **Impacto** | 1. Recebe o pagamento (fluxo verde) e despacha o produto.<br>2. Interage com o Mediador (Balança) para responder a Devoluções ou disputas caso o produto chegue com defeito. |

### 3. Mediador (Aplicação / Balança)

| Campo | Descrição |
|---|---|
| **Noção** | Representação do sistema do Mercado Livre no **Rich Picture** (simbolizado pela balança), que atua garantindo o equilíbrio e a segurança entre Usuário e Vendedor. |
| **Impacto** | 1. Exige identificação prévia (Login/Cadastro) para garantir rastreabilidade.<br>2. Arbitra o fluxo de Devolução (setas vermelhas) garantindo o estorno via Instituição Financeira. |

### 4. Instituição Financeira

| Campo | Descrição |
|---|---|
| **Noção** | Entidade bancária ou de processamento (incluindo o Mercado Pago) responsável por gerenciar a transação monetária. |
| **Impacto** | 1. Efetiva a cobrança no fluxo de compra (setas verdes).<br>2. Realiza o estorno do valor no fluxo de devolução (setas vermelhas) sob comando do Mediador. |

### 5. Transportadora

| Campo | Descrição |
|---|---|
| **Noção** | Parceiro logístico (incluindo Mercado Envios) responsável pela movimentação física do produto entre o Vendedor e o Usuário. |
| **Impacto** | 1. Realiza a entrega do produto.<br>2. Executa a logística reversa quando o Usuário aciona a devolução de um produto estragado. |

---

## Objetos do Domínio

### 6. Anúncio

| Campo | Descrição |
|---|---|
| **Noção** | Publicação criada pelo Vendedor descrevendo um Produto disponível para venda, contendo preço e condições de Frete. |
| **Impacto** | 1. Fica visível para busca de Usuários.<br>2. Recebe Avaliações após vendas concluídas. |

### 7. Produto

| Campo | Descrição |
|---|---|
| **Noção** | Item físico ou digital ofertado em um Anúncio. |
| **Impacto** | 1. É o objeto transportado pelas Transportadoras.<br>2. Se "chega errado/estragado", é o gatilho que converte o fluxo do **Rich Picture** de verde (sucesso) para vermelho (devolução). |

---

## Processos e Estados

### 8. Compra e Pagamento (Fluxo Verde)

| Campo | Descrição |
|---|---|
| **Noção** | Caminho feliz do usuário na plataforma, representado pelas setas verdes no **Rich Picture**, que engloba a escolha do produto e a transação aprovada. |
| **Impacto** | 1. Depende da aprovação da Instituição Financeira.<br>2. Exige sessão válida gerada pelo **Módulo de Autenticação** (rastreável no **BPMN** e **NFR**). |

### 9. Acesso Inicial / Autenticação

| Campo | Descrição |
|---|---|
| **Noção** | Barreira de entrada de segurança do sistema, mapeada no **NFR Framework** (Usabilidade vs. Segurança) e detalhada no **BPMN**. |
| **Impacto** | 1. Funciona como a "catraca" que o Usuário deve passar antes de iniciar a Compra ou acionar uma Devolução, garantindo que o Mediador saiba quem está transacionando. |

---

## Serviços da Plataforma

### 10. Interface (Camada de Apresentação)

| Campo | Descrição |
|---|---|
| **Noção** | Componente de front-end responsável por exibir telas, formulários de entrada e mensagens de erro ao Usuário, mapeado diretamente como a primeira raia do **BPMN**. |
| **Impacto** | 1. Coleta dados de credenciais no **Login** e **Cadastro**.<br>2. Exibe feedback visual atômico, impactando o *softgoal* de `Facilidade de Aprendizado` no **NFR Framework**. |

### 11. Módulo de Segurança, Autenticação e Gestão de Sessão

| Campo | Descrição |
|---|---|
| **Noção** | Subsistema de back-end responsável por validar credenciais e controlar tentativas de acesso, correspondendo às raias centrais do **BPMN**. |
| **Impacto** | 1. Executa o fluxo de senhas, *Passwordless* (OTP) e 2FA.<br>2. Gera trade-offs críticos de `Confidencialidade` e `Eficiência` mapeados no SIG de **Login**. |

---

## Pós-venda e Conflitos

### 12. Devolução (Fluxo Vermelho)

| Campo | Descrição |
|---|---|
| **Noção** | Processo de retorno do Produto ao Vendedor acionado quando a expectativa do Usuário é frustrada (produto chega errado/estragado). |
| **Impacto** | 1. Representado pelas setas vermelhas e pelo ícone de polegar para baixo no **Rich Picture**.<br>2. Exige a intervenção do Mediador (Balança) para instruir a Instituição Financeira a estornar o valor e a Transportadora a recolher o item. |

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 27/08/26 | Criação da página e adição do domínio léxico | José Joaquim da Silva Neto | João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.1 | 28/08/26 | Adicionando elos de rastreabilidade | José Joaquim da Silva Neto e Pedro Henrique Gomes | -- |
| 1.2 | 28/08/26 | Ajuste do léxico para integração com BPMN e NFR Framework | Pedro Henrique Gomes | José Joaquim da Silva Neto |
| 1.3 | 28/08/26 | Refatoração de atores (Mediador, Transportadora, Instituição Financeira) e fluxos (Verde/Vermelho) para alinhar ao novo Rich Picture |José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes | José Joaquim da Silva Neto, João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes|