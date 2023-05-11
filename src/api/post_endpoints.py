from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
import sqlalchemy

router = APIRouter()

class drug_yearJson(BaseModel):
  year: int
  drug_id: int
  total_dosge_units: float
  total_claims: float
  avg_spending_per_claim: float
  avg_spending_per_dosage_weighted: float
  total_spending: float
  outlier: bool

@router.post("/add_entry/{drug_id}", tags=["entry"])
def add_entry(drug_id: int, drug_year: drug_yearJson):
  """
  This endpoint will insert a new row into the drug_year database with the 
  given information, if the year is not specified it will default to the 
  earliest recorded year not already filled. If a year is given it will 
  only fill in the drug data for the given year, (all inputs after tot_mftr) 
  """
  sql = """ 
  select min(year)
  from drug_year
  where drug_id = :x"""

  post_result = []
  json = []
  with db.engine.connect() as conn:
    result = conn.execute(sqlalchemy.text(sql), drug_id)
    if result.rowcount == 0:
      raise HTTPException(status_code=404, detail="drug not found")
  
  with db.engine.connect() as conn:
    post_result = conn.execute(db.drug.insert().values(drug_year))
    if post_result.rowcount == 0:
      raise HTTPException(status_code=404, detail="drug not found")
    for row in post_result:
      json.append({
        'rows': row.post_result
      })
  return json

@router.post("/delete_entry/{drug_id}", tags=["entry"])
def delete_entry(
  year: int = -1,
  drug_id: int = -1):
  """
  This endpoint will delete entries under the drug id. If no year is specified
  it will automatically delete all for that entry,
  if a year is given it will only delete information for that calendar year.
  """
  first_sql = """select drug_id from drug_year where drug_id = {}""", drug_id
  with db.engine.connect() as conn:
    test_result = conn.execute(sqlalchemy.text(first_sql))
    if test_result.rowcount == 0:
      raise HTTPException(status_code=404, detail="invalid drug_id")

  sql = """
  delete from drug_year
  where drug_id = :y"""

  if year == -1:
    additional_string = ""
  else:
    additional_string = " and year = {}", year 
  json = []
  with db.engine.connect() as conn:
    result = conn.execute(sqlalchemy.text(sql), additional_string)
    if result.rowcount == 0:
      raise HTTPException(status_code=404, detail="drug not found")
    for row in result:
      json.append({
        'rows': row.post_result
      })
  return json