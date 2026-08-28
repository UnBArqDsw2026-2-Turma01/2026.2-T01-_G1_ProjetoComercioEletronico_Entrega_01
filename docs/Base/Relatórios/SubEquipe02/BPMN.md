# Modelagem BPMN

Este documento detalha o fluxo do sistema de busca, auto-completar e exibição de resultados, integrando a visão do usuário e o comportamento sistêmico.

## O que é o artefato

A *Business Process Management Notation* (BPMN) é uma notação padronizada para diagramação de fluxos para o gerenciamento de processos de negócio.
* Notação que foi aderida pelo consórcio internacional *Object Management Group* (OMG).
* O modelo utiliza conectores para mostrar a ordem de sequenciamento das atividades e dos eventos que ocorrem no fluxo.
* Os elementos gráficos podem ser utilizados para definir o caminho principal de execução de um processo.

## O artefato

[![BPMN Fluxo de Busca](../../../assets/Subequipe02/BPMN-Subequipe02-JuliaPatricio.jpg)](../../../assets/SubEquipe02/BPMN-Subequipe02-JuliaPatricio.jpg ":ignore")

<sub>*Clique na imagem para abri-la em tamanho real.*</sub>

> *Figura 1 — Diagrama BPMN da Seção de Busca. O fluxo mapeia a interação desde a digitação do comprador até a renderização dos resultados finais na interface.*

## Elementos Utilizados e Justificativas

A construção deste artefato seguiu as regras de notação para representar o sistema de forma concisa:

* **Piscina e Raias:** O fluxo está contido em uma única piscina (Seção de Busca) dividida em três raias: Comprador, Interface e API de Busca. As raias são comumente utilizadas para organizar e categorizar atividades, representando sistemas e papéis internos.
* **Conectores:** Mostram a ordem de sequenciamento das atividades e dos eventos contidos em um fluxo de trabalho. Neste caso, utilizou-se apenas de fluxos de sequência, uma vez que fluxos de mensagens são destinados a mensagens entre dois participantes distintos, o que não foi considerado dentro de uma mesma piscina.
* **Atividades:** Representação de partes do processo nas quais alguma espécie de trabalho será realizada, nesta representação em específico, foram utilizadas tarefas de tipagem de serviço, envio e humana.
* **Evento:** Sub-processo especializado que não surge a partir de um fluxo normal derivado de um processo anterior. Neste caso, o Timer, ícone de relógio, indica uma espera dentro do processo, ou seja, uma demora programada entre as atividades. 
* **Gateway Exclusivo:** Controla fluxo de sequência, Utilizado na decisão "Origem do disparo?", pois atua como um ponto de ramificação onde os caminhos alternativos são baseados em eventos e logo após a renderização do *grid* para criar fluxos alternativos exclusivos.

---

## Referências

SERRANO, Milene. **Arquitetura e Desenho de Software: AULA – Notação BPMN**. UnB Gama.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Criação da documentação e adição do fluxo de busca | Guilherme Davila, Julia Oliveira Patricio, Maria Clara Sena | -- |