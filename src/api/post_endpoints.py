from fastapi import APIRouter, HTTPException
from src import database as db

from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy

router = APIRouter()

@router.post("/add_entry", tags=["add_entry"])
def add_entry(
  year: int = 2017,
  drug_id: int = 1,
  total_dosge_units: float = 0,
  total_claims: float = 0,
  avg_spending_per_claim: float = 0,
  avg_spending_per_dosage_weighted: float = 0,
  total_spending: float = 0,
  outlier: bool = True):

  """
  This endpoint will insert a new row into the drug_year database with the given information, if the year is not specified it will default to the earliest year not already 
  filled. If a year is given it will only fill in the drug data for the given year, (all inputs after tot_mftr) 
  """
  sql = """ 
  select min(year)
  from drug_year
  where drug_id = :x"""

  post_result = {}
  with db.engine.connect() as conn:
    result = conn.execute(sqlalchemy.text(sql), drug_id)
  year = max(year, result.year)
  post_values = {'year' : year, 'drug_id': drug_id, 
  'total_dosge_units': total_dosge_units, 'total_claims': total_claims, 
  'avg_spending_per_claim' : avg_spending_per_claim, 
  'avg_spending_per_dosage_weighted' : avg_spending_per_dosage_weighted,
  'total_spending' : total_spending,
  'outlier' : outlier}
  with db.engine.connect() as conn:
    post_result = conn.execute(db.drug.insert().values(post_values))
    
@router.post("/delete_entry", tags=["delete_entry"])
def delete_entry(
  year: int = -1,
  drug_id: int = -1):
  """
  This endpoint will delete entries under the drug id. If no year is specified it will automatically delete all for that entry,
  if a year is given it will only delete information for that calendar year.
  """
  first_sql = """select drug_id from drug_year where drug_id = {}""", drug_id
  with db.engine.connect() as conn:
    test_result = conn.execute(sqlalchemy.text(first_sql))

  sql = """
  delete from drug_year
  where drug_id = :y"""

  if year == -1:
    additional_string = ""
  else:
    additional_string = " and year = {}", year 

  with db.engine.connect() as conn:
    test_result = conn.execute(sqlalchemy.text(sql), additional_string)