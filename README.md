# Weather Forecasting API with FastAPI

This project provides a simple API for user registration, authentication, and retrieving a 7‑day weather forecast. It uses **FastAPI** for the web framework, **SQLAlchemy** for database interactions, **PostgreSQL** as the database backend, and **WeatherAPI.com** for fetching weather data.

## Features

- **User signup** and **login** endpoints with hashed passwords and JSON Web Tokens (JWT) for authentication.
- **Weather forecast** endpoint that returns a week's forecast for a given city. Weather data is pulled from WeatherAPI.com using your API key.
- Database credentials, JWT secret and WeatherAPI key are stored in `config.json` and loaded via `config.py`.

## Prerequisites

* Python 3.11 (or newer).
* PostgreSQL installed and running. Create a database named **`db_weather_forecasting`** and note your username and password.
* A **WeatherAPI.com** API key (the included configuration uses `85fe739f0f7f4f17b0a173001251308` as a placeholder).

## Installation

1. **Clone or extract** this repository.

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure the application**:

   Update `config.json` with your PostgreSQL credentials, a secure JWT secret and your WeatherAPI key.

5. **Initialize the database** (creates the `users` table):

   ```bash
   python init_db.py
   ```

6. **Run the server**:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`. Interactive documentation can be found at `http://127.0.0.1:8000/docs`.

## API Endpoints

### POST `/auth/signup`

Register a new user.

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

**Response:**

Returns an access token if successful.

### POST `/auth/login`

Authenticate an existing user.

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

**Response:**

Returns an access token if the credentials are valid.

### GET `/weather`

Fetch a 7‑day weather forecast for a given city. Requires a valid Bearer token.

**Query parameters:**

* `city` (string) – the name of the city.
* `lat` (float) – the latitude of the city.
* `lon` (float) – the longitude of the city.

**Example request:**

```bash
curl -H "Authorization: Bearer <token>" \
     "http://127.0.0.1:8000/weather?city=Lahore&lat=31.5204&lon=74.3587"
```

**Response:**

Returns a JSON object containing geographic coordinates, start and end dates, and an array of daily forecasts.

## License

This project is provided as‑is under the MIT license. See the `LICENSE` file for details.