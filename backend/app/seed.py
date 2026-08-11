import json, random, sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from sqlalchemy import select
from .database import Base, SessionLocal, engine
from .models import Reward, Transaction, Wallet

MERCHANTS = [("Fresh Basket", "Groceries"), ("Metro Ride", "Transport"), ("Cineplex", "Entertainment"), ("Cloud Nine Cafe", "Dining"), ("MediCare", "Health"), ("Urban Threads", "Shopping"), ("PayWave", "Bills")]
REWARDS = [("₹100 Amazon voucher", "A digital voucher delivered instantly.", 850), ("₹250 bill cashback", "Credit towards your next statement.", 2000), ("Movie night", "Two cinema tickets.", 3200), ("₹500 travel voucher", "A travel voucher for your next getaway.", 4800), ("Premium coffee", "A café voucher for any drink.", 650)]

def normalize(row, i):
    merchant = row.get("merchant") or row.get("merchant_name") or f"Merchant {i}"
    raw_date = row.get("date") or row.get("occurred_on") or date.today().isoformat()
    return Transaction(merchant=merchant, category=row.get("category", "Other"), amount=Decimal(str(row.get("amount", 0))).copy_abs(), occurred_on=date.fromisoformat(str(raw_date)[:10]), status=str(row.get("status", "successful")).lower(), card_last4=str(row.get("card_last4", "4242"))[-4:], notes=row.get("notes"))

def generated():
    rng = random.Random(42); today = date.today()
    for i in range(10_000):
        merchant, category = rng.choice(MERCHANTS)
        yield Transaction(merchant=merchant, category=category, amount=Decimal(str(round(rng.uniform(90, 8500), 2))), occurred_on=today-timedelta(days=rng.randrange(540)), status=rng.choices(["successful", "pending", "failed"], [88,8,4])[0], card_last4=str(rng.choice(["4242", "8891", "0927"])), notes=None)

def main(source: str | None = None):
    Base.metadata.create_all(engine)
    with SessionLocal.begin() as session:
        if session.scalar(select(Transaction.id).limit(1)): print("Database already seeded; no changes made."); return
        if source and Path(source).exists():
            rows = json.loads(Path(source).read_text())
            records = [normalize(row, i) for i,row in enumerate(rows, 1)]
        else: records = list(generated())
        session.add_all(records)
        coins = sum(int(t.amount // 100) for t in records if t.status == "successful")
        session.add(Wallet(id=1, balance=coins))
        session.add_all([Reward(name=n, description=d, cost=c) for n,d,c in REWARDS])
        print(f"Seeded {len(records)} transactions and {coins} coins.")
if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else None)
