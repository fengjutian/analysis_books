from pydantic import BaseModel

class CompanyCreate(BaseModel):
    company_id: str
    name: str

class CompanyOut(BaseModel):
    company_id: str
    name: str
