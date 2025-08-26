from neo4j import Session
from app.schemas import CompanyCreate, CompanyOut

def create_company(session: Session, company: CompanyCreate) -> CompanyOut:
    query = """
    MERGE (c:Company {company_id:$company_id})
    ON CREATE SET c.name=$name
    ON MATCH  SET c.name=$name
    RETURN c.company_id AS company_id, c.name AS name
    """
    result = session.run(query, company_id=company.company_id, name=company.name)
    record = result.single()
    return CompanyOut(**record.data())

def get_company(session: Session, company_id: str) -> CompanyOut | None:
    query = """
    MATCH (c:Company {company_id:$company_id})
    RETURN c.company_id AS company_id, c.name AS name
    """
    record = session.run(query, company_id=company_id).single()
    return CompanyOut(**record.data()) if record else None
