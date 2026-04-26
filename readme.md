# URL-Shortener

Simple REST API for shortening URLs, accessible via local server.

## Features

### Short URL Generation
- Shorten a long URL to a unique 6-character short URL
- Collision resistance by implementing retry logic (up to 5 times)
- Prevents shortening links that already belong to application's database

### URL Redirection
- Short URL redirects user to original URL
- Implements a Read-Through Cache pattern using Redis. Frequently accessed links are served from cache instead of database.
- Cached URLs are stored for 7 days and after that data is cleaned
- Redirection for specific short URL is counted in background task for statistics

### Statistics
- View click count for specific short URL by using it in input

## CI/CD & Testing
- GitHub Actions integration for Continuous Integration (CI) - tests are automatically run on every push and pull request
- Unit tests with pytest
- Integration tests with pytest and Testcontainers

## Installation
1. Clone the repository:

```bash
git clone https://github.com/Eeernest/URL-Shortener.git
cd URL-Shortener
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Create an .env file in the project root:

```env
# POSTGRESQL

POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db

# Database URL format: postgresql://USER:PASSWORD@HOST:PORT/DB
POSTGRES_URL=your_postgres_url

# REDIS

REDIS_URL=redis://redis:6379/0

# REDIS-RATE-LIMIT

REDIS_RL_URL=redis://redis:6379/1

# WEBSITE URL

NETLOC=127.0.0.1:8000

FRONT_URL=http://localhost:8000
```

> Do not commit real credentials. Replace all values with your own before running the application.

4. Run the application using Docker Compose:

```bash
docker-compose up --build
```

5. Run tests locally:

```bash
pytest
```

## Access:
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure
- app/
  - templates/ HTML templates
  - static/ CSS and JavaScript files
  - routers/ API endpoints
  - dependencies/ dependency injections
  - services/ business logic
  - tasks/ background tasks
  - repositories/ database and cache operations
  - schemas/ Pydantic models for data validation
  - models/ SQLAlchemy database models
  - cache/ Redis cache configurations
  - db/ PostgreSQL connection and session setup
  - core/ configuration, middleware and exception handling

- tests/
  - routers/ unit and integrations tests for API endpoints
  - services/ unit tests for business logic
  - repositories/ integeration tests for DB and Cache
  - fixtures/ pytest fixtures for test components

## Tech Stack
- Python 3.12 (FastAPI)
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL, SQLAlchemy
- Cache: Redis
- Migrations: Alembic
- Tests: Pytest, Testcontainers
- Infrastructure: Docker & Docker Compose