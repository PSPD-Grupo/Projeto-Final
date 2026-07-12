# Gateway Contract

O API Gateway deve chamar o Patient Data Service via gRPC e repassar contexto
do usuario autenticado usando metadata.

## Metadata esperada

```text
x-user-username: username usado nas tabelas do banco
x-user-roles: MEDICO, ESTAGIARIO ou PESQUISADOR
x-user-scopes: lista separada por virgula
x-request-id: id opcional para rastreio
```

Exemplos:

```text
x-user-username: maria.silva
x-user-roles: MEDICO
x-user-scopes: patient:read
```

```text
x-user-username: joao.estagio
x-user-roles: ESTAGIARIO
x-user-scopes: patient:read
```

```text
x-user-username: ana.pesquisa
x-user-roles: PESQUISADOR
x-user-scopes: research:read
```

## Regra de acesso inicial

- `MEDICO`: acessa dados FULL de pacientes com vinculo ativo
  `assignment_type = 'ATTENDING'`.
- `ESTAGIARIO`: acessa dados PARTIAL de pacientes com vinculo ativo
  `assignment_type = 'TRAINEE'` e `supervisor_username` preenchido.
- `PESQUISADOR`: nao acessa identificadores diretos; acessa projetos,
  estatisticas agregadas e exames anonimizados de coortes aprovadas.

## Operacoes

### GetPatient

Busca um paciente por `patient_id`.

Retorna:

- FULL para `MEDICO`;
- PARTIAL para `ESTAGIARIO`;
- negado para `PESQUISADOR`.

### SearchPatients

Busca por `full_name`, `patient_id`, `cpf` ou `cns` para `MEDICO`. A busca
sempre fica restrita aos pacientes vinculados ao usuario.

Para `ESTAGIARIO`, a busca nao usa CPF/CNS e a resposta nao contem
identificadores diretos.

### ListEncounters

Lista atendimentos de um paciente, ordenados do mais recente para o mais antigo.

### ListClinicalEvents

Lista eventos clinicos de um paciente. Pode filtrar por `encounter_id` e
`event_type`.

Valores esperados para `event_type`:

```text
CONDITION
OBSERVATION
MEDICATION
```

### ListResearchProjects

Lista os projetos do pesquisador autenticado.

### GetCohortStats

Retorna estatisticas agregadas de um projeto aprovado e ainda valido:

- total de pacientes;
- distribuicao por sexo;
- distribuicao por faixa etaria;
- distribuicao por departamento.

### ListAnonymizedLabResults

Retorna exames laboratoriais anonimizados para pacientes da coorte do projeto.
O paciente aparece apenas como hash, com sexo, faixa etaria e estado.
