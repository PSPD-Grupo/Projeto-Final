# Gateway Contract

O API Gateway deve chamar o Patient Data Service via gRPC e repassar contexto
do usuario autenticado usando metadata.

## Metadata esperada

```text
x-user-username: username usado nas tabelas do banco
x-user-roles: lista separada por virgula
x-user-scopes: lista separada por virgula
x-request-id: id opcional para rastreio
```

Exemplos:

```text
x-user-username: maria.silva
x-user-roles: DOCTOR
x-user-scopes: patient:read
```

```text
x-user-username: admin
x-user-roles: ADMIN
x-user-scopes: patient:read:all
```

## Regra de acesso inicial

- `ADMIN` ou `patient:read:all`: pode consultar todos os pacientes.
- outros usuarios: so acessam pacientes com vinculo ativo em
  `user_patient_assignments`.

## Operacoes

### GetPatient

Busca um paciente por `patient_id`.

### SearchPatients

Busca por `full_name`, `patient_id`, `cpf` ou `cns`. Quando o usuario nao tem
acesso global, a busca fica restrita aos seus pacientes vinculados.

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
