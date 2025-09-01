from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class CreditType(str, Enum):
    PURCHASE = "purchase"
    BONUS = "bonus"
    REFUND = "refund"
    TRANSFER = "transfer"


class CreditStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    EXPIRED = "expired"
    USED = "used"


class CreditBase(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    amount: float = Field(..., gt=0, description="Quantidade de créditos")
    credit_type: CreditType = Field(..., description="Tipo do crédito")
    description: Optional[str] = Field(None, description="Descrição do crédito")
    expires_at: Optional[datetime] = Field(None, description="Data de expiração")


class CreditCreate(CreditBase):
    pass


class CreditUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Nova quantidade de créditos")
    status: Optional[CreditStatus] = Field(None, description="Novo status")
    description: Optional[str] = Field(None, description="Nova descrição")
    expires_at: Optional[datetime] = Field(None, description="Nova data de expiração")


class Credit(CreditBase):
    id: str = Field(..., description="ID único do crédito")
    status: CreditStatus = Field(default=CreditStatus.ACTIVE, description="Status do crédito")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação")
    updated_at: datetime = Field(default_factory=datetime.now, description="Data de atualização")

    class Config:
        from_attributes = True


class CreditBalance(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    total_balance: float = Field(..., description="Saldo total de créditos")
    active_credits: int = Field(..., description="Número de créditos ativos")
    pending_credits: int = Field(..., description="Número de créditos pendentes")
    expired_credits: int = Field(..., description="Número de créditos expirados")


class CreditTransaction(BaseModel):
    id: str = Field(..., description="ID da transação")
    user_id: str = Field(..., description="ID do usuário")
    amount: float = Field(..., description="Quantidade de créditos")
    operation: str = Field(..., description="Operação realizada")
    description: str = Field(..., description="Descrição da transação")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da transação")


class APIResponse(BaseModel):
    success: bool = Field(..., description="Indica se a operação foi bem-sucedida")
    message: str = Field(..., description="Mensagem da resposta")
    data: Optional[dict] = Field(None, description="Dados da resposta")


class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Indica falha na operação")
    error: str = Field(..., description="Descrição do erro")
    error_code: Optional[str] = Field(None, description="Código do erro")