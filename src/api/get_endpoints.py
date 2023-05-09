from fastapi import APIRouter, HTTPException
from src import database as db
import sqlalchemy

router = APIRouter()

@router.get("/claims/", tags=["claims"])
def get_claims(year):
    """
    This endpoint will return a list of drugs for each drug it returns
    the following aggregated for all manufacturers:
    manufacturer: manufacturer that produced the drug
    brand name: brand name of the given drug
    total_spending : a list of total yearly spending on that drug
    Avg_spending : a list of tuples containing average spending by claims 
    and by units
    total_dsg : a list of yearly dosage units
    outlier_years : a list of years in which the drug was considered an outlier
    """

    claim = sqlalchemy.select(
        db.manufacturer.c.manufacturer_name,
        db.drug.c.brand_name,
        db.drug_year.c.total_spending,
        db.drug_year.c.avg_spending_per_claim,
        db.drug_year.c.total_dosage_unit,
        db.drg_year.c.outlier
        ).where(db.drug_year.c.year == year)         
    
    with db.engine.connect() as conn:
        result = conn.execute(claim)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="drug not found")
        json = []
        for i in result:
            json.append({
                "manufacturer:": i.manufacturer_name,
                "brand_name:": i.brand_name,
                "total_spending:": i.total_spending,
                "avg_spending_per_claim:": i.avg_spending_per_claim,
                "total_dosage_unit:": i.total_dosage_unit,
                "outlier:": i.outlier
            })
    return json
    
@router.get("/manufacturers/{dId}", tags=["manufacturers"])
def get_manufacturers(id: int):
    """
    This endpoint returns a list of manufacturers that manufacture a given 
    drug. For each manufacturer it returns:
    name : the name of the manufacturer
    year : the year production began for that drug by a given manufacturer
    generic_name : the generic_name of the drug
    brand_name : the manufacturers given name for the drug

    You can filter for only manufacturers that make a given generic_name,
    brand_name or both
    """
    sql = sqlalchemy.text("""
            select manufacturer_name, min(year) as production_year, 
            generic_name, brand_name
            from manufacturer 
            join drug on manufacturer.manufacturer_id = drug.manufacturer_id
            join drug_year on drug.drug_id = drug_year.drug_id
            where drug.drug_id = id
            group by manufacturer_name, generic_name, brand_name
            order by production_year asc
        """)
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))


@router.get("/gross_cost/{id}", tags = ["gross_cost"])
def get_manufacturer_gross_cost(id: int):
    """
    This endpoint returns the total reimbursement medicaid paid to a 
    given manufacturer for a given year 
    """
    sql = sqlalchemy.text("""
            select manufacturer.manufacturer_name, 
            sum(total_spending) as medicaid_paid, year
            from manufacturer 
            join drug on manufacturer.manufacturer_id = drug.manufacturer_id
            join drug_year on drug.drug_id = drug_year.drug_id
            where manufacturer.manufacturer_id = id
            group by year, manufacturer.manufacturer_name
            order by year asc
        """)
    with db.engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(sql))
    
@router.get("change_avg_spend", tags = ["change_avg_spend"])
def change_avg_spend(brand_nam):
    """
    This endpoint returns a tupled list showing the change in
    rate of average spending over the year for a given drug 
    produced by a manufacturer
    
    WIP- may need to split drug_year into seperate tables?
    """
    change = sqlalchemy.select(
        db.manufacturer.c.manufacturer_name, 
        db.drug_year.c.year,
        db.drug_year.c.avg_spending_per_claim,
        db.drug_year.c.avg_spending_per_dosage_weighted,
        ).where(db.drug.c.brand_name == brand_nam)     
    
    with db.engine.connect() as conn:
        result = conn.execute(change)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="drug not found")
        json = []
        for i in result:
            json.append({
                "manufacturer:": i.manufacturer_name,
                "brand_name:": i.year,
                "avg_spending_per_claim:": i.avg_spending_per_claim,
                "avg_spending_per_dosage_weighted": 
                i.avg_spending_per_dosage_weighted,
            })
    return json
