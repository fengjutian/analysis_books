from fastapi import FastAPI, Depends, HTTPException
from app.db import get_session, CloseNeo4jSessionMiddleware
from app import crud, schemas

app = FastAPI(title="Neo4j FastAPI Example")

# Add middleware to close Neo4j sessions
app.add_middleware(CloseNeo4jSessionMiddleware)

@app.get("/")
async def root():
    return {
        "message": "Neo4j FastAPI Example",
        "version": "0.1.0",
        "docs_url": "/docs",
        "description": "API for managing company data in Neo4j graph database"
    }

@app.post("/companies/", response_model=schemas.CompanyOut)
async def create_company(company: schemas.CompanyCreate, session=Depends(get_session)):
    # 检查公司是否已存在
    existing_company = crud.get_company(session, company.company_id)
    if existing_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(session, company)

@app.get("/companies/{company_id}", response_model=schemas.CompanyOut)
async def get_company(company_id: str, session=Depends(get_session)):
    result = crud.get_company(session, company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return result
