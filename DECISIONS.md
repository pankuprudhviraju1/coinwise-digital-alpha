# Technical decisions

- **Server-side data operations:** PostgreSQL indexes and paginated API responses avoid transferring 10,000 records for every interaction.
- **Offset pagination:** predictable page navigation is sufficient for the assignment; cursor pagination would be preferable for an unbounded feed.
- **SQLAlchemy Core-style query composition:** keeps filter logic readable and parameterized without hiding the SQL model.
- **Atomic redemption:** `SELECT ... FOR UPDATE` locks the wallet inside a single database transaction before inserting a redemption.
- **No table component library:** the table is semantic HTML plus authored CSS, including sticky headers and narrow-screen fallbacks.
