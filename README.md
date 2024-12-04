# WhatsApp Bot Incompleto
Coleção de versões usadas na criação do bot de WhatsApp.  
Devido a condições de tempo, o projeto não foi finalizado. 

# Descrição

O software é um bot para WhatsApp capaz de coletar telemetria relacionada às notas de estudantes, compilar dados, informar o professor sobre eventos e
flutuações na média das turmas. No caso específico em que está sendo utilizado, ele é aplicado em grupos de RPG, com a função de informar como o jogo funciona,
registrar presenças, notas e feedback dos jogadores em relação ao narrador. Além disso, o bot serve como um lembrete para aulas e possíveis cancelamentos, com
o objetivo de facilitar a organização de grupos grandes.  
Embora a ideia de bots para comunicação e organização não seja nova, sua aplicação no contexto educacional, especialmente em sala de aula, ainda é pouco
explorada. A simplicidade do processo, ao permitir que um bot mantenha os alunos informados e explique superficialmente como funciona a matéria, é um
diferencial significativo. O software também pode ser utilizado para informar planos de ensino ou comunicar alterações no cronograma.  
Ao final do semestre, o bot gera uma tabela consolidada com a telemetria dos estudantes, incluindo indicadores como taxa de evasão, reprovação, aprovação,
divisão por gênero e problemas identificados ao longo do período. Essa funcionalidade proporciona ao professor uma visão mais ampla e detalhada da turma,
auxiliando na análise e na tomada de decisões pedagógicas.  
Em relação a futuras ampliações, o bot pode ser personalizado para cada turma ou aplicação. Embora serviços similares existam no âmbito profissional, sua
aplicação dentro do contexto escolar é inédita, o que confere ao projeto um alto potencial de escalabilidade.

# Etapas
## Data Base
Criação da DataBase sera feita localmente com SQLite.  

- Info de usuario: # Estudantes da Turma
  - Wa_id (Id do WhatsApp)
    - Nome
    - Matrícula
    - Grupo
    - Genêro
    - Curso de origem
    - Observações especiais
    - Desistencia

- Info de Turma:
    - Grupos
        - Nome do grupo
          - Lider
          - Participante
        
- Info de Adm: # Possui Privilegios em ações
    - Wa_id
        - Nome

- Info de Sala:
  - Dia
    - Lider
      - Matricula
        - Pontualidade # Nota dada pelo jogador, de maneira anonima
        - Tema
        - Inclusão
    - Jogador
      - Matricula
        - Presença
        - Nota do dia
          
- Info Coletada: # Medias
    - Lider
      - Matrícula
        - Dias Jogados
        - Media dos Jogadores
        - Menor nota aplicada
        - Maior nota aplicada
        - Media de pontualidade
        - media de tema
        - media de inclusão
    - Jogador
      - Matrícula
        - Media de presença
        - Media de nota
    - Grupo
      - Matricula do Lider
        - Media dos jogadores
        - Dias jogados
        - Desistencias

## Front End
A parte que vai interagir com os usuarios, organização de tabelas.

Acredito ser de bom gosto usar a função de enquetes presente no WhatsApp Para coletar informações

## Back End 
Como o programa ira funcionar por baixo dos panos

Estarei usando o modulo Flask do python para gerenciar comunicações de request, assim como APIs disponibilizadas pela propria Meta.

A hospedagem do serviço sera feita pelo google cloud .
  

