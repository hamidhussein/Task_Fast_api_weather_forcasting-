# Weather Forecasting API

This project is a simple FastAPI application that lets users register, obtain a
JSON Web Token (JWT) and then query a seven‑day weather forecast for a
specified city.  The forecast data comes from the public WeatherAPI
service.

## Project structure

```
weather_api_project/
├── app/
│   ├── __init__.py        # Marks the app package
│   ├── config.py          # Loads configuration from config.json via Pydantic
│   ├── database.py        # SQLAlchemy engine and session management
│   ├── models.py          # SQLAlchemy models (User table)
│   ├── schemas.py         # Pydantic schemas for requests and responses
│   ├── utils/
│   │   └── auth.py        # Password hashing, JWT creation and current user logic
│   └── routers/
│       ├── auth.py        # `/auth` routes for signup and login
│       └── weather.py     # `/weather` route for forecasts
├── config.json            # Database and API credentials (not checked in)
├── requirements.txt       # Frozen dependencies
└── README.md              # This file
```

## Getting started

These instructions assume you have **Python 3.10+** and **PostgreSQL**
installed locally.  Replace values like database credentials and API keys
with your own.

1. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**

   Copy `config.json` and edit the values:

   ```json
   {
     "database": {
       "database_user": "postgres",
       "database_password": "postgres",
       "database_host": "localhost",
       "database_port": 5432,
       "database_name": "weatherdb"
     },
     "jwt": {
       "secret_key": "CHANGE_ME",    
       "algorithm": "HS256",
       "access_token_expire_minutes": 60
     },
     "weather_api": {
       "api_key": "YOUR_WEATHERAPI_KEY"
     }
   }
   ```

   - The database credentials should point to a PostgreSQL instance.  Create a
     database (e.g. `CREATE DATABASE weatherdb;`) before running the app.
   - The `weather_api.api_key` is your [WeatherAPI](https://www.weatherapi.com/) key.

4. **Initialize the database**

   The database tables are created automatically when the first request
   requiring the model is made.  To pre‑create them, run:

   ```bash
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

5. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.  Interactive
   documentation is at `/docs`.

## API endpoints

### `POST /auth/signup`

Register a new user and get a JWT.

**Request body**

```json
{
  "email": "hamid@example.com",
  "password": "SecretPass123"
}
```

**Response (201)**

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

**cURL**

```bash
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"hamid@example.com","password":"SecretPass123"}'
```

---

### `POST /auth/login`

Authenticate an existing user and get a JWT.  Credentials must match a
registered user.

**Request body**

```json
{
  "email": "hamid@example.com",
  "password": "SecretPass123"
}
```

**Response (200)**

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

**cURL**

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"SecretPass123"}'
```

---

### `GET /weather`

Fetch a seven‑day forecast for a city starting from a given date.  This route
requires authentication via the `Authorization` header.  The `date`
parameter must be in `YYYY-MM-DD` format; `city` is a city name.

**Query parameters**

| Name | Type | Description |
| --- | --- | --- |
| `date` | string | Start date in `YYYY-MM-DD`. Must be today or a future date within 14 days. |
| `city` | string | City name to retrieve the forecast for. |

**Headers**

| Name | Value |
| --- | --- |
| `Authorization` | `Bearer <JWT>` obtained from the signup/login endpoints. |

**Response (200)**

```json
{
  "latitude": 31.52,
  "longitude": 74.36,
  "start_date": "2025-08-18",
  "end_date": "2025-08-24",
  "days": [
    {
      "date": "2025-08-18",
      "temp_max_c": 39.6,
      "temp_min_c": 27.0,
      "precipitation_mm": 1.2,
      "weathercode": 113
    },
    …
  ]
}
```

**cURL**

```bash
TOKEN="<JWT>"
curl -G http://127.0.0.1:8000/weather \
  -H "Authorization: Bearer $TOKEN" \
  --data-urlencode "date=2025-08-18" \
  --data-urlencode "city=Lahore"
```

### About the WeatherAPI

This project uses the [WeatherAPI](https://www.weatherapi.com/) forecast
endpoint.  According to the documentation, each request consists of a
base URL and an API method; for forecasts the method is
`/forecast.json` and the base URL is `http://api.weatherapi.com/v1`【882191624372483†L100-L109】.
The required parameters include your API key (`key`), a location
query (`q`) and the number of forecast days (`days`, between 1 and 14)
【882191624372483†L123-L145】.  If `days` is omitted the API returns only the
current day’s weather.  Our `/weather` route calls this endpoint
with `days=7` to obtain a week‑long forecast.

## Freezing dependencies

To capture all installed packages and their versions after setting up your
virtual environment, run:

```bash
pip freeze > requirements.txt
```

This ensures reproducibility for others installing the project.

