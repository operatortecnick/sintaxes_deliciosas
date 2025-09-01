import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from models import Credit, CreditCreate, CreditUpdate, CreditStatus, CreditType, CreditBalance, CreditTransaction


class CreditStorage:
    """Armazenamento em memória para créditos - em produção seria um banco de dados"""
    
    def __init__(self):
        self.credits: Dict[str, Credit] = {}
        self.transactions: List[CreditTransaction] = []
    
    def create_credit(self, credit_data: CreditCreate) -> Credit:
        """Cria um novo crédito"""
        credit_id = str(uuid.uuid4())
        credit = Credit(
            id=credit_id,
            **credit_data.dict(),
            status=CreditStatus.ACTIVE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.credits[credit_id] = credit
        
        # Registra a transação
        transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=credit.user_id,
            amount=credit.amount,
            operation="CREATE",
            description=f"Crédito criado: {credit.description or 'N/A'}"
        )
        self.transactions.append(transaction)
        
        return credit
    
    def get_credit(self, credit_id: str) -> Optional[Credit]:
        """Busca um crédito por ID"""
        return self.credits.get(credit_id)
    
    def get_credits_by_user(self, user_id: str) -> List[Credit]:
        """Busca todos os créditos de um usuário"""
        return [credit for credit in self.credits.values() if credit.user_id == user_id]
    
    def update_credit(self, credit_id: str, update_data: CreditUpdate) -> Optional[Credit]:
        """Atualiza um crédito existente"""
        credit = self.credits.get(credit_id)
        if not credit:
            return None
        
        # Armazena valores antigos para log
        old_amount = credit.amount
        old_status = credit.status
        
        # Atualiza os campos fornecidos
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(credit, field, value)
        
        credit.updated_at = datetime.now()
        
        # Registra a transação
        transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=credit.user_id,
            amount=credit.amount,
            operation="UPDATE",
            description=f"Crédito atualizado de {old_amount} para {credit.amount}, status: {old_status} -> {credit.status}"
        )
        self.transactions.append(transaction)
        
        return credit
    
    def delete_credit(self, credit_id: str) -> bool:
        """Remove um crédito"""
        credit = self.credits.get(credit_id)
        if not credit:
            return False
        
        # Registra a transação antes de deletar
        transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=credit.user_id,
            amount=credit.amount,
            operation="DELETE",
            description=f"Crédito removido: {credit.description or 'N/A'}"
        )
        self.transactions.append(transaction)
        
        del self.credits[credit_id]
        return True
    
    def get_user_balance(self, user_id: str) -> CreditBalance:
        """Calcula o saldo de créditos de um usuário"""
        user_credits = self.get_credits_by_user(user_id)
        
        total_balance = sum(credit.amount for credit in user_credits if credit.status == CreditStatus.ACTIVE)
        active_credits = len([c for c in user_credits if c.status == CreditStatus.ACTIVE])
        pending_credits = len([c for c in user_credits if c.status == CreditStatus.PENDING])
        expired_credits = len([c for c in user_credits if c.status == CreditStatus.EXPIRED])
        
        return CreditBalance(
            user_id=user_id,
            total_balance=total_balance,
            active_credits=active_credits,
            pending_credits=pending_credits,
            expired_credits=expired_credits
        )
    
    def get_user_transactions(self, user_id: str) -> List[CreditTransaction]:
        """Busca todas as transações de um usuário"""
        return [transaction for transaction in self.transactions if transaction.user_id == user_id]
    
    def transfer_credits(self, from_user_id: str, to_user_id: str, amount: float) -> bool:
        """Transfere créditos entre usuários"""
        # Verifica se o usuário tem saldo suficiente
        from_balance = self.get_user_balance(from_user_id)
        if from_balance.total_balance < amount:
            return False
        
        # Deduz créditos do usuário origem
        user_credits = [c for c in self.get_credits_by_user(from_user_id) if c.status == CreditStatus.ACTIVE]
        remaining_amount = amount
        
        for credit in user_credits:
            if remaining_amount <= 0:
                break
            
            if credit.amount <= remaining_amount:
                # Remove todo o crédito
                remaining_amount -= credit.amount
                credit.status = CreditStatus.USED
                credit.updated_at = datetime.now()
            else:
                # Remove parcialmente
                credit.amount -= remaining_amount
                credit.updated_at = datetime.now()
                remaining_amount = 0
        
        # Adiciona créditos ao usuário destino
        transfer_credit = CreditCreate(
            user_id=to_user_id,
            amount=amount,
            credit_type=CreditType.TRANSFER,
            description=f"Transferência recebida de {from_user_id}"
        )
        self.create_credit(transfer_credit)
        
        # Registra as transações
        from_transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=from_user_id,
            amount=-amount,
            operation="TRANSFER_OUT",
            description=f"Transferência enviada para {to_user_id}"
        )
        
        to_transaction = CreditTransaction(
            id=str(uuid.uuid4()),
            user_id=to_user_id,
            amount=amount,
            operation="TRANSFER_IN",
            description=f"Transferência recebida de {from_user_id}"
        )
        
        self.transactions.extend([from_transaction, to_transaction])
        return True


# Instância global do storage (em produção seria injetada como dependência)
credit_storage = CreditStorage()