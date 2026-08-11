# AI usage

AI was used as a development accelerator for first-pass component/file structure, endpoint scaffolding, and documentation wording. I reviewed and adapted each output, especially the transaction boundary and query construction.

Discarded/fixed examples:

1. An initial reward calculation treated all transactions as eligible. It was replaced with a `status == successful` guard because pending and failed payments must not award coins.
2. An initial redemption approach updated the balance before recording the redemption. It was replaced with one transaction and a row lock so failures and concurrent requests cannot leave an incorrect balance.
