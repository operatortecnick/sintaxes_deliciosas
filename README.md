# API Modificador de Créditos

API completa para integração e modificação de créditos com saída perfeita e real.

## Funcionalidades

- ✅ **Criação de Créditos**: Adicione novos créditos ao sistema
- ✅ **Consulta de Créditos**: Busque créditos específicos ou por usuário
- ✅ **Modificação de Créditos**: Atualize quantidade, status e descrição
- ✅ **Remoção de Créditos**: Delete créditos do sistema
- ✅ **Saldo de Usuário**: Calcule o saldo total e detalhado por usuário
- ✅ **Transferência entre Usuários**: Transfira créditos entre contas
- ✅ **Histórico de Transações**: Acompanhe todas as operações realizadas
- ✅ **Validação Completa**: Validação de dados e tratamento de erros
- ✅ **Documentação Automática**: Swagger UI e ReDoc incluídos

## Instalação e Execução

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a API

```bash
python main.py
```

A API estará disponível em: `http://localhost:8000`

### 3. Documentação

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints da API

### Créditos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/credits` | Criar novo crédito |
| GET | `/credits/{credit_id}` | Buscar crédito por ID |
| PUT | `/credits/{credit_id}` | Atualizar crédito |
| DELETE | `/credits/{credit_id}` | Remover crédito |

### Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/users/{user_id}/credits` | Listar créditos do usuário |
| GET | `/users/{user_id}/balance` | Obter saldo do usuário |
| GET | `/users/{user_id}/transactions` | Histórico de transações |

### Transferências

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/transfers` | Transferir créditos entre usuários |

### Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Status de saúde |

## Tipos de Crédito

- **purchase**: Créditos comprados
- **bonus**: Créditos de bônus
- **refund**: Créditos de reembolso
- **transfer**: Créditos transferidos

## Status de Crédito

- **active**: Crédito ativo e utilizável
- **pending**: Crédito pendente de aprovação
- **expired**: Crédito expirado
- **used**: Crédito já utilizado

## Exemplos de Uso

### Criar um Crédito

```bash
curl -X POST "http://localhost:8000/credits" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123",
       "amount": 100.0,
       "credit_type": "purchase",
       "description": "Compra de créditos"
     }'
```

### Consultar Saldo

```bash
curl "http://localhost:8000/users/user123/balance"
```

### Transferir Créditos

```bash
curl -X POST "http://localhost:8000/transfers?from_user_id=user1&to_user_id=user2&amount=50.0"
```

## Testes

Execute os testes com:

```bash
pytest test_api.py -v
```

## Estrutura do Projeto

```
sintaxes_deliciosas/
├── main.py           # API principal
├── models.py         # Modelos de dados
├── storage.py        # Sistema de armazenamento
├── test_api.py       # Testes da API
├── requirements.txt  # Dependências
└── README.md         # Esta documentação
```

## Características Técnicas

- **Framework**: FastAPI (moderno e performático)
- **Validação**: Pydantic (validação automática de dados)
- **Documentação**: Automática com OpenAPI/Swagger
- **Testes**: Pytest (cobertura completa)
- **Tratamento de Erros**: Sistema robusto de error handling
- **Logs de Transação**: Auditoria completa de operações

## Próximos Passos (Produção)

Para uso em produção, considere:

1. **Banco de Dados**: Substituir storage em memória por PostgreSQL/MySQL
2. **Autenticação**: Implementar JWT ou OAuth2
3. **Rate Limiting**: Controle de taxa de requisições
4. **Caching**: Redis para performance
5. **Monitoramento**: Logs estruturados e métricas
6. **Deploy**: Docker + Kubernetes ou similar

---

**API Modificador de Créditos** - Saída perfeita e real ✨
