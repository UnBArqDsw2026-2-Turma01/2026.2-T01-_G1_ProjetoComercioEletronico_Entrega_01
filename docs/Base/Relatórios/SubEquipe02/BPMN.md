# Modelagem BPMN

Este documento detalha o fluxo do sistema de busca, auto-completar e exibição de resultados, integrando a visão do usuário e o comportamento sistêmico.

## O que é o artefato

A *Business Process Management Notation* (BPMN) é uma notação padronizada para diagramação de fluxos de processos de negócio.
* Esta notação foi adotada pelo consórcio internacional *Object Management Group* (OMG).
* O modelo utiliza conectores para mostrar a ordem de sequenciamento das atividades e dos eventos que ocorrem no fluxo.
* Os elementos gráficos podem ser utilizados para definir o caminho principal de execução de um processo.

## O artefato

[![BPMN Fluxo de Busca](../../../assets/SubEquipe02/BPMN-Subequipe02-JuliaPatricio.jpg)](../../../assets/SubEquipe02/BPMN-Subequipe02-JuliaPatricio.jpg ":ignore")

<sub>*Clique na imagem para abri-la em tamanho real.*</sub>

> *Figura 1 — Diagrama BPMN da Seção de Busca. O fluxo mapeia a interação desde a digitação do comprador até a renderização dos resultados finais na interface.*

## Elementos Utilizados e Justificativas

A construção deste artefato seguiu as regras de notação para representar o sistema de forma concisa:

* **Piscina e Raias:** O fluxo está contido em uma única piscina (Seção de Busca) dividida em três raias: Comprador, Interface e API de Busca. As raias são comumente utilizadas para organizar e categorizar atividades, representando sistemas e papéis internos.
* **Atividades:** As caixas representam ações ou operações executadas no processo. A identificação foi feita utilizando um verbo na terceira pessoa do singular (ex: "Insere", "Requisita", "Processa", "Renderiza"), conforme a convenção da notação. 
* **Evento Timer (Intermediário):** O ícone de relógio ("Aguarda 300ms") indica uma espera dentro do processo, ou seja, uma demora programada entre as atividades. 
* **Gateway Exclusivo Baseado em Eventos:** Utilizado na decisão "Origem do disparo?", pois atua como um ponto de ramificação onde os caminhos alternativos são baseados em eventos. Dependendo da ação (clique do comprador ou remoção do foco), apenas um caminho prossegue.
* **Gateway Exclusivo:** Utilizado logo após a renderização do *grid* para criar fluxos alternativos exclusivos (produtos encontrados ou zero resultados). Neste ponto de decisão, apenas um caminho poderá ser seguido.

---

## Referências

SERRANO, Milene. **Arquitetura e Desenho de Software: AULA – Notação BPMN**. UnB Gama.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.0 | 27/08/2026 | Criação da documentação e adição do fluxo de busca | Julia Oliveira Patricio |