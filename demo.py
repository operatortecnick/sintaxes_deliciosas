#!/usr/bin/env python3
"""
Exemplo de uso da API Modificador de Créditos
Demonstra todas as funcionalidades principais
"""

import requests
import json
import time

# URL base da API
BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Imprime a resposta de forma formatada"""
    print(f"\n{'='*50}")
    print(f"📋 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)


def main():
    print("🚀 Demonstração da API Modificador de Créditos")
    print("Testando todas as funcionalidades...")

    # 1. Verificar status da API
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Status da API")

    # 2. Criar créditos para diferentes usuários
    users_credits = [
        {
            "user_id": "empresario_123",
            "amount": 500.0,
            "credit_type": "purchase",
            "description": "Compra inicial de créditos"
        },
        {
            "user_id": "freelancer_456",
            "amount": 200.0,
            "credit_type": "bonus",
            "description": "Bônus de primeira utilização"
        },
        {
            "user_id": "cliente_789",
            "amount": 150.0,
            "credit_type": "refund",
            "description": "Reembolso de transação"
        }
    ]

    credit_ids = []
    for credit_data in users_credits:
        response = requests.post(f"{BASE_URL}/credits", json=credit_data)
        print_response(response, f"Criando crédito para {credit_data['user_id']}")
        if response.status_code == 201:
            credit_ids.append(response.json()["data"]["credit"]["id"])

    # 3. Consultar saldo dos usuários
    for user_id in ["empresario_123", "freelancer_456", "cliente_789"]:
        response = requests.get(f"{BASE_URL}/users/{user_id}/balance")
        print_response(response, f"Saldo do {user_id}")

    # 4. Listar créditos de um usuário específico
    response = requests.get(f"{BASE_URL}/users/empresario_123/credits")
    print_response(response, "Créditos do empresario_123")

    # 5. Atualizar um crédito
    if credit_ids:
        update_data = {
            "amount": 600.0,
            "description": "Crédito atualizado com bônus",
            "status": "active"
        }
        response = requests.put(f"{BASE_URL}/credits/{credit_ids[0]}", json=update_data)
        print_response(response, "Atualizando crédito")

    # 6. Transferir créditos entre usuários
    response = requests.post(
        f"{BASE_URL}/transfers",
        params={
            "from_user_id": "empresario_123",
            "to_user_id": "freelancer_456",
            "amount": 100.0
        }
    )
    print_response(response, "Transferência de créditos")

    # 7. Verificar saldos após transferência
    for user_id in ["empresario_123", "freelancer_456"]:
        response = requests.get(f"{BASE_URL}/users/{user_id}/balance")
        print_response(response, f"Saldo após transferência - {user_id}")

    # 8. Histórico de transações
    response = requests.get(f"{BASE_URL}/users/freelancer_456/transactions")
    print_response(response, "Histórico de transações do freelancer_456")

    # 9. Buscar um crédito específico
    if credit_ids:
        response = requests.get(f"{BASE_URL}/credits/{credit_ids[0]}")
        print_response(response, "Consultando crédito específico")

    # 10. Status de saúde da API
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Status de saúde da API")

    print(f"\n{'🎉'*50}")
    print("✅ Demonstração concluída com sucesso!")
    print("🌟 API Modificador de Créditos funcionando perfeitamente!")
    print(f"{'🎉'*50}")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        print("Execute: python main.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")