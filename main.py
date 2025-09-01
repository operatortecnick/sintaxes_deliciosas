from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime

from models import (
    Credit, CreditCreate, CreditUpdate, CreditBalance, 
    CreditTransaction, APIResponse, ErrorResponse, CreditStatus
)
from storage import credit_storage

app = FastAPI(
    title="API Modificador de Créditos",
    description="API para integração e modificação de créditos com saída perfeita e real",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global para exceções"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=f"Erro interno do servidor: {str(exc)}",
            error_code="INTERNAL_ERROR"
        ).dict()
    )


@app.get("/", response_model=APIResponse)
async def root():
    """Endpoint raiz da API"""
    return APIResponse(
        success=True,
        message="API Modificador de Créditos está funcionando perfeitamente!",
        data={"version": "1.0.0", "status": "active"}
    )


@app.post("/credits", response_model=APIResponse, status_code=201)
async def create_credit(credit_data: CreditCreate):
    """Cria um novo crédito"""
    try:
        credit = credit_storage.create_credit(credit_data)
        return APIResponse(
            success=True,
            message="Crédito criado com sucesso",
            data={"credit": credit.dict()}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar crédito: {str(e)}")


@app.get("/credits/{credit_id}", response_model=APIResponse)
async def get_credit(
    credit_id: str = Path(..., description="ID do crédito")
):
    """Busca um crédito específico por ID"""
    credit = credit_storage.get_credit(credit_id)
    if not credit:
        raise HTTPException(status_code=404, detail="Crédito não encontrado")
    
    return APIResponse(
        success=True,
        message="Crédito encontrado",
        data={"credit": credit.dict()}
    )


@app.put("/credits/{credit_id}", response_model=APIResponse)
async def update_credit(
    update_data: CreditUpdate,
    credit_id: str = Path(..., description="ID do crédito")
):
    """Atualiza um crédito existente"""
    credit = credit_storage.update_credit(credit_id, update_data)
    if not credit:
        raise HTTPException(status_code=404, detail="Crédito não encontrado")
    
    return APIResponse(
        success=True,
        message="Crédito atualizado com sucesso",
        data={"credit": credit.dict()}
    )


@app.delete("/credits/{credit_id}", response_model=APIResponse)
async def delete_credit(
    credit_id: str = Path(..., description="ID do crédito")
):
    """Remove um crédito"""
    success = credit_storage.delete_credit(credit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Crédito não encontrado")
    
    return APIResponse(
        success=True,
        message="Crédito removido com sucesso",
        data={"credit_id": credit_id}
    )


@app.get("/users/{user_id}/credits", response_model=APIResponse)
async def get_user_credits(
    user_id: str = Path(..., description="ID do usuário"),
    status: Optional[CreditStatus] = Query(None, description="Filtrar por status")
):
    """Busca todos os créditos de um usuário"""
    credits = credit_storage.get_credits_by_user(user_id)
    
    if status:
        credits = [credit for credit in credits if credit.status == status]
    
    return APIResponse(
        success=True,
        message=f"Encontrados {len(credits)} créditos para o usuário",
        data={
            "user_id": user_id,
            "credits": [credit.dict() for credit in credits],
            "total_credits": len(credits)
        }
    )


@app.get("/users/{user_id}/balance", response_model=APIResponse)
async def get_user_balance(
    user_id: str = Path(..., description="ID do usuário")
):
    """Obtém o saldo de créditos de um usuário"""
    balance = credit_storage.get_user_balance(user_id)
    
    return APIResponse(
        success=True,
        message="Saldo calculado com sucesso",
        data={"balance": balance.dict()}
    )


@app.get("/users/{user_id}/transactions", response_model=APIResponse)
async def get_user_transactions(
    user_id: str = Path(..., description="ID do usuário"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de transações")
):
    """Busca o histórico de transações de um usuário"""
    transactions = credit_storage.get_user_transactions(user_id)
    
    # Ordena por timestamp decrescente e aplica o limite
    transactions = sorted(transactions, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    return APIResponse(
        success=True,
        message=f"Encontradas {len(transactions)} transações",
        data={
            "user_id": user_id,
            "transactions": [transaction.dict() for transaction in transactions],
            "total_transactions": len(transactions)
        }
    )


@app.post("/transfers", response_model=APIResponse)
async def transfer_credits(
    from_user_id: str = Query(..., description="ID do usuário origem"),
    to_user_id: str = Query(..., description="ID do usuário destino"),
    amount: float = Query(..., gt=0, description="Quantidade a transferir")
):
    """Transfere créditos entre usuários"""
    if from_user_id == to_user_id:
        raise HTTPException(status_code=400, detail="Não é possível transferir para o mesmo usuário")
    
    success = credit_storage.transfer_credits(from_user_id, to_user_id, amount)
    
    if not success:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para transferência")
    
    return APIResponse(
        success=True,
        message="Transferência realizada com sucesso",
        data={
            "from_user_id": from_user_id,
            "to_user_id": to_user_id,
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.get("/health", response_model=APIResponse)
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return APIResponse(
        success=True,
        message="API funcionando perfeitamente",
        data={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "total_credits": len(credit_storage.credits),
            "total_transactions": len(credit_storage.transactions)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)