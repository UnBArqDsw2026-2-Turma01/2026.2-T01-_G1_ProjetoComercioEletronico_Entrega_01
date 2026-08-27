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

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Lições aprendidas sobre IA | Julia Oliveira Patricio | -- |
