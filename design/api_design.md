# API Design for Option Pricing Application

## Overview
This document outlines the REST API design for the option pricing application that compares Pareto (Power Law), Black-Scholes-Merton, and market prices for tail options. The API serves 100 traders with approximately 2,000 requests per day.

## Base URL
```
Production: https://api.optionpricing.com/v1
Development: http://localhost:8000/v1
```

## Authentication
All API endpoints require Bearer token authentication.

### Authentication Header
```
Authorization: Bearer <jwt_token>
```

### Get Access Token
**POST** `/auth/token`

**Request Body:**
```json
{
  "username": "trader001",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "trader_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## API Endpoints

### 1. Trader Management

#### Get Trader Profile
**GET** `/traders/profile`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Response:**
```json
{
  "trader_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "trader001",
  "email": "trader001@firm.com",
  "full_name": "John Smith",
  "organization": "ABC Trading",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

#### Update Trader Profile
**PUT** `/traders/profile`

**Request Body:**
```json
{
  "full_name": "John A. Smith",
  "organization": "ABC Trading LLC"
}
```

**Response:**
```json
{
  "message": "Profile updated successfully",
  "trader_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Market Data

#### Get Current Market Data
**GET** `/market-data/{symbol}`

**Example Request:**
```
GET /market-data/SPY
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "market_data_id": "660e8400-e29b-41d4-a716-446655440001",
  "symbol": "SPY",
  "spot_price": 415.50,
  "risk_free_rate": 0.0525,
  "data_date": "2024-01-15",
  "created_at": "2024-01-15T09:30:00Z"
}
```

#### Get Market Data History
**GET** `/market-data/{symbol}/history`

**Query Parameters:**
- `start_date` (optional): YYYY-MM-DD format
- `end_date` (optional): YYYY-MM-DD format
- `limit` (optional): Number of records (default: 30)

**Example Request:**
```
GET /market-data/SPY/history?start_date=2024-01-01&end_date=2024-01-15&limit=10
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "symbol": "SPY",
  "data": [
    {
      "market_data_id": "660e8400-e29b-41d4-a716-446655440001",
      "spot_price": 415.50,
      "risk_free_rate": 0.0525,
      "data_date": "2024-01-15"
    },
    {
      "market_data_id": "660e8400-e29b-41d4-a716-446655440002",
      "spot_price": 412.30,
      "risk_free_rate": 0.0520,
      "data_date": "2024-01-14"
    }
  ],
  "total_records": 10,
  "page": 1
}
```

### 3. Option Pricing

#### Calculate Option Prices
**POST** `/pricing/calculate`

**Request Body:**
```json
{
  "option_details": {
    "symbol": "SPY",
    "strike_price": 420.00,
    "expiration_date": "2024-03-15",
    "option_type": "CALL"
  },
  "market_data": {
    "spot_price": 415.50,
    "risk_free_rate": 0.0525
  },
  "input_parameters": {
    "volatility": 0.20,
    "tail_index_alpha": 3.0,
    "anchor_strike": 410.00,
    "anchor_price": 8.50
  }
}
```

**Response:**
```json
{
  "request_id": "770e8400-e29b-41d4-a716-446655440003",
  "status": "COMPLETED",
  "calculation_time_ms": 125,
  "option_details": {
    "symbol": "SPY",
    "strike_price": 420.00,
    "expiration_date": "2024-03-15",
    "option_type": "CALL",
    "time_to_expiry": 0.16667
  },
  "input_parameters": {
    "spot_price": 415.50,
    "volatility": 0.20,
    "risk_free_rate": 0.0525,
    "tail_index_alpha": 3.0,
    "anchor_strike": 410.00,
    "anchor_price": 8.50
  },
  "results": {
    "bsm_price": 7.25,
    "pareto_price": 8.75,
    "market_reference_price": 8.50
  },
  "comparisons": {
    "pareto_vs_bsm": {
      "difference": 1.50,
      "percentage": 20.69
    },
    "market_vs_bsm": {
      "difference": 1.25,
      "percentage": 17.24
    },
    "pareto_vs_market": {
      "difference": 0.25,
      "percentage": 2.94
    }
  },
  "created_at": "2024-01-15T14:30:00Z"
}
```

#### Batch Calculate Multiple Options
**POST** `/pricing/batch-calculate`

**Request Body:**
```json
{
  "requests": [
    {
      "option_details": {
        "symbol": "SPY",
        "strike_price": 420.00,
        "expiration_date": "2024-03-15",
        "option_type": "CALL"
      },
      "input_parameters": {
        "volatility": 0.20,
        "tail_index_alpha": 3.0,
        "anchor_strike": 410.00,
        "anchor_price": 8.50
      }
    },
    {
      "option_details": {
        "symbol": "SPY",
        "strike_price": 425.00,
        "expiration_date": "2024-03-15",
        "option_type": "CALL"
      },
      "input_parameters": {
        "volatility": 0.22,
        "tail_index_alpha": 3.2,
        "anchor_strike": 415.00,
        "anchor_price": 6.75
      }
    }
  ],
  "market_data": {
    "spot_price": 415.50,
    "risk_free_rate": 0.0525
  }
}
```

**Response:**
```json
{
  "batch_id": "880e8400-e29b-41d4-a716-446655440004",
  "total_requests": 2,
  "completed": 2,
  "failed": 0,
  "results": [
    {
      "request_id": "770e8400-e29b-41d4-a716-446655440005",
      "status": "COMPLETED",
      "option_details": {
        "strike_price": 420.00,
        "option_type": "CALL"
      },
      "results": {
        "bsm_price": 7.25,
        "pareto_price": 8.75,
        "market_reference_price": 8.50
      }
    },
    {
      "request_id": "770e8400-e29b-41d4-a716-446655440006",
      "status": "COMPLETED",
      "option_details": {
        "strike_price": 425.00,
        "option_type": "CALL"
      },
      "results": {
        "bsm_price": 5.80,
        "pareto_price": 7.15,
        "market_reference_price": 6.75
      }
    }
  ]
}
```

### 4. Pricing History

#### Get Pricing Request History
**GET** `/pricing/history`

**Query Parameters:**
- `limit` (optional): Number of records (default: 20, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `symbol` (optional): Filter by symbol
- `start_date` (optional): YYYY-MM-DD format
- `end_date` (optional): YYYY-MM-DD format

**Example Request:**
```
GET /pricing/history?limit=10&symbol=SPY&start_date=2024-01-10
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "total_records": 45,
  "limit": 10,
  "offset": 0,
  "data": [
    {
      "request_id": "770e8400-e29b-41d4-a716-446655440003",
      "option_details": {
        "symbol": "SPY",
        "strike_price": 420.00,
        "expiration_date": "2024-03-15",
        "option_type": "CALL"
      },
      "results": {
        "bsm_price": 7.25,
        "pareto_price": 8.75,
        "market_reference_price": 8.50
      },
      "comparisons": {
        "pareto_vs_bsm_percentage": 20.69
      },
      "created_at": "2024-01-15T14:30:00Z"
    }
  ]
}
```

#### Get Specific Pricing Request
**GET** `/pricing/requests/{request_id}`

**Example Request:**
```
GET /pricing/requests/770e8400-e29b-41d4-a716-446655440003
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "request_id": "770e8400-e29b-41d4-a716-446655440003",
  "trader_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "option_details": {
    "symbol": "SPY",
    "strike_price": 420.00,
    "expiration_date": "2024-03-15",
    "option_type": "CALL",
    "time_to_expiry": 0.16667
  },
  "input_parameters": {
    "spot_price": 415.50,
    "volatility": 0.20,
    "risk_free_rate": 0.0525,
    "tail_index_alpha": 3.0,
    "anchor_strike": 410.00,
    "anchor_price": 8.50
  },
  "results": {
    "bsm_price": 7.25,
    "pareto_price": 8.75,
    "market_reference_price": 8.50
  },
  "comparisons": {
    "pareto_vs_bsm": {
      "difference": 1.50,
      "percentage": 20.69
    },
    "market_vs_bsm": {
      "difference": 1.25,
      "percentage": 17.24
    }
  },
  "created_at": "2024-01-15T14:30:00Z",
  "calculation_time_ms": 125
}
```

### 5. Analytics and Reporting

#### Get Pricing Statistics
**GET** `/analytics/pricing-stats`

**Query Parameters:**
- `period` (optional): "1d", "7d", "30d" (default: "7d")
- `symbol` (optional): Filter by symbol

**Example Request:**
```
GET /analytics/pricing-stats?period=30d&symbol=SPY
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "period": "30d",
  "symbol": "SPY",
  "statistics": {
    "total_requests": 156,
    "average_bsm_price": 12.45,
    "average_pareto_price": 14.78,
    "average_pareto_vs_bsm_percentage": 18.7,
    "price_ranges": {
      "bsm_min": 2.10,
      "bsm_max": 35.60,
      "pareto_min": 2.85,
      "pareto_max": 42.30
    },
    "volatility_stats": {
      "avg_volatility": 0.22,
      "min_volatility": 0.15,
      "max_volatility": 0.35
    },
    "alpha_stats": {
      "avg_alpha": 3.2,
      "min_alpha": 2.5,
      "max_alpha": 4.0
    }
  },
  "generated_at": "2024-01-15T16:00:00Z"
}
```

#### Get Trader Activity Summary
**GET** `/analytics/activity-summary`

**Query Parameters:**
- `period` (optional): "1d", "7d", "30d" (default: "7d")

**Example Request:**
```
GET /analytics/activity-summary?period=7d
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "period": "7d",
  "trader_id": "550e8400-e29b-41d4-a716-446655440000",
  "summary": {
    "total_requests": 28,
    "daily_average": 4.0,
    "symbols_traded": ["SPY", "QQQ", "IWM"],
    "option_types": {
      "CALL": 18,
      "PUT": 10
    },
    "most_active_day": "2024-01-12",
    "most_active_day_requests": 8
  },
  "daily_breakdown": [
    {
      "date": "2024-01-15",
      "requests": 6
    },
    {
      "date": "2024-01-14",
      "requests": 4
    }
  ]
}
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "volatility",
      "issue": "Value must be between 0.01 and 2.0"
    },
    "timestamp": "2024-01-15T14:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Invalid or missing authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Common Error Codes
- `INVALID_TOKEN` - JWT token is invalid or expired
- `VALIDATION_ERROR` - Request data validation failed
- `CALCULATION_ERROR` - Error in option pricing calculation
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `SYMBOL_NOT_FOUND` - Market data not available for symbol
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions

## Rate Limiting
- **Rate Limit**: 100 requests per minute per trader
- **Burst Limit**: 20 requests per 10 seconds
- **Headers Returned**:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1642262400
  ```

## Pagination
For endpoints returning lists, pagination follows this pattern:
- `limit`: Number of items per page (max 100)
- `offset`: Number of items to skip
- Response includes `total_records`, `limit`, and `offset`

## WebSocket API (Real-time Updates)

### Connection
```
wss://api.optionpricing.com/v1/ws?token=<jwt_token>
```

### Subscribe to Real-time Market Data
```json
{
  "action": "subscribe",
  "type": "market_data",
  "symbols": ["SPY", "QQQ"]
}
```

### Real-time Market Data Update
```json
{
  "type": "market_data_update",
  "data": {
    "symbol": "SPY",
    "spot_price": 416.20,
    "timestamp": "2024-01-15T14:35:00Z"
  }
}
```

## API Versioning
- Current version: `v1`
- Version specified in URL path: `/v1/...`
- Backward compatibility maintained for at least 12 months
- Deprecation notices provided 6 months in advance

## Security Considerations
- All endpoints require HTTPS in production
- JWT tokens expire after 1 hour
- Rate limiting to prevent abuse
- Input validation on all parameters
- SQL injection prevention
- CORS configuration for web clients
- API key rotation support for service accounts