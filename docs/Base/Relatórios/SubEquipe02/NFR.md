# NFR Framework - Módulo de Busca (Subequipe 02)

O NFR Framework é uma abordagem sistemática voltada para a representação e análise de Requisitos Não Funcionais (RNFs) ou qualidades de software. O framework trata estes requisitos como *softgoals* (metas flexíveis), que podem ser satisfeitos em graus variados (satisfeito, parcialmente satisfeito, negado, etc.) em vez de um critério binário de atendido/não atendido.

Este documento apresenta o relatório do NFR Framework desenvolvido pela **Subequipe 02** para o **Módulo de Busca** do sistema de comércio eletrônico, incluindo a modelagem do SIG (Softgoal Interdependency Graph) e a validação técnica das decisões arquiteturais utilizando o DevTools do navegador.

---

## 1. Introdução e Embasamento Teórico

Na engenharia de software tradicional, os Requisitos Não Funcionais frequentemente recebem menor prioridade em comparação com as funcionalidades básicas. O **NFR Framework**, proposto originalmente por Lawrence Chung et al. (2000), visa solucionar essa assimetria elevando os RNFs a elementos de primeira classe no design de arquitetura.

O framework utiliza o conceito de **Softgoal**, uma meta que não possui uma definição ou critério de aceitação estrito e absoluto. Há três tipos principais de softgoals:
1. **NFR Softgoals (Nuvens Claras):** Representam os Requisitos Não Funcionais abstratos a serem alcançados (ex: Desempenho, Usabilidade).
2. **Operationalization Softgoals (Nuvens de Bordas Grossas):** Representam decisões técnicas de design, soluções de engenharia ou mecanismos de implementação propostos para satisfazer os NFR Softgoals.
3. **Claim Softgoals (Nuvens de Borda Pontilhada):** Funcionam como argumentos ou justificativas baseados em evidências concretas para validar ou apoiar as relações de contribuição.

A interdependência entre esses elementos é representada graficamente por meio de um **SIG (Softgoal Interdependency Graph)**. As contribuições podem ter diferentes intensidades:
* `++` (Make): A operacionalização satisfaz o softgoal de forma decisiva.
* `+` (Help): A operacionalização ajuda a satisfazer o softgoal.
* `-` (Hurt): A operacionalização prejudica a satisfação do softgoal.
* `--` (Break): A operacionalização nega ou impede a satisfação do softgoal.

---

## 2. Metodologia

A **Subequipe 02** focou no **Módulo de Busca**, considerado a principal porta de entrada de conversão em plataformas de e-commerce modernos. A metodologia baseou-se nos seguintes passos:
1. **Ciclo de Modelagem:** O SIG foi desenvolvido interativamente. Identificou-se que as soluções de otimização de latência (como cache e autocomplete) e de usabilidade (como corretor fonético e busca preditiva) geravam tensões mútuas, exigindo uma análise explícita de correlações negativas (`-`).
2. **Coleta de Evidências:** A validação prática das operacionalizações foi executada capturando dados reais de tráfego de rede (requests fetch/XHR, latências, tamanhos de payload e códigos de status) da ferramenta de testes.

---

## 3. Diagrama SIG (Softgoal Interdependency Graph)

Abaixo está a representação gráfica do SIG modelado para o Módulo de Busca do Comércio Eletrônico:

![Softgoal Interdependency Graph - Busca](../../../assets/Subequipe02/Diagrama%20NFR.png)

---

## 4. Detalhamento dos Softgoals e Operacionalizações

### 4.1. NFR Softgoals (Metas Principais)

* **modulo de busca [comercio eletronico]:** O softgoal raiz do sistema, que representa a experiência global de busca em um portal de compras. Ele é decomposto (via refinamento *AND*) em duas vertentes principais:
  * **Desempenho [busca]:** Mede os aspectos de eficiência temporal e de recursos físicos do sistema de busca.
  * **Usabilidade [busca]:** Foca na facilidade, precisão e satisfação do usuário ao tentar encontrar produtos.

#### Decomposição de Desempenho:
* **Baixa Latência de Resposta (Refinamento AND):** Tempo decorrido entre a digitação do usuário e a renderização das sugestões ou resultados em tela. Essencial para evitar o abandono do site.
* **Eficiência de Payload/Rede (Refinamento AND):** Minimização do tamanho dos dados trafegados nas requisições de busca, preservando a largura de banda do usuário e do servidor.

#### Decomposição de Usabilidade:
* **Relevância dos Resultados (Refinamento AND):** Grau de correspondência entre o desejo de compra do usuário e os itens sugeridos pelo sistema.
* **Facilidade de Refinamento (Refinamento AND):** Capacidade de filtrar e ordenar listagens densas de produtos de forma rápida.
* **Tolerância a Falhas de Digitação (Refinamento AND):** Robustez do mecanismo em entender o termo buscado mesmo em caso de erros gramaticais ou fonéticos.

---

### 4.2. Operationalization Softgoals (Mecanismos Técnicos)

* **Op: Autocomplete com Debounce (250ms):** 
  * *Contribuição:* Ajuda (`+`) a **Baixa Latência de Resposta**. 
  * *Justificativa:* Ao aguardar o usuário pausar a digitação por 250ms antes de disparar a chamada de API, reduz-se o volume de requisições inúteis no servidor, liberando recursos e acelerando as respostas reais.
* **Op: Cache de Borda / CDN em Termos Populares:** 
  * *Contribuição:* Satisfeita decisivamente (`++`) a **Baixa Latência de Resposta**.
  * *Justificativa:* Requisições para termos muito buscados (ex: "celular") são interceptadas e respondidas na borda da rede (CDN), sem precisar acessar o banco de dados principal.
* **Op: Lazy Loading e Imagens WebP:** 
  * *Contribuição:* Ajuda (`+`) a **Eficiência de Payload/Rede** e a **Baixa Latência de Resposta**.
  * *Justificativa:* Imagens de produtos só carregam quando rolam para a área visível do navegador e utilizam o formato otimizado WebP, que reduz drasticamente os bytes consumidos.
* **Op: Sugestões Preditivas por Categoria:** 
  * *Contribuição:* Ajuda (`+`) a **Relevância dos Resultados**.
  * *Correlação:* Prejudica (`-`) a **Eficiência de Payload/Rede**.
  * *Justificativa:* Agrupar termos sugeridos por seções lógicas ajuda o usuário a achar o produto de forma rápida. Contudo, retorna um JSON mais denso e estruturado, o que consome mais largura de banda na rede.
* **Op: Filtros Facetados via Fetch/AJAX:** 
  * *Contribuição:* Satisfeita decisivamente (`++`) a **Facilidade de Refinamento** e ajuda (`+`) a **Eficiência de Payload/Rede**.
  * *Justificativa:* Permite alternar atributos (como marca ou preço) de forma dinâmica atualizando apenas a div de resultados via requisições assíncronas XHR, evitando recarregar toda a estrutura HTML/CSS da página.
* **Op: Algoritmo de Correção Fonética / Typos:** 
  * *Contribuição:* Ajuda (`+`) a **Tolerância a Falhas de Digitação**.
  * *Correlação:* Prejudica (`-`) a **Baixa Latência de Resposta**.
  * *Justificativa:* Garante que o usuário encontre o produto desejado mesmo se digitar incorretamente. No entanto, exige processamento matemático extra no backend (ex: cálculo de distância de Levenshtein ou Soundex) a cada caractere digitado, aumentando ligeiramente o tempo de processamento.

---

### 4.3. Claim Softgoal (Argumento de Validação)

* **Claim: Tempo de resposta medido no DevTools < 150ms:**
  * Este argumento funciona como uma evidência que apoia a eficácia da contribuição do **Cache de Borda/CDN** para a **Baixa Latência de Resposta**, comprovando empiricamente que a decisão de cache resulta em tempos de resposta extremamente baixos (quase instantâneos), sustentando a contribuição positiva (`++`).

---

## 5. Validação Técnica com DevTools (Evidências Práticas)

Os prints extraídos do console DevTools do portal demonstram a validação dos requisitos não funcionais descritos na modelagem do SIG:

### Evidência 1: Autocomplete e Sugestão de Termos
O print do JSON retornado comprova o funcionamento da operacionalização **Autocomplete com Debounce** e **Sugestões Preditivas**:

![JSON Autocomplete](../../../assets/Subequipe02/print%20da%20webtool%20do%20json%20retornado%20para%20um%20termo.png)

* **Análise Técnica:** Quando o usuário insere o fragmento `"celu"`, a API responde de forma estruturada com sugestões relevantes de busca completa baseadas em histórico de relevância (ex: `"celular"`, `"celular samsung"`, `"celular motorola"`). Isso valida a busca preditiva de forma a maximizar a **Relevância dos Resultados** para a usabilidade do usuário.

### Evidência 2: Validação do Claim de Baixa Latência (Cache de Borda/CDN)
O print de rede do navegador valida empiricamente o **Claim** de tempo de resposta menor que 150ms para chamadas repetidas ou termos comuns:

![Validação de Cache](../../../assets/Subequipe02/print%20da%20webtool%20na%20busca%20de%20um%20termo.png)

* **Análise Técnica:** Podemos observar a requisição repetida de `/autosuggest?showFilters=t...` retornando com status `200` e tamanho rotulado como `(cache)`. O tempo total medido para esta operação foi de apenas **1 ms**. Isso atesta o sucesso da operacionalização de **Cache de Borda**, superando com folga o limite de 150ms postulado pelo Claim e atestando que a latência foi minimizada.

### Evidência 3: Filtros Facetados dinâmicos via Fetch/AJAX
O print de rede abaixo demonstra o comportamento dinâmico e otimizado ao aplicar um filtro na tela:

![Filtro Facetado](../../../assets/Subequipe02/Print%20da%20webtool%20da%20busca%20com%20filtro.png)

* **Análise Técnica:** A aplicação de um filtro facetado dispara uma chamada assíncrona (`xhr` no tipo de inicialização) enviando parâmetros detalhados de categoria (`api?category_id=MLB1055&...`). O tamanho do payload recebido é compacto (**5,6 kB**). Isso demonstra que o portal carrega somente os dados específicos dos produtos filtrados em segundo plano, sem necessidade de re-renderizar cabeçalhos e rodapés pesados, atendendo de forma unificada a **Eficiência de Payload** e a **Facilidade de Refinamento**.

### Evidência 4: Tolerância a Falhas de Digitação
A imagem abaixo demonstra o funcionamento do sistema quando o usuário comete um erro ortográfico grosseiro:

![Busca com Erro](../../../assets/Subequipe02/Print%20de%20busca%20com%20erro.png)

* **Análise Técnica:** O usuário pesquisou pelo termo incorreto `"Notibuque"`. Mesmo contendo graves erros de ortografia em relação ao termo correto ("Notebook"), a interface redirecionou o contexto para a categoria lógica `Informática > Portáteis e Acessórios > Notebooks` e encontrou **3 resultados relevantes**. Isso comprova que o **Algoritmo de Correção Fonética / Typos** foi ativado com sucesso em backend, garantindo que o softgoal de **Tolerância a Falhas** seja plenamente atendido em termos de Usabilidade.

---

## 6. Referências Bibliográficas

* CHUNG, Lawrence; NIXON, Brian A.; YU, Eric; MYLOPOULOS, John. **Non-functional requirements in software engineering**. Springer Science & Business Media, 2000.
* **Documentação do DSM3**. Disponível em: <https://www.cin.ufpe.br/~jhcp/dsm3goals/index.html>. Acesso em: 26 ago. 2026.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| :---: | :---: | :---: | :---: | :---: |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 26/08/2026 | Elaboração do conteúdo completo, modelagem do SIG, análise do DevTools e atualização do modelo NFR | Guilherme Davila, Julia Oliveira Patricio, Maria Clara Sena |  |