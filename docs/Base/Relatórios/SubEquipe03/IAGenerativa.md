# IA Generativa

## Ponto de Vista - João Paulo Barbosa Pereira Nunes

### Uso da IA Generativa (senso crítico)

Durante a elaboração do diagrama BPMN, a inteligência artificial generativa (Claude) foi utilizada como ferramenta de apoio técnico e visual, atuando em três frentes principais, com uma separação rigorosa entre a tomada de decisão humana e a assistência automatizada.

**Diagnóstico técnico e correção de desvios:** Na etapa inicial, a IA foi empregada para inspecionar o diagrama. Ela foi capaz de identificar que a versão preliminar reaproveitava erroneamente um template genérico de processo de compra (*Order Fulfillment*), desconexo do escopo real de Login e Cadastro. A ferramenta também apontou falhas na notação, como gateways mal posicionados e ausência de conteúdo nas raias planejadas, alertando para inconsistências estruturais.

**Apoio na estruturação da engenharia reversa:** Como não há documentação pública do fluxo interno de autenticação do Mercado Livre, o mapeamento do comportamento da plataforma (verificação de e-mail e celular, 2FA, bloqueio por tentativas excedidas e recuperação de senha) exigiu um trabalho estritamente humano de engenharia reversa e observação prática. A IA não gerou as regras de negócio, mas atuou como um suporte fundamental para traduzir a lógica empírica que levantei em um encadeamento BPMN coerente e completo.

**Refinamento visual e aplicação de notação:** Na construção final, a ferramenta auxiliou na aplicação estrita da notação BPMN oficial (pools, raias, gateways exclusivos identificados com "X", eventos de início e fim). Após uma primeira versão apresentar poluição visual, a IA ajudou a reorganizar o layout, reduzindo o cruzamento de conectores e alinhando as etapas em colunas com pontos de interface adicionais para melhorar a legibilidade.

**Conclusão sobre a responsabilidade do autor:** Todo o processo de decisão sobre o que o diagrama deveria conter, quais regras de negócio modelar e como as etapas se conectam na realidade, partiu exclusivamente da minha análise e validação em parceria com a Júlia. A IA funcionou estritamente como um assistente de estruturação, diagnóstico técnico e diagramação visual, sem interferir na autoria da lógica do processo.

---
## Ponto de Vista - José Joaquim da Silva Neto

### Lições Aprendidas

**BPMN não é um mapa mental, é um contrato entre raias.** A primeira versão do diagrama tentava concentrar praticamente todas as ações dentro de uma raia só, como se o processo de login e cadastro pertencesse a um único responsável genérico chamado "sistema". Isso só deixou de fazer sentido quando entendemos que cada raia no BPMN representa um limite real de responsabilidade dentro da arquitetura: a raia de Interface não pode decidir nada, ela apenas exibe telas e coleta dados do usuário; quem valida credencial, gera token de redefinição de senha, incrementa contador de tentativas ou bloqueia a conta são raias completamente diferentes — Autenticação, Segurança e Cadastro. Toda vez que um elemento parecia "não caber direito" numa raia, isso era sinal de que ainda não tínhamos separado com clareza "quem solicita" de "quem decide" de "quem executa". Essa separação forçou decisões de modelagem que, sem o BPMN, provavelmente teriam ficado implícitas — por exemplo, decidir que a geração do código de verificação 2FA pertence à raia de Autenticação, mas o envio efetivo da notificação (SMS/e-mail) é tratado como uma ação distinta, associada a um serviço de notificação, e não misturada dentro do mesmo elemento.

**NRF Framework não aceita requisito vago.** Escrever "o sistema deve ser seguro" ou "o cadastro deve ser confiável" como softgoal no NRF Framework é fácil de redigir e praticamente inútil como especificação, porque não é operacionalizável nem testável. O framework só passou a funcionar de fato quando cada softgoal foi decomposto em operacionalizações concretas — por exemplo, decompor "Segurança no Login" em sub-elementos como "Limitar tentativas de autenticação", "Expirar código de verificação após tempo definido" e "Bloquear conta temporariamente após limite excedido". Cada uma dessas operacionalizações, por sua vez, só fazia sentido depois de já termos desenhado o gateway correspondente no BPMN — o que reforçou, de novo, que os dois artefatos não foram produzidos em sequência estanque, mas se corrigiram mutuamente ao longo do processo.


**Rich Picture como origem dos atores modelados no BPMN.** O Rich Picture, construído antes do BPMN, foi o que nos fez identificar formalmente os atores que depois viraram raias ou elementos do diagrama de processo: o usuário, o módulo de interface, o módulo de autenticação, o serviço de segurança/antifraude e o serviço de notificação. Sem esse mapeamento inicial, é provável que tivéssemos desenhado o BPMN com menos raias, agrupando responsabilidades que, na prática, pertencem a componentes distintos do sistema — como confundir a raia de Segurança com a de Autenticação, tratando geração de token e validação de credencial como a mesma coisa.

**Publicação no Docsify/GitHub Pages expõe inconsistência entre artefatos.** Publicar Rich Picture, NRF Framework e BPMN no mesmo site tornou visível, lado a lado, qualquer defasagem entre eles — um diagrama BPMN já corrigido convivendo com uma versão desatualizada do NRF Framework que ainda não refletia a mesma regra de negócio, por exemplo. Isso fez da atualização cruzada dos três artefatos parte do fluxo de trabalho corrente, e não uma etapa de revisão isolada feita apenas ao final do projeto, já que qualquer pessoa acessando o site conseguiria perceber a inconsistência imediatamente.

**Controle de versão via Git como registro de decisão de modelagem, não apenas de código.** Diferente de projetos puramente de código, versionar artefatos de modelagem (diagramas exportados, arquivos-fonte do BPMN, documentos do NRF Framework) no mesmo repositório do site Docsify exigiu cuidado extra com nomenclatura de arquivos e histórico de commits, já que cada revisão de um gateway ou de um softgoal era, em si, uma decisão de engenharia de requisitos que precisava ficar rastreável. Usar `Co-authored-by` nos commits que vieram de decisão conjunta — como os ajustes nos gateways do fluxo de login e nos elementos da raia de Segurança, discutidos junto com Pedro Henrique, João Paulo e Júlia — deixou o histórico do repositório refletir com mais precisão quem de fato participou de cada decisão de modelagem, em vez de atribuir toda a autoria apenas a quem executou o commit no terminal.

### Uso da IA Generativa (senso crítico)

A IA generativa foi utilizada como ferramenta de apoio à documentação, empregada nas seguintes atividades: estruturação de relatórios técnicos a partir de artefatos já produzidos (por exemplo, geração do relatório descritivo do diagrama BPMN a partir do arquivo exportado em PDF), organização textual de conteúdo já definido pela equipe e formatação de documentos em Markdown para publicação no Docsify.

Todo conteúdo gerado foi submetido a revisão manual antes da incorporação aos artefatos finais. Em pontos específicos, identificou-se que a ferramenta apresentava suposições não confirmadas pela equipe, como valores numéricos de limite de tentativas de login ou tempo de expiração de código, que não constavam explicitamente no BPMN modelado. Esses trechos foram removidos ou sinalizados como pontos em aberto, não incorporados como definição de requisito.

As decisões de modelagem, estrutura das raias, definição dos gateways, elementos do NRF Framework e do Rich Picture, permaneceram sob responsabilidade exclusiva da equipe, sendo a IA generativa utilizada apenas como suporte de redação e organização de conteúdo já definido, sem interferência nas decisões de engenharia de requisitos do projeto.

---

## Ponto de Vista - Júlia Santana Campos

### Lições Aprendidas

**A engenharia reversa como fundação da modelagem realista.** Trabalhando em dupla com o João, ficou claro que desenhar um diagrama BPMN de um sistema existente e sem documentação pública, como o Mercado Livre, exige muito mais do que apenas conhecer a ferramenta de desenho. Aprendi que o passo fundamental é a observação tátil do sistema (engenharia reversa de caixa-preta). Tentar abstrair o funcionamento antes de testar na prática nos levou a erros iniciais, como o uso de templates genéricos. O BPMN só passou a ter valor real quando começamos a mapear o comportamento empírico da plataforma, como os fluxos de exceção, validação em duas etapas e bloqueios.

**Separação arquitetural através das raias.** Outra lição valiosa foi compreender que o BPMN força a definição de limites arquiteturais. O processo nos ensinou a parar de pensar no "sistema" como uma entidade única e começar a separar "quem solicita", "quem valida" e "quem notifica". Essa clareza transformou nossa visão sobre o fluxo de autenticação, mostrando que a interface é apenas uma casca, enquanto os motores de segurança e cadastro operam regras de negócio complexas nos bastidores.

### Uso da IA Generativa (senso crítico)

Encarei a inteligência artificial generativa como uma grande facilitadora metodológica e de aprendizado durante a elaboração deste trabalho em dupla. O uso da ferramenta foi focado na compreensão técnica e na ponte entre a teoria e a prática.

**Compreensão aprofundada da notação:** Utilizei a IA como uma tutora para dominar as regras oficiais do BPMN. Quando tínhamos dúvidas sobre como representar corretamente regras de negócio complexas, como o uso correto de gateways exclusivos ou a sinalização de eventos intermediários, a IA ajudou a esclarecer a semântica da notação, garantindo que não estivéssemos apenas desenhando um fluxograma comum, mas sim um modelo de processos formal.

**Apoio na estruturação da engenharia reversa:** A IA foi fundamental para me ajudar a entender *como* aplicar os achados da nossa engenharia reversa de maneira estruturada. Eu fornecia as observações práticas de como a plataforma do Mercado Livre se comportava (ex: o que acontece quando o limite de tentativas é excedido), e utilizava a IA para discutir como traduzir essa lógica observada em etapas processuais coerentes.

**Conclusão sobre o método:** A IA atuou como uma ponte que facilitou a tradução do comportamento real (caixa-preta) para a linguagem formal do BPMN. Contudo, a responsabilidade de "ir a campo", testar o software, provocar os erros na interface e validar se o desenho final de fato representava a realidade permaneceu inteiramente humana. A IA otimizou o como fazer, mas o *que* fazer partiu da nossa análise crítica e empírica do sistema.

---

## Ponto de Vista - Pedro Henrique Gomes

### Lições Aprendidas

**O primeiro contato com o SIG e a quebra de expectativa.** Antes desta entrega, eu não conhecia o NFR Framework e os diagramas SIG (Softgoal Interdependency Graph). Minha visão inicial sobre requisitos não funcionais era de que eles formavam apenas uma lista de desejos teóricos ("o sistema deve ser rápido e seguro"). Aprender a notação do SIG me ensinou que um requisito não funcional se modela a partir de *trade-offs*: toda decisão técnica melhora algo ao custo de piorar outra coisa. 

**O NFR Framework só tem valor se for empírico.** A chave para o meu trabalho virou quando passei a basear o grafo em telemetria real e atributos de código através da engenharia reversa de caixa-preta. Provar que a validação de segurança ocorre na interface de forma síncrona (evento `input` e não `focus_out`) ou identificar o uso de *Long-Lived Cookies* transformou o artefato. Ele deixou de ser uma abstração genérica para se tornar um mapa de decisões arquiteturais rigorosamente documentadas. 

**A conversão governa a segurança.** Ler os fluxos na prática me forçou a modelar conflitos reais no SIG. Ficou claro que a plataforma aceita deliberadamente uma dívida de segurança (adotando autenticação *Passwordless* e sacrificando a confidencialidade contra ataques locais ou *SIM Swap*) para reduzir a fricção e reter o usuário. A segurança rígida não deixou de existir, ela apenas foi empurrada para o momento de ações financeiras. Aprender a expressar essa "dívida assumida" através das setas de contribuição negativa (Hurt/Break) foi o maior aprendizado da modelagem.

### Uso da IA Generativa (senso crítico)

Utilizei a IA Generativa de forma intensiva, mas com uma separação estrita de responsabilidades: **eu fornecia o dado empírico e as regras de negócio, a IA atuava como tutora da notação e assistente de formatação.**

**Onde a IA foi indispensável (Tutoria e Estrutura):** Onde a IA foi indispensável (Tutoria e Estrutura): Como eu não conhecia o SIG antes deste trabalho, a IA funcionou como um excelente "segundo professor" para tirar dúvidas rápidas sobre as regras da notação (por exemplo, a diferença de impacto entre MAKE, HELP, HURT e BREAK). Ela foi fundamental para me ajudar a entender a lógica de decomposição dos softgoals e a regra de propagação dos rótulos até a raiz, garantindo que os trade-offs que identifiquei fossem representados de forma estruturada e coerente com a teoria do framework.

**Onde a IA falhou ou foi inútil (Geração de Conhecimento):** A IA não sabe fazer engenharia reversa. Se eu pedisse para ela "fazer o SIG do login do Mercado Livre", ela me entregaria um grafo genérico de e-mail e senha. Ela não sabia que a plataforma ofusca erros de e-mail inválido, não sabia que o OTP chega isolado em uma *Express Lane*, e não sabia do padrão de *Progressive Profiling* no cadastro. Todo o mapeamento de exceções, interceptação de rede e leitura de DOM teve que ser feito manualmente por mim. A IA só conseguiu ajudar a estruturar e formatar essas regras *depois* que eu as descobri na prática e as forneci no prompt.

**Conclusão sobre o método:** A IA é uma ótima assistente de formatação e uma boa ferramenta para explicar frameworks desconhecidos, mas ela é cega para a realidade tátil do software. O trabalho de investigar, abrir o *DevTools*, provocar exceções no sistema e definir o que de fato é relevante colocar no SIG continua sendo um trabalho cem por cento humano.

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.1 | 27/08/2026 | Adição das visões | Júlia Santana Campos | João Paulo Barbosa Pereira Nunes |