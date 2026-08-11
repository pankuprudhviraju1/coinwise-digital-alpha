from datetime import date
from decimal import Decimal
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .database import get_session
from .models import Redemption, Reward, Transaction, Wallet
from .schemas import RedeemIn, TransactionOut

app = FastAPI(title="Coinwise API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/transactions")
def transactions(search: str | None = None, category: str | None = None, status: str | None = None,
    date_from: date | None = None, date_to: date | None = None, min_amount: Decimal | None = None,
    max_amount: Decimal | None = None, sort_by: str = Query("occurred_on", pattern="^(occurred_on|amount)$"),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$"), page: int = Query(1, ge=1), page_size: int = Query(50, ge=10, le=100), session: Session = Depends(get_session)):
    stmt = select(Transaction)
    if search: stmt = stmt.where(Transaction.merchant.ilike(f"%{search.strip()}%"))
    if category: stmt = stmt.where(Transaction.category == category)
    if status: stmt = stmt.where(Transaction.status == status)
    if date_from: stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to: stmt = stmt.where(Transaction.occurred_on <= date_to)
    if min_amount is not None: stmt = stmt.where(Transaction.amount >= min_amount)
    if max_amount is not None: stmt = stmt.where(Transaction.amount <= max_amount)
    total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    column = Transaction.occurred_on if sort_by == "occurred_on" else Transaction.amount
    stmt = stmt.order_by(column.desc() if sort_dir == "desc" else column.asc(), Transaction.id.desc()).offset((page-1)*page_size).limit(page_size)
    return {"items": [TransactionOut.model_validate(x).model_dump(mode="json") for x in session.scalars(stmt)], "total": total, "page": page, "page_size": page_size}

@app.get("/api/transactions/{transaction_id}", response_model=TransactionOut)
def transaction(transaction_id: int, session: Session = Depends(get_session)):
    item = session.get(Transaction, transaction_id)
    if not item: raise HTTPException(404, "Transaction not found")
    return item

@app.get("/api/analytics/spending")
def spending(date_from: date | None = None, date_to: date | None = None, session: Session = Depends(get_session)):
    base = [Transaction.status == "successful"]
    if date_from: base.append(Transaction.occurred_on >= date_from)
    if date_to: base.append(Transaction.occurred_on <= date_to)
    by_category = session.execute(select(Transaction.category, func.sum(Transaction.amount)).where(*base).group_by(Transaction.category).order_by(func.sum(Transaction.amount).desc())).all()
    by_month = session.execute(select(func.to_char(Transaction.occurred_on, "YYYY-MM"), func.sum(Transaction.amount)).where(*base).group_by(func.to_char(Transaction.occurred_on, "YYYY-MM")).order_by(func.to_char(Transaction.occurred_on, "YYYY-MM"))).all()
    return {"categories": [{"label": a, "value": b} for a,b in by_category], "months": [{"label": a, "value": b} for a,b in by_month]}

@app.get("/api/rewards/balance")
def balance(session: Session = Depends(get_session)):
    wallet = session.get(Wallet, 1)
    return {"balance": wallet.balance if wallet else 0}

@app.get("/api/rewards/catalog")
def catalog(session: Session = Depends(get_session)):
    return session.scalars(select(Reward).order_by(Reward.cost)).all()

@app.post("/api/rewards/redeem")
def redeem(payload: RedeemIn, session: Session = Depends(get_session)):
    with session.begin():
        wallet = session.scalar(select(Wallet).where(Wallet.id == 1).with_for_update())
        reward = session.get(Reward, payload.reward_id)
        if not reward: raise HTTPException(404, "Reward not found")
        if not wallet or wallet.balance < reward.cost: raise HTTPException(409, "Not enough coins for this reward")
        wallet.balance -= reward.cost
        session.add(Redemption(reward_id=reward.id, cost=reward.cost))
    return {"balance": wallet.balance, "message": f"{reward.name} redeemed"}
