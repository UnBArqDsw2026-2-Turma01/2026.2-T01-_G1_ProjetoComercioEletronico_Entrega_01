# IA Generativa


# Uso de Inteligência Artificial Generativa: Lições Aprendidas (Julia Oliveira Patricio)

A adoção de Inteligências Artificiais Generativas no fluxo de trabalho da engenharia de software exige um equilíbrio rigoroso entre produtividade e responsabilidade técnica. Como estudante de Engenharia de Software na Universidade de Brasília, estruturei este documento para registrar minhas reflexões e o senso crítico aplicado ao longo deste projeto, garantindo que essas tecnologias atuem como ferramentas de apoio, e não como substitutas do raciocínio analítico.

---

## Diretrizes Práticas de Uso

*   **Validação Obrigatória:** Nenhuma saída gerada por IA foi incorporada diretamente ao código-fonte ou à documentação sem validação e revisão prévia. Toda sugestão foi testada e confrontada com os requisitos arquiteturais do projeto.
*   **Apoio, não Autoria:** A IA foi utilizada para contornar gargalos de sintaxe (como estruturação de tabelas Markdown, sintaxe de comandos Git ou formatação de templates), enquanto as decisões de domínio, regras de negócio e modelagem (como o BPMN e a Engenharia Reversa) permaneceram inteiramente sob minha autoria.
*   **Proteção de Contexto:** Dados sensíveis, senhas, chaves de API e informações confidenciais do projeto nunca foram inseridos nos *prompts*.
*   **Transparência:** O uso da ferramenta para otimização de texto ou estruturação de formatação é reconhecido como parte do processo de desenvolvimento moderno, assumindo total responsabilidade pelo artefato final gerado.

---

## Lições Aprendidas e Senso Crítico

### 1. A Armadilha da Sintaxe Perfeita
IAs generativas frequentemente produzem soluções sintaticamente impecáveis, mas semanticamente incorretas. Durante o desenvolvimento, ficou claro que a ferramenta pode sugerir abordagens que utilizam bibliotecas obsoletas ou que ignoram o contexto de dependências do projeto.

### 2. Visão Local vs. Visão Sistêmica
A IA possui um escopo de contexto limitado à janela de conversa. Ela é excelente em resolver um problema isolado em uma função ou arquivo, mas é incapaz de prever como essa solução afeta a arquitetura global do sistema. Aplicar cegamente uma sugestão local pode ferir princípios de design de software e criar acoplamentos indesejados. O julgamento arquitetural sistêmico é uma habilidade exclusivamente humana.

### 3. Prevenção da "Erosão do Conhecimento"
Delegar a resolução de *bugs* rotineiros ou a formulação de consultas complexas para a IA cria uma falsa sensação de proficiência técnica. A IA deve acelerar a digitação e a busca, não suprimir o processo de aprendizado.

### 4. A Importância da Restrição no Prompt
A qualidade da resposta da IA é diretamente proporcional às restrições impostas a ela. Fornecer contexto específico e estabelecer limites claros (ex: *"Explique o erro sem reescrever o código inteiro"* ou *"Formate apenas em Markdown sem alterar o texto"*) evita que a ferramenta adote um comportamento excessivamente proativo, economizando tempo de revisão e retrabalho.

---

---

# Uso de Inteligência Artificial Generativa: Lições Aprendidas (Guilherme Davila)

## Uso da IA Generativa

**Tutor de Conteúdo Teórico:** A IA foi utilizada como apoio a dúvidas respondendo perguntas sobre o conteúdo para melhorar meu entendimento.<br>
**Apoio na Elaboração de Documentos:** Utilizei a ferramenta para estruturar a redação técnica do relatório final de NFR, garantindo um tom claro, formal e coeso.

##  Senso Crítico e Lições Aprendidas

A elaboração deste framework trouxe insights críticos para a equipe sobre as complexidades do desenho arquitetural de sistemas:

1. **Inexistência de Solução Perfeita (Trade-offs):** A engenharia de software é guiada por compromissos mútuos. Ficou nítido que buscar a Usabilidade extrema (ex: analisando foneticamente strings erradas em tempo real) gera atrito direto com o Desempenho (latência de resposta). Cabe ao arquiteto encontrar o ponto de equilíbrio aceitável pelo negócio (por exemplo, aplicando um cache agressivo de CDN para mitigar a latência introduzida pelos algoritmos de correção).
2. **Importância dos Argumentos (Claims):** Apenas modelar diagramas conceituais não basta para provar a qualidade. A introdução de dados empíricos do DevTools atuou como o fator decisivo para provar que as metas de engenharia propostas na modelagem se sustentam em ambiente produtivo real.

---
## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Lições aprendidas sobre IA | Julia Oliveira Patricio | -- |
| 1.2 | 27/08/2026 | Lições aprendidas sobre IA | Guilherme Davila | -- |
