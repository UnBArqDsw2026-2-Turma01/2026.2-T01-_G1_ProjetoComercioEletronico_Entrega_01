# Léxico Ampliado da Linguagem (LAL) — Domínio Mercado Livre

> Técnica de Léxico Ampliado da Linguagem, aplicada ao domínio de comércio eletrônico do Mercado Livre. Cada símbolo é definido por uma **Noção** (denotação, sem julgamento) e um **Impacto** (conotação, consequências/ações no universo de discurso).

## Sumário

- [Atores](#atores)
- [Objetos do Domínio](#objetos-do-domínio)
- [Processos e Estados](#processos-e-estados)
- [Serviços da Plataforma](#serviços-da-plataforma)
- [Pós-venda e Conflitos](#pós-venda-e-conflitos)

---

## Atores

### 1. Comprador

| Campo | Descrição |
|---|---|
| **Noção** | Usuário da plataforma que busca, seleciona e adquire produtos anunciados por um Vendedor. |
| **Impacto** | 1. Realiza busca de Produto.<br>2. Adiciona item ao Carrinho de Compras.<br>3. Confirma Pedido e efetua Pagamento.<br>4. Pode registrar Reclamação ou solicitar Devolução após a compra. |

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
| **Impacto** | 1. Libera o Pedido para separação e Envio.<br>2. Pode ser estornado em caso de Chargeback ou cancelamento. |

### 10. Avaliação / Reputação

| Campo | Descrição |
|---|---|
| **Noção** | Pontuação e comentário atribuídos por Comprador ou Vendedor após a conclusão de um Pedido, refletindo a qualidade do serviço prestado. |
| **Impacto** | 1. Compõe o histórico público do Vendedor.<br>2. Influencia o posicionamento do Anúncio nas buscas. |

---

## Serviços da Plataforma

### 11. Mercado Pago

| Campo | Descrição |
|---|---|
| **Noção** | Serviço de intermediação financeira da plataforma responsável pelo processamento de Pagamentos, repasses a Vendedores e gestão de estornos. |
| **Impacto** | 1. Retém valores até confirmação de entrega em algumas modalidades.<br>2. Processa reembolsos em Devoluções. |

### 12. Frete

| Campo | Descrição |
|---|---|
| **Noção** | Custo e condição logística de transporte do Produto do Vendedor até o Comprador. |
| **Impacto** | 1. É calculado no momento da compra.<br>2. Pode ser gratuito conforme regras do Vendedor ou da plataforma. |

### 13. Mercado Envios

| Campo | Descrição |
|---|---|
| **Noção** | Serviço logístico da plataforma que gerencia o transporte, rastreamento e entrega dos Pedidos. |
| **Impacto** | 1. Gera código de rastreio para o Comprador.<br>2. Notifica alterações de status de Envio. |

### 14. Mercado Livre Full

| Campo | Descrição |
|---|---|
| **Noção** | Modalidade logística em que o Vendedor armazena Estoque previamente em centros de distribuição da plataforma, que assume a separação e o Envio. |
| **Impacto** | 1. Reduz prazo de entrega.<br>2. Isenta o Vendedor da etapa de despacho manual. |

---

## Pós-venda e Conflitos

### 15. Reclamação

| Campo | Descrição |
|---|---|
| **Noção** | Manifestação formal do Comprador relatando problema com Produto, Envio ou atendimento referente a um Pedido. |
| **Impacto** | 1. Pode escalar para Disputa.<br>2. Aciona prazo de resposta obrigatório do Vendedor. |

### 16. Disputa

| Campo | Descrição |
|---|---|
| **Noção** | Processo de mediação formal aberto quando Comprador e Vendedor não resolvem uma Reclamação diretamente. |
| **Impacto** | 1. Envolve intervenção da plataforma como mediadora.<br>2. Pode resultar em Devolução ou reembolso via Mercado Pago. |

### 17. Devolução

| Campo | Descrição |
|---|---|
| **Noção** | Processo de retorno do Produto ao Vendedor motivado por Reclamação, Disputa ou arrependimento de compra. |
| **Impacto** | 1. Aciona reembolso via Pagamento.<br>2. Reincorpora o item ao Estoque, quando aplicável. |

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 27/08/2026 | Criação da págica e adição do domínio léxico | José Joaquim da Silva Neto | João Paulo Barbosa Pereira Nunes, Júlia Santana Campos e Pedro Henrique Gomes |