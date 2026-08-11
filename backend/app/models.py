from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    merchant: Mapped[str] = mapped_column(String(160), index=True)
    category: Mapped[str] = mapped_column(String(48), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), index=True)
    occurred_on: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(16), index=True)
    card_last4: Mapped[str] = mapped_column(String(4))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

class Wallet(Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(Integer, default=0)

class Reward(Base):
    __tablename__ = "rewards"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(240))
    cost: Mapped[int] = mapped_column(Integer)

class Redemption(Base):
    __tablename__ = "redemptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    reward_id: Mapped[int] = mapped_column(ForeignKey("rewards.id"))
    cost: Mapped[int] = mapped_column(Integer)
    redeemed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
