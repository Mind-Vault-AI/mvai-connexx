## 🚀 MVAI CONNEXX - REST API DOCUMENTATIE

**Versie:** 2.0.0
**Base URL:** `https://your-app.fly.dev/api/v1`
**Authenticatie:** API Key (X-API-Key header)

---

## 🔐 Authenticatie

Alle API endpoints vereisen een geldige API key. Je kunt API keys aanmaken via het Customer Dashboard.

**Methode 1: Header (aanbevolen)**
```bash
curl -H "X-API-Key: mvai_xxx..." https://your-app.fly.dev/api/v1/status
```

---

## 📚 API ENDPOINTS

### Health & Status

## 📚 API ENDPOINTS

### Health & Status
#### `GET /api/v1/health`
Health check endpoint (geen authenticatie vereist)

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-27T10:30:00",
  "database": "connected",
  "version": "2.0.0"
}
```

#### `GET /api/v1/status`
Haal account status en statistieken op

**Response:**
```json
{
  "customer": {
    "id": 1,
    "name": "TransLog Nederland BV",
    "status": "active",
    "created_at": "2025-12-27 10:00:00"
  },
  "stats": {
    "total_logs": 150,
    "logs_today": 12,
    "logs_week": 45,
    "first_log": "2025-12-20 14:30:00",
    "last_log": "2025-12-27 10:25:00"
  }
}
```

---

### Logs Endpoints

#### `GET /api/v1/logs`
Haal logs op voor jouw account

**Parameters:**
- `limit` (optional): Max aantal logs (default: 100, max: 1000)
- `offset` (optional): Offset voor paginatie (default: 0)

**Request:**
```bash
curl -H "X-API-Key: mvai_xxx..." \
  "https://your-app.fly.dev/api/v1/logs?limit=10&offset=0"
```

**Response:**
```json
{
  "logs": [
    {
      "id": 150,
      "customer_id": 1,
      "ip_address": "192.168.1.100",
      "timestamp": "2025-12-27 10:25:00",
      "data": "{\"action\":\"container_arrived\",\"container_id\":\"CONT-1234\"}"
    }
  ],
  "count": 10,
  "limit": 10,
  "offset": 0
}
```

#### `POST /api/v1/logs`
Maak nieuwe log entry aan

**Request:**
```bash
curl -X POST \
  -H "X-API-Key: mvai_xxx..." \
  -H "Content-Type: application/json" \
  -d '{"action":"shipment_sent","tracking":"TR12345"}' \
  https://your-app.fly.dev/api/v1/logs
```

**Response:**
```json
{
  "success": true,
  "log_id": 151,
  "timestamp": "2025-12-27T10:30:00"
}
```

#### `GET /api/v1/logs/<log_id>`
Haal specifieke log op

**Response:**
```json
{
  "id": 150,
  "customer_id": 1,
  "ip_address": "192.168.1.100",
  "timestamp": "2025-12-27 10:25:00",
  "data": "{...}"
}
```

#### `GET /api/v1/logs/search`
Zoek in logs

**Parameters:**
- `q` (required): Zoekterm

**Request:**
```bash
curl -H "X-API-Key: mvai_xxx..." \
  "https://your-app.fly.dev/api/v1/logs/search?q=container"
```

**Response:**
```json
{
  "query": "container",
  "results": [...],
  "count": 5
}
```

#### `POST /api/v1/logs/batch`
Maak meerdere logs in één request (max 100)

**Request:**
```bash
curl -X POST \
  -H "X-API-Key: mvai_xxx..." \
  -H "Content-Type: application/json" \
  -d '{
    "logs": [
      {"action": "item1"},
      {"action": "item2"},
      {"action": "item3"}
    ]
  }' \
  https://your-app.fly.dev/api/v1/logs/batch
```

**Response:**
```json
{
  "success": true,
  "created_count": 3,
  "created_ids": [151, 152, 153],
  "errors": []
}
```

---

### Analytics Endpoints

#### `GET /api/v1/analytics/stats`
Haal algemene statistieken op

**Response:**
```json
{
  "total_logs": 150,
  "logs_today": 12,
  "logs_week": 45,
  "first_log": "2025-12-20 14:30:00",
  "last_log": "2025-12-27 10:25:00"
}
```

#### `GET /api/v1/analytics/daily`
Haal dagelijkse activiteit op

**Parameters:**
- `days` (optional): Aantal dagen (default: 30, max: 365)

**Response:**
```json
{
  "period": "30 days",
  "data": [
    {"date": "2025-12-01", "count": 5},
    {"date": "2025-12-02", "count": 8},
    ...
  ]
}
```

---

### Export Endpoints

#### `GET /api/v1/export/json`
Export alle data als JSON

**Parameters:**
- `limit` (optional): Max aantal logs (default: 10000, max: 100000)

**Response:**
```json
{
  "customer": {
    "id": 1,
    "name": "TransLog Nederland BV"
  },
  "exported_at": "2025-12-27T10:30:00",
  "log_count": 150,
  "logs": [...]
}
```

---

### API Key Management

#### `GET /api/v1/keys`
List alle API keys voor jouw account

**Response:**
```json
{
  "keys": [
    {
      "id": 1,
      "key_value": "mvai_xxx...",
      "name": "Production Key",
      "is_active": true,
      "created_at": "2025-12-27 10:00:00",
      "last_used_at": "2025-12-27 10:25:00"
    }
  ],
  "count": 1
}
```

---

## 📊 Rate Limiting

**Default limits:**
- 200 requests per dag
- 50 requests per uur

Bij overschrijding: HTTP 429 Too Many Requests

---

## 🔧 Error Codes

| Code | Betekenis |
|------|-----------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized (invalid API key) |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

**Error Response Format:**
```json
{
  "error": "Invalid API key",
  "message": "API key is invalid or has been revoked"
}
```

---

## 💡 Code Voorbeelden

### Python
```python
import requests

API_KEY = "mvai_xxx..."
BASE_URL = "https://your-app.fly.dev/api/v1"

headers = {"X-API-Key": API_KEY}

# Haal logs op
response = requests.get(f"{BASE_URL}/logs", headers=headers)
logs = response.json()

# Maak nieuwe log
data = {"action": "shipment_sent", "tracking": "TR12345"}
response = requests.post(f"{BASE_URL}/logs", json=data, headers=headers)
```

### JavaScript (Node.js)
```javascript
const axios = require('axios');

const API_KEY = 'mvai_xxx...';
const BASE_URL = 'https://your-app.fly.dev/api/v1';

const headers = { 'X-API-Key': API_KEY };

// Haal logs op
const logs = await axios.get(`${BASE_URL}/logs`, { headers });

// Maak nieuwe log
const data = { action: 'shipment_sent', tracking: 'TR12345' };
await axios.post(`${BASE_URL}/logs`, data, { headers });
```

### cURL
```bash
# Haal status op
curl -H "X-API-Key: mvai_xxx..." \
  https://your-app.fly.dev/api/v1/status

# Maak log
curl -X POST \
  -H "X-API-Key: mvai_xxx..." \
  -H "Content-Type: application/json" \
  -d '{"action":"test"}' \
  https://your-app.fly.dev/api/v1/logs
```

---

## 🔒 Best Practices

1. **Beveilig je API keys**: Sla keys nooit op in version control
2. **Gebruik HTTPS**: Altijd encryptie voor API calls
3. **Rate limiting**: Implementeer exponential backoff bij 429 errors
4. **Error handling**: Altijd HTTP status codes checken
5. **Batch operations**: Gebruik `/logs/batch` voor meerdere logs tegelijk

---

## 📞 Support

Vragen over de API?
- GitHub Issues: https://github.com/Mind-Vault-AI/mvai-connexx/issues
- Email: support@mindvault.ai

---

**MVAI Connexx API v2.0.0** | Enterprise Multi-Tenant Platform
