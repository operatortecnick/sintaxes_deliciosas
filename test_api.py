import pytest
import asyncio
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app
from storage import credit_storage
from models import CreditType, CreditStatus


@pytest.fixture
def client():
    """Cliente de teste para a API"""
    return TestClient(app)


@pytest.fixture
def clean_storage():
    """Limpa o storage antes de cada teste"""
    credit_storage.credits.clear()
    credit_storage.transactions.clear()
    yield
    credit_storage.credits.clear()
    credit_storage.transactions.clear()


def test_root_endpoint(client, clean_storage):
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "API Modificador de Créditos" in data["message"]


def test_health_endpoint(client, clean_storage):
    """Testa o endpoint de saúde"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_create_credit(client, clean_storage):
    """Testa a criação de créditos"""
    credit_data = {
        "user_id": "user123",
        "amount": 100.0,
        "credit_type": "purchase",
        "description": "Compra de créditos"
    }
    
    response = client.post("/credits", json=credit_data)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["credit"]["amount"] == 100.0
    assert data["data"]["credit"]["user_id"] == "user123"


def test_get_credit(client, clean_storage):
    """Testa a busca de um crédito específico"""
    # Primeiro cria um crédito
    credit_data = {
        "user_id": "user123",
        "amount": 50.0,
        "credit_type": "bonus",
        "description": "Bônus de cadastro"
    }
    
    create_response = client.post("/credits", json=credit_data)
    credit_id = create_response.json()["data"]["credit"]["id"]
    
    # Agora busca o crédito
    response = client.get(f"/credits/{credit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["credit"]["id"] == credit_id


def test_get_nonexistent_credit(client, clean_storage):
    """Testa a busca de um crédito inexistente"""
    response = client.get("/credits/inexistent-id")
    assert response.status_code == 404


def test_update_credit(client, clean_storage):
    """Testa a atualização de créditos"""
    # Cria um crédito
    credit_data = {
        "user_id": "user123",
        "amount": 100.0,
        "credit_type": "purchase"
    }
    
    create_response = client.post("/credits", json=credit_data)
    credit_id = create_response.json()["data"]["credit"]["id"]
    
    # Atualiza o crédito
    update_data = {
        "amount": 150.0,
        "status": "pending",
        "description": "Crédito atualizado"
    }
    
    response = client.put(f"/credits/{credit_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["credit"]["amount"] == 150.0
    assert data["data"]["credit"]["status"] == "pending"


def test_delete_credit(client, clean_storage):
    """Testa a remoção de créditos"""
    # Cria um crédito
    credit_data = {
        "user_id": "user123",
        "amount": 100.0,
        "credit_type": "purchase"
    }
    
    create_response = client.post("/credits", json=credit_data)
    credit_id = create_response.json()["data"]["credit"]["id"]
    
    # Remove o crédito
    response = client.delete(f"/credits/{credit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verifica que o crédito foi removido
    get_response = client.get(f"/credits/{credit_id}")
    assert get_response.status_code == 404


def test_get_user_credits(client, clean_storage):
    """Testa a busca de créditos por usuário"""
    user_id = "user123"
    
    # Cria múltiplos créditos para o usuário
    credits_data = [
        {"user_id": user_id, "amount": 100.0, "credit_type": "purchase"},
        {"user_id": user_id, "amount": 50.0, "credit_type": "bonus"},
        {"user_id": "other_user", "amount": 25.0, "credit_type": "purchase"}
    ]
    
    for credit_data in credits_data:
        client.post("/credits", json=credit_data)
    
    # Busca créditos do usuário
    response = client.get(f"/users/{user_id}/credits")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total_credits"] == 2  # Apenas os do user123


def test_get_user_balance(client, clean_storage):
    """Testa o cálculo do saldo do usuário"""
    user_id = "user123"
    
    # Cria créditos ativos
    active_credits = [
        {"user_id": user_id, "amount": 100.0, "credit_type": "purchase"},
        {"user_id": user_id, "amount": 50.0, "credit_type": "bonus"}
    ]
    
    for credit_data in active_credits:
        client.post("/credits", json=credit_data)
    
    # Busca o saldo
    response = client.get(f"/users/{user_id}/balance")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    balance = data["data"]["balance"]
    assert balance["total_balance"] == 150.0
    assert balance["active_credits"] == 2


def test_transfer_credits(client, clean_storage):
    """Testa a transferência de créditos entre usuários"""
    from_user = "user1"
    to_user = "user2"
    
    # Cria créditos para o usuário origem
    credit_data = {
        "user_id": from_user,
        "amount": 200.0,
        "credit_type": "purchase"
    }
    client.post("/credits", json=credit_data)
    
    # Realiza a transferência
    transfer_amount = 75.0
    response = client.post(
        f"/transfers?from_user_id={from_user}&to_user_id={to_user}&amount={transfer_amount}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["amount"] == transfer_amount
    
    # Verifica os saldos após a transferência
    from_balance_response = client.get(f"/users/{from_user}/balance")
    from_balance = from_balance_response.json()["data"]["balance"]["total_balance"]
    
    to_balance_response = client.get(f"/users/{to_user}/balance")
    to_balance = to_balance_response.json()["data"]["balance"]["total_balance"]
    
    assert from_balance == 125.0  # 200 - 75
    assert to_balance == 75.0


def test_transfer_insufficient_balance(client, clean_storage):
    """Testa transferência com saldo insuficiente"""
    from_user = "user1"
    to_user = "user2"
    
    # Cria crédito insuficiente
    credit_data = {
        "user_id": from_user,
        "amount": 50.0,
        "credit_type": "purchase"
    }
    client.post("/credits", json=credit_data)
    
    # Tenta transferir mais do que tem
    response = client.post(
        f"/transfers?from_user_id={from_user}&to_user_id={to_user}&amount=100.0"
    )
    
    assert response.status_code == 400


def test_transfer_same_user(client, clean_storage):
    """Testa transferência para o mesmo usuário (deve falhar)"""
    user_id = "user1"
    
    response = client.post(
        f"/transfers?from_user_id={user_id}&to_user_id={user_id}&amount=50.0"
    )
    
    assert response.status_code == 400


def test_get_user_transactions(client, clean_storage):
    """Testa o histórico de transações do usuário"""
    user_id = "user123"
    
    # Cria alguns créditos para gerar transações
    credits_data = [
        {"user_id": user_id, "amount": 100.0, "credit_type": "purchase"},
        {"user_id": user_id, "amount": 50.0, "credit_type": "bonus"}
    ]
    
    for credit_data in credits_data:
        client.post("/credits", json=credit_data)
    
    # Busca as transações
    response = client.get(f"/users/{user_id}/transactions")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["transactions"]) == 2


def test_create_credit_validation(client, clean_storage):
    """Testa validação na criação de créditos"""
    # Testa com amount inválido
    invalid_credit_data = {
        "user_id": "user123",
        "amount": -50.0,  # Valor negativo
        "credit_type": "purchase"
    }
    
    response = client.post("/credits", json=invalid_credit_data)
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__])