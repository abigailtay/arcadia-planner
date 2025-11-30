# Budget Analytics Documentation

## /analytics Endpoint

- **GET /analytics**
- Optional query params: `type` (`expense`/`income`), `category`

**Response**
{"success": true,
"summary": 
{"sum": 420.0,
"average": 140.0,
"by_category": 
{"Food": {"sum": 300, "count": 2},
"Transport": {"sum": 120, "count": 1}
}
}
}

- Returns `summary: null` if no data matches.

**Validation**
- Only allowed types: expense, income.
- Category must be a string.

**Examples**
- `/analytics?type=expense`
- `/analytics?category=Food`
