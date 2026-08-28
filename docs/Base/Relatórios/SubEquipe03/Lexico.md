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

### 1. Comprador (Cliente / Ator)

| Campo | Descrição |
|---|---|
| **Noção** | Usuário da plataforma que busca, seleciona e adquire produtos anunciados por um Vendedor. Atua como o ator inicial no fluxo de autenticação e navegação. |
| **Impacto** | 1. Inicia o processo interativo disparando o fluxo de **Login** ou **Cadastro** no BPMN.<br>2. Insere dados de credenciais na Interface.<br>3. Realiza busca de Produto e adiciona item ao Carrinho de Compras (mapeado no *Rich Picture*).<br>4. Confirma Pedido e efetua Pagamento, podendo registrar Reclamação ou solicitar Devolução. |

### 2. Vendedor

| Campo | Descrição |
|---|---|
| **Noção** | Usuário, pessoa física ou jurídica, que cadastra Anúncios de Produtos para comercialização na plataforma. |
| **Impacto** | 1. Cria e publica Anúncio.<br>2. Gerencia Estoque.<br>3. Despacha Pedido para Envio.<br>4. Responde a Reclamações e Disputas abertas por Compradores. |

---

## Objetos do Domínio

### 3. Anúncio

| Campo | Descrição |
|---|---|
| **Noção** | Publicação criada pelo Vendedor descrevendo um Produto disponível para venda, contendo preço, fotos, características e condições de Frete. |
| **Impacto** | 1. Fica visível para busca de Compradores.<br>2. Pode ser pausado, editado ou removido pelo Vendedor.<br>3. Recebe Avaliações após vendas concluídas. |

### 4. Produto

| Campo | Descrição |
|---|---|
| **Noção** | Item físico ou digital ofertado em um Anúncio, associado a uma Categoria e a um nível de Estoque. |
| **Impacto** | 1. É adicionado ao Carrinho de Compras.<br>2. Integra um Pedido após confirmação de compra. |

### 5. Carrinho de Compras

| Campo | Descrição |
|---|---|
| **Noção** | Espaço virtual temporário onde o Comprador reúne Produtos selecionados antes de finalizar a compra. |
| **Impacto** | 1. Permite adicionar ou remover Produtos.<br>2. É convertido em Pedido no fechamento da compra. |

### 6. Estoque

| Campo | Descrição |
|---|---|
| **Noção** | Quantidade disponível de um Produto que o Vendedor possui para atender Pedidos. |
| **Impacto** | 1. É decrementado a cada Pedido confirmado.<br>2. Quando zerado, pausa automaticamente o Anúncio. |

### 7. Cupom de Desconto

| Campo | Descrição |
|---|---|
| **Noção** | Benefício promocional aplicável ao valor de um Pedido, oferecido pela plataforma ou pelo Vendedor. |
| **Impacto** | 1. Reduz o valor cobrado no Pagamento.<br>2. Possui regras de elegibilidade e validade. |

---

## Processos e Estados

### 8. Pedido

| Campo | Descrição |
|---|---|
| **Noção** | Registro formal gerado a partir da confirmação de compra, vinculando Comprador, Vendedor, Produto(s) e status de Pagamento e Envio. |
| **Impacto** | 1. Aciona cobrança via Pagamento.<br>2. Gera obrigação de Envio ao Vendedor.<br>3. Pode ser cancelado antes do despacho. |

### 9. Pagamento

| Campo | Descrição |
|---|---|
| **Noção** | Transação financeira que efetiva a quitação do valor do Pedido, processada via Mercado Pago. |
| **Impacto** | 1. Libera o Pedido para separação e Envio.<br>2. Pode ser estornado em caso de Chargeback ou cancelamento.<br>3. Exige reautenticação (*Step-Up Authentication*), relacionando-se com a segurança do **Login**. |

### 10. Avaliação / Reputação

| Campo | Descrição |
|---|---|
| **Noção** | Pontuação e comentário atribuídos por Comprador ou Vendedor após a conclusão de um Pedido, refletindo a qualidade do serviço prestado. |
| **Impacto** | 1. Compõe o histórico público do Vendedor.<br>2. Influencia o posicionamento do Anúncio nas buscas. |

---

## Serviços da Plataforma

### 11. Interface (Camada de Apresentação)

| Campo | Descrição |
|---|---|
| **Noção** | Componente de front-end responsável por exibir telas, formulários de entrada e mensagens de erro ao Comprador, mapeado diretamente como a primeira raia do **BPMN**. |
| **Impacto** | 1. Coleta dados de credenciais no **Login** e **Cadastro**.<br>2. Exibe feedback visual atômico (*Validação Contínua de Input*), impactando diretamente o *softgoal* de `Facilidade de Aprendizado` no **NFR Framework**. |

### 12. Módulo de Autenticação e Gestão de Sessão

| Campo | Descrição |
|---|---|
| **Noção** | Subsistema de back-end responsável por validar credenciais, controlar tentativas de acesso e gerenciar tokens de sessão, correspondendo às raias centrais do **BPMN**. |
| **Impacto** | 1. Executa o fluxo de senhas, *Passwordless* (OTP) e validação de 2FA.<br>2. Gera trade-offs críticos de `Confidencialidade` e `Eficiência` mapeados no SIG de **Login** do **NFR Framework**. |

### 13. Módulo de Segurança e Antifraude

| Campo | Descrição |
|---|---|
| **Noção** | Subsistema isolado que monitora comportamentos anômalos, gerencia bloqueios temporários por excesso de tentativas e tokens sensíveis de recuperação. |
| **Impacto** | 1. Aciona o evento de fim *Acesso Bloqueado* no **BPMN**.<br>2. Introduz restrições que impactam negativamente a `Usabilidade` em prol da proteção de contas no **NFR Framework**. |

### 14. Mercado Pago

| Campo | Descrição |
|---|---|
| **Noção** | Serviço de intermediação financeira da plataforma responsável pelo processamento de Pagamentos, repasses a Vendedores e gestão de estornos. |
| **Impacto** | 1. Retém valores até confirmação de entrega em algumas modalidades.<br>2. Processa reembolsos em Devoluções. |

### 15. Frete

| Campo | Descrição |
|---|---|
| **Noção** | Custo e condição logística de transporte do Produto do Vendedor até o Comprador. |
| **Impacto** | 1. É calculado no momento da compra.<br>2. Pode ser gratuito conforme regras do Vendedor ou da plataforma. |

### 16. Mercado Envios

| Campo | Descrição |
|---|---|
| **Noção** | Serviço logístico da plataforma que gerencia o transporte, rastreamento e entrega dos Pedidos. |
| **Impacto** | 1. Gera código de rastreio para o Comprador.<br>2. Notifica alterações de status de Envio. |

### 17. Mercado Livre Full

| Campo | Descrição |
|---|---|
| **Noção** | Modalidade logística em que o Vendedor armazena Estoque previamente em centros de distribuição da plataforma, que assume a separação e o Envio. |
| **Impacto** | 1. Reduz prazo de entrega.<br>2. Isenta o Vendedor da etapa de despacho manual. |

---

## Pós-venda e Conflitos

### 18. Reclamação

| Campo | Descrição |
|---|---|
| **Noção** | Manifestação formal do Comprador relatando problema com Produto, Envio ou atendimento referente a um Pedido. |
| **Impacto** | 1. Pode escalar para Disputa.<br>2. Aciona prazo de resposta obrigatório do Vendedor. |

### 19. Disputa

| Campo | Descrição |
|---|---|
| **Noção** | Processo de mediação formal aberto quando Comprador e Vendedor não resolvem uma Reclamação diretamente. |
| **Impacto** | 1. Envolve intervenção da plataforma como mediadora.<br>2. Pode resultar em Devolução ou reembolso via Mercado Pago. |

### 20. Devolução

| Campo | Descrição |
|---|---|
| **Noção** | Processo de retorno do Produto ao Vendedor motivado por Reclamação, Disputa ou arrependimento de compra. |
| **Impacto** | 1. Aciona reembolso via Pagamento.<br>2. Reincorpora o item ao Estoque, quando aplicável. |

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 27/08/26 | Criação da página e adição do domínio léxico | José Joaquim da Silva Neto | João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |
| 1.1 | 28/08/26 | Adicionando elos de rastreabilidade | José Joaquim da Silva Neto e Pedro Henrique Gomes | -- |
| 1.2 | 28/08/26 | Ajuste do léxico para integração com BPMN, NFR Framework e Rich Picture | Pedro Henrique Gomes | José Joaquim da Silva Neto|