# Neo4j Project with FastAPI

This is a simple project demonstrating how to use Neo4j with FastAPI to create a REST API for managing company data.

## Project Structure

```
neo4j-project/
├── app/
│   ├── crud.py        # Database operations
│   ├── db.py          # Database connection setup
│   └── schemas.py     # Pydantic models for request/response validation
├── main.py            # FastAPI application entry point
├── pyproject.toml     # Project dependencies and configuration
└── README.md          # Project documentation
```

## Requirements

- Python 3.13+
- Neo4j database
- FastAPI
- Uvicorn

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Configure Neo4j connection**
   The database connection is configured in `app/db.py`. By default, it connects to a Neo4j instance running on localhost:7687 with username/password "fengjutian/fengjutian".
   You can override these settings using environment variables:
   - `NEO4J_URI`
   - `NEO4J_USER`
   - `NEO4J_PASS`

## Running the Application

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Neo4j Connection Testing

If you encounter issues connecting to Neo4j, you can use the provided test scripts to diagnose problems:

```bash
# Simple connection test using default credentials
python test_neo4j_connection.py

# Interactive connection test to try different credentials
python test_neo4j_interactive.py
```

## Troubleshooting Neo4j Connection Issues

If you're experiencing problems connecting to Neo4j, please refer to the detailed troubleshooting guide:

```bash
# Open the troubleshooting guide
start neo4j_troubleshooting.md  # Windows
open neo4j_troubleshooting.md   # macOS
xdg-open neo4j_troubleshooting.md  # Linux
```

The guide covers common errors like authentication failures and service unavailability, with step-by-step solutions for resolving these issues.
API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs`

## API Endpoints

### Companies

- **Create a company**
  - Method: POST
  - URL: `/companies/`
  - Request Body:
    ```json
    {
      "company_id": "string",
      "name": "string"
    }
    ```
  - Response:
    ```json
    {
      "company_id": "string",
      "name": "string"
    }
    ```

- **Get a company by ID**
  - Method: GET
  - URL: `/companies/{company_id}`
  - Response:
    ```json
    {
      "company_id": "string",
      "name": "string"
    }
    ```
  - 404 Error if company not found

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast (high-performance) web framework for building APIs
- [Neo4j](https://neo4j.com/) - Graph database for storing company relationships
- [Uvicorn](https://www.uvicorn.org/) - ASGI server implementation


## 删除节点及其关系

```
MATCH (n:Book {id: 4})
DETACH DELETE n

```