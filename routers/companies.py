from fastapi import APIRouter, HTTPException, Depends
from app.db import get_session
from app import crud, schemas

router = APIRouter(
    prefix="/companies",       # 路由前缀
    tags=["companies"],        # 文档分类标签
)

# 创建公司
@router.post("/", response_model=schemas.CompanyOut)
async def create_company(company: schemas.CompanyCreate, session=Depends(get_session)):
    existing_company = crud.get_company(session, company.company_id)
    if existing_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(session, company)

# 获取公司
@router.get("/{company_id}", response_model=schemas.CompanyOut)
async def get_company(company_id: str, session=Depends(get_session)):
    result = crud.get_company(session, company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return result

# 更新公司
@router.put("/{company_id}", response_model=schemas.CompanyOut)
async def update_company(company_id: str, company: schemas.CompanyCreate, session=Depends(get_session)):
    result = crud.update_company(session, company_id, company)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return result

# 删除公司
@router.delete("/{company_id}")
async def delete_company(company_id: str, session=Depends(get_session)):
    result = crud.delete_company(session, company_id)
    if not result:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted"}