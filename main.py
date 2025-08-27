from fastapi import FastAPI, Depends, HTTPException
from app.db import get_session, CloseNeo4jSessionMiddleware
from app import crud, schemas
from routers import all_routers

app = FastAPI(title="Neo4j FastAPI Example")

# Add middleware to close Neo4j sessions
app.add_middleware(CloseNeo4jSessionMiddleware)

for r in all_routers:
    app.include_router(r)


@app.get("/")
async def root():
    return {
        "message": "Neo4j FastAPI Example",
        "version": "0.1.0",
        "docs_url": "/docs",
        "description": "API for managing company data in Neo4j graph database"
    }

# # 创建公司
# @app.post("/companies/", response_model=schemas.CompanyOut)
# async def create_company(company: schemas.CompanyCreate, session=Depends(get_session)):
#     existing_company = crud.get_company(session, company.company_id)
#     if existing_company:
#         raise HTTPException(status_code=400, detail="Company already exists")
#     return crud.create_company(session, company)

# # 获取公司
# @app.get("/companies/{company_id}", response_model=schemas.CompanyOut)
# async def get_company(company_id: str, session=Depends(get_session)):
#     result = crud.get_company(session, company_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return result

# # 更新公司
# @app.put("/companies/{company_id}", response_model=schemas.CompanyOut)
# async def update_company(company_id: str, company: schemas.CompanyCreate, session=Depends(get_session)):
#     result = crud.update_company(session, company_id, company)
#     if not result:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return result

# # 删除公司
# @app.delete("/companies/{company_id}")
# async def delete_company(company_id: str, session=Depends(get_session)):
#     result = crud.delete_company(session, company_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return {"message": "Company deleted"}