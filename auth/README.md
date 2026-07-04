# Auth Service

Este diretório contém o microsserviço de autenticação do projeto, implementado com gRPC em Python.

## O que é

O serviço Auth fornece endpoints para:
- Login de usuários
- Geração e renovação de tokens de acesso
- Logout de sessões

A comunicação entre cliente e servidor é definida no arquivo de contrato gRPC [proto/auth.proto](proto/auth.proto).

## Como rodar

1. Entre na pasta do serviço:
   ```bash
   cd auth
   ```

2. Ative o ambiente virtual, se ainda não estiver ativo:
   ```bash
   source venv/bin/activate
   ```

3. Execute o servidor:
   ```bash
   python app/AuthService.py
   ```

O servidor ficará disponível para conexões gRPC na porta padrão configurada no projeto.

## Como rodar os testes

Os testes estão organizados em pastas de unidade e integração.

Para executar todos os testes:
```bash
pytest
```

Para executar apenas os testes de integração:
```bash
pytest tests/integration
```

Para executar um arquivo específico:
```bash
pytest tests/integration/test_login.py -vv
```

## Arquivo .proto

O contrato gRPC está em [proto/auth.proto](proto/auth.proto).

Ele define os métodos e mensagens usados pelo serviço, incluindo:
- Login
- RefreshToken
- Logout

Se for necessário atualizar o contrato, é preciso regerar os arquivos Python gerados a partir do proto. O script disponível é:
```bash
./gera_proto.sh
```

## Formato do JWT

Os tokens emitidos pelo serviço são JWTs em formato HS256. O payload contém:
- `exp`: timestamp de expiração
- `ANONYMIZED`: permissão booleana
- `AGGREGATED`: permissão booleana
- `PARTIAL`: permissão booleana
- `FULL`: permissão booleana

Exemplo de payload:
```json
{
  "ANONYMIZED": false,
  "AGGREGATED": false,
  "PARTIAL": false,
  "FULL": true,
  "exp": 1760000000
}
```

Exemplo de código em Python para decodificar e validar o token:
```python
import jwt
from app.AuthService import SECRET

token = "<token_jwt_aqui>"

try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    print(payload)

    if payload.get("FULL") is True:
        print("Usuário possui permissão FULL")
    else:
        print("Usuário não possui permissão FULL")

except jwt.ExpiredSignatureError:
    print("Token expirado")
except jwt.InvalidTokenError:
    print("Token inválido")
```

## Banco de dados

Atualmente, a conexão com um banco de dados real ainda não está implementada.
Para permitir o funcionamento do serviço em ambiente de desenvolvimento e testes, foi criada a classe [app/Memory.py](app/Memory.py) como solução temporária, usando uma implementação em memória para armazenar usuários e estado de login.
