from fastapi import APIRouter, HTTPException
from src import database as db
from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy

router = APIRouter()

#maybe do SQL?

@router.get("/claims/", tags=["claims"])
def get_claims():
    """
    This endpoint will return a list of drugs for each drug it returns the following aggregated for all manufacturers:
    total_spending : a list of total yearly spending on that drug
    Avg_spending : a list of tuples containing average spending by claims and by units
    total_dsg : a list of yearly dosage units
    outlier_years : a list of years in which the drug was considered an outlier
    """
    
    
@router.get("/manufacturers/", tags=["manufacturers"])
def get_():
    """
    This endpoint returns a list of manufacturers that manufacture a given drug. For each manufacturer it returns:
    name : the name of the manufacturer
    year : the year production began for that drug by a given manufacturer
    generic_name : the generic_name of the drug
    brand_name : the manufacturers given name for the drug
    
    You can filter for only manufacturers that make a given generic_name, brand_name or both
    """

@router.get("/gross_cost", tags = ["gross_cost"])
def get_gross_cost():
    """
    This endpoint returns the total reimbursement medicaid paid to a given manufacturer for a given year 
    """
    
@router.get("change_avg_spend", tags = ["change_avg_spend"])
def change_avg_spend():
    """
    This endpoint returns a tupled list showing the change in
    average spending over the year for a given drug produced by all the manufacturers  
    """