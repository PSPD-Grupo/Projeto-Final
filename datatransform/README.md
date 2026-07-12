# Data Transform Service

Microsserviço responsável por converter dados clínicos brutos (paciente, atendimentos, eventos clínicos) em recursos padronizados **HL7/FHIR**, aplicando a política de anonimização redação correta de acordo com o nível de acesso do usuário autenticado.

Faz parte do sistema de monitoramento/observabilidade em Kubernetes descrito na especificação da disciplina PSPD (Prof. Fernando W. Cruz) — arquitetura de microsserviços simulando um sistema de prontuário eletrônico do Hospital Universitário.

---

## 1. Onde este serviço se encaixa

```
Frontend → API Gateway → Authorization Service   (decide nível de acesso)
                       → Patient Data Service     (busca dados brutos no banco)
                       → Data Transform Service   (ESTE SERVIÇO — transforma e censura)
```

Este serviço:
- **Recebe**: dados brutos (linhas de `patients`, `encounters`, `clinical_events`) + um JWT do usuário, via metadata da chamada gRPC.
- **Devolve**: os mesmos dados convertidos para recursos FHIR (`Patient`, `Encounter`, `Condition`, `Observation`, `MedicationRequest`), já censurados conforme o nível de acesso do token.

Este serviço **não** consulta banco de dados e **não** decide se o usuário pode acessar aquele paciente específico — essas responsabilidades são do Patient Data Service e do Authorization Service, respectivamente.

---

## 2. Níveis de acesso

O token JWT carrega 4 flags booleanas independentes. O serviço resolve qual nível vale por ordem de prioridade (o mais permissivo prevalece):

| Nível | Quem usa | O que é exposto |
|---|---|---|
| `FULL` | Médicos | Todos os dados, sem restrição |
| `PARTIAL` | Estagiários | Iniciais do nome, ano de nascimento, sem CPF/CNS |
| `ANONYMIZED` | Pesquisadores (consulta individual anonimizada) | ID pseudonimizado (hash), sem nome/CPF/CNS/data exata |
| `AGGREGATED` | Pesquisadores (consulta de coorte) | Apenas estatísticas agregadas, nenhum paciente identificável |

---

## 3. Estrutura do projeto

```
datatransform/
├── proto/                      # contrato gRPC (.proto) e stubs gerados
├── src/
│   ├── server.py                # ponto de entrada — sobe o servidor gRPC
│   ├── config.py                # leitura de variáveis de ambiente
│   ├── grpc_service.py          # implementação das RPCs
│   ├── auth/                    # decodificação de JWT + interceptor de autenticação
│   ├── fhir/                    # conversão de dado bruto → recurso FHIR
│   ├── redaction/                # política de censura/pseudonimização por nível
│   ├── aggregation/              # estatísticas de coorte (nível AGGREGATED)
│   └── observability/            # métricas Prometheus
├── tests/
│   ├── unit/                     # testes isolados, sem gRPC
│   └── integration/              # testes com servidor gRPC real, in-process
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 4. Como rodar localmente

### Pré-requisitos
- Python 3.11+
- `make`

### Passo a passo

```bash
# 1. Instala dependências (cria venv automaticamente)
make install

# 2. Gera os stubs Python a partir do .proto
make proto

# 3. Roda os testes (unitários + integração)
make test

# 4. Sobe o servidor localmente
make run
```

O servidor gRPC sobe na porta **50053**, e o endpoint de métricas Prometheus sobe na porta **9103** (`http://localhost:9103/metrics`).

### Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GRPC_PORT` | Não (default `50053`) | Porta do servidor gRPC |
| `METRICS_PORT` | Não (default `9103`) | Porta do endpoint `/metrics` |
| `JWT_SECRET` | **Sim** | Chave HS256 compartilhada com o serviço que emite os tokens (Auth Service) |
| `PSEUDONYMIZE_SALT` | **Sim** | Salt usado para gerar os hashes de pseudonimização (nível `ANONYMIZED`) |

`make run` já define valores de desenvolvimento (`dev-secret`, `dev-salt`) automaticamente — **não usar em produção**.

---

## 5. Executando com Docker

```bash
make docker-build   # constrói a imagem
make docker-up       # sobe via docker-compose (usa .env se existir)
```

Variáveis `JWT_SECRET` e `PSEUDONYMIZE_SALT` podem ser passadas via `.env` na raiz do projeto ou exportadas no shell antes do `docker compose up`.

---

## 6. Autenticação — como chamar este serviço

O JWT **não vai dentro da mensagem** — ele é enviado como metadata da chamada gRPC, no header `authorization`:

```python
metadata = [("authorization", f"Bearer {jwt_token}")]
response = stub.Transform(request, metadata=metadata)
```

### Formato esperado do JWT (HS256)

```json
{
  "FULL": true,
  "PARTIAL": false,
  "ANONYMIZED": false,
  "AGGREGATED": false,
  "exp": 1760000000
}
```

### Erros de autenticação

Todo erro relacionado a token vem com o código gRPC padrão (`UNAUTHENTICATED` ou `PERMISSION_DENIED`) **e** um motivo específico no trailing metadata (`error-reason`), pra permitir tratamento fino do lado do cliente:

| Situação | Código gRPC | `error-reason` |
|---|---|---|
| Nenhum token enviado | `UNAUTHENTICATED` | `TOKEN_MISSING` |
| Token expirado | `UNAUTHENTICATED` | `TOKEN_EXPIRED` |
| Assinatura inválida / token corrompido | `UNAUTHENTICATED` | `TOKEN_INVALID` |
| Token válido, mas nenhuma flag concede acesso | `PERMISSION_DENIED` | `NO_ACCESS_LEVEL` |

Exemplo de tratamento no cliente:

```python
try:
    response = stub.Transform(request, metadata=metadata)
except grpc.RpcError as e:
    reason = dict(e.trailing_metadata() or []).get("error-reason")
    if reason == "TOKEN_EXPIRED":
        ...  # renovar token e repetir a chamada
    elif reason == "TOKEN_INVALID":
        ...  # forçar novo login
```

Guia completo com todos os tipos de consulta (Resumo Clínico, Histórico, atendimentos isolados, exames, medicamentos, coorte de pesquisa) está em [`INTEGRATION.md`](./INTEGRATION.md).

---

## 7. Testes

```bash
make test-unit          # só unitários (rápidos, sem gRPC)
make test-integration    # só integração (sobe servidor gRPC real)
make test                 # tudo, com relatório de cobertura
```

### O que é coberto

- **Unitários**: decodificação de JWT (válido/expirado/inválido), resolução de nível de acesso, conversão de cada tipo de recurso FHIR, política de redação por nível, pseudonimização, cálculo de agregações.
- **Integração**: fluxo completo via servidor gRPC real — autenticação, autorização por nível, montagem do Bundle FHIR, erros de token.

---

## 8. Observabilidade

O serviço expõe métricas Prometheus em `/metrics` (porta 9103):

| Métrica | Tipo | Labels | O que mede |
|---|---|---|---|
| `data_transform_requests_total` | Counter | `access_level`, `rpc` | Total de transformações realizadas |
| `data_transform_errors_total` | Counter | `error_type` | Total de erros por tipo |
| `data_transform_latency_seconds` | Histogram | `rpc` | Distribuição de latência das transformações |

### Consultando localmente

```bash
curl localhost:9103/metrics
```

## 9. Contrato gRPC (resumo)

```protobuf
service DataTransform {
  rpc Transform (TransformRequest) returns (TransformResponse);
  rpc TransformAggregate (AggregateRequest) returns (AggregateResponse);
}
```

- `Transform`: consulta sobre um paciente específico (médico/estagiário). Todos os campos da requisição são opcionais — envie só o que a consulta precisa (ex: só `encounters` para listar atendimentos).
- `TransformAggregate`: consulta de coorte de pesquisa. Exige token com nível `AGGREGATED`.

Contrato completo em [`proto/data_transform.proto`](./proto/data_transform.proto).

---

## 10. Decisões de arquitetura relevantes

- **Autenticação via interceptor gRPC**, não dentro de cada método — garante que nenhuma RPC nova possa "esquecer" de validar o token.
- **Token via metadata, não no payload** — separa preocupação de transporte (quem está chamando) de dados de negócio (o que está sendo transformado).
- **Redação declarativa** (`_DROP_FIELDS` em `redaction/levels.py`) — a política de cada nível fica numa tabela única, fácil de auditar contra a especificação, em vez de espalhada em condicionais.
- **Pseudonimização com salt secreto** — hash SHA-256 determinístico, mas não recalculável fora do sistema sem conhecer o salt.
- **Fail-closed**: qualquer ambiguidade (token sem nível, campo ausente) resulta em negar acesso, nunca em conceder por padrão.

---

## 11. Referências

- HL7 FHIR: https://www.hl7.org/fhir/
- gRPC Python: https://grpc.io/docs/languages/python/
- Prometheus: https://prometheus.io/