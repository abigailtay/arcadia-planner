# Budget API Documentation

## Endpoints

### Create Transaction
POST /transactions

{
"name": "Groceries",
"amount": 150.0,
"category": "Food",
"type": "expense"
}


### Update Transaction
PUT /transactions/<transactionId>

Body: Any subset of above fields

### View Transaction
GET /transactions/<transactionId>

### List Transactions
GET /transactions

### Delete Transaction
DELETE /transactions/<transactionId>

Success response (all endpoints):
{ "success": true }

