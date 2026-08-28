# IA Generativa

## Ponto de Vista - João Paulo Barbosa Pereira Nunes

### Lições Aprendidas

**Raia não é camada de UI, é responsabilidade real.** A primeira versão do nosso BPMN tinha uma raia chamada "Interface", e por um bom tempo isso pareceu correto, afinal, alguém precisa "mostrar a tela" pro usuário. O ponto de virada foi entender que uma raia representa um ator que toma decisão ou executa regra de negócio, e interface não decide nada, ela só media a interação. Depois de remover essa raia, ficou muito mais claro que Autenticação, Segurança e Cadastro são responsabilidades de fato distintas (uma valida credencial, outra bloqueia conta e mexe com token, outra cuida do ciclo de vida da conta), e que juntar tudo embaixo de um rótulo genérico de "sistema" ou "interface" só escondia essa separação.

**Abstração errada é tão problema quanto conteúdo errado.** Corrigir o conteúdo do diagrama (trocar o template genérico pelo fluxo real de login e cadastro) não foi suficiente sozinho. As atividades continuavam descrevendo telas ("exibe tela de login") em vez de regra de negócio. Só quando reescrevi as atividades num nível mais técnico (consulta ao banco, comparação de hash, geração de token com TTL) o diagrama passou a ser útil como especificação, e não só como ilustração do que o usuário vê na tela.

**Diagrama também acumula dívida técnica.** Trabalhando direto no Miro via API, percebi que ficar remendando um board (mover uma caixa aqui, reconectar uma linha ali) tem um limite. Depois de algumas rodadas de ajuste incremental, o board ficou instável e algumas operações de edição simplesmente pararam de funcionar direito. A saída mais confiável, mesmo sendo mais trabalhosa, foi apagar tudo e recriar do zero já com o layout corrigido de uma vez. É basicamente o mesmo princípio de dívida técnica em código, só que aplicado a artefato visual: às vezes remendar sai mais caro do que refazer.

**Rastreabilidade não é burocracia, é o que evita retrabalho de revisão.** Ligar cada decisão do BPMN (por que esse TTL, por que esse gateway) à observação de engenharia reversa que a originou, e essa observação a uma reunião ou metodologia específica, obrigou a gente a documentar o "porquê" na hora, em vez de tentar reconstruir a justificativa depois, numa banca ou revisão, só de memória.

**Fluxo de Git também é modelagem de processo, só que do próprio trabalho.** Entender a diferença entre atualizar minha branch local com o que já está na main (git merge origin/main) e abrir um Pull Request pedindo pra minha branch ir pra main foi uma confusão real que tive nessa etapa. São dois fluxos com direção oposta, e o GitHub sugere o segundo automaticamente depois de um push, mesmo quando a intenção era só o primeiro. Vendo esse erro de perto ficou muito mais claro por que, no NRF Framework, a gente insiste tanto em explicitar sentido e direção de cada relação, ambiguidade de direção também gera retrabalho fora do modelo.

## Uso da IA Generativa (senso crítico)

Usei o Claude nesta etapa principalmente para diagnóstico do diagrama, reformulação estrutural (remover a raia de Interface, reduzir o nível de abstração) e construção do BPMN diretamente no Miro via API, além de apoio na estruturação dos documentos do projeto e no fluxo de Git.

A ferramenta também errou de um jeito que valeu como aprendizado prático. Em um dos ajustes, ela usou o comando de criação em vez de atualização e duplicou uma leva de itens no board sem eu ter pedido isso, e precisou de confirmação minha antes de apagar a bagunça. Em outro momento, o próprio layout gerado pela IA tinha linhas de conexão passando por cima de gateways de outras raias, um problema que só ficou visível quando eu de fato olhei o board com calma e perguntei, a IA não sinalizou isso sozinha. Ou seja, mesmo o conteúdo gerado pela IA precisou da minha checagem visual e funcional antes de ser aceito como versão final, o que reforça que revisão crítica não é só sobre o texto ou a regra de negócio, é também sobre o artefato visual em si.

As decisões sobre quais TTLs, limites de tentativa e regras de negócio o diagrama deveria representar vieram da nossa engenharia reversa da plataforma real, não de suposição da IA, e continuam marcadas como hipóteses a validar com os stakeholders, não como especificação fechada.

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
| 1.1 | 27/08/2026 | Adiciona ponto de vista | José Joaquim da Silva Neto | Pedro Henrique Gomes |
| 1.2 | 27/08/2026 | Adição das visões | Júlia Santana Campos | João Paulo Barbosa Pereira Nunes |
| 1.3 | 28/08/2026 | Atualização do ponto de vista | João Paulo Barbosa Pereira Nunes | Julia Santana Campos | 