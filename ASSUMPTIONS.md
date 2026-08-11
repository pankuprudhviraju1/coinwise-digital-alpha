# Product assumptions

- Currency is INR and a successful payment earns `floor(amount / 100)` coins. Failed and pending payments earn none.
- A transaction earns coins once at ingestion; redemptions never recalculate its reward.
- A redeemed reward is recorded as an immutable ledger entry. Concurrent requests lock the balance row, so it cannot go negative.
- Category analytics reflect the active date range but do not mirror the category filter, so a category slice remains meaningful and clickable.
- Source timestamps arrive in ISO, Unix-millisecond, and `DD/MM/YYYY HH:MM:SS` forms; the seed normalizes each to a calendar date. Blank/missing categories become `Uncategorized`, and `SUCCESS` becomes the API's `successful` status.
