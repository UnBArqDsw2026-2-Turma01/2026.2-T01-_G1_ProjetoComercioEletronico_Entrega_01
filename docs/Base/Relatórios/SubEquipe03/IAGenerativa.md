# IA Generativa

## Ponto de Vista - João Paulo Barbosa Pereira Nunes

### Lições Aprendidas

### Uso da IA Generativa (senso crítico)

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

### Uso da IA Generativa (senso crítico)

---

## Ponto de Vista - Pedro Henrique Gomes

### Lições Aprendidas

### Uso da IA Generativa (senso crítico)

---

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 24/08/2026 | Estruturação inicial | José Joaquim da Silva Neto | Pedro Henrique Gomes |
