from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
import sqlalchemy

router = APIRouter()

class drug_yearJson(BaseModel):
  year: int
  total_dosage_units: float
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
  post_result = []
  json = []
 
  insertStmnt = """
  insert into drug_year (year, drug_id, total_dosage_units, total_claims, 
  avg_spending_per_claim, avg_spending_per_dosage_weighted, outlier)
  values ( :year, :drug_id, :total_dosage_units, :total_claims,
  :avg_spending_per_claim, :avg_spending_per_dosage_weighted, :outlier)
  on conflict (year, drug_id)
  do update set
    total_dosage_units = :total_dosage_units,
    total_claims = :total_claims,
    avg_spending_per_claim = :avg_spending_per_claim,
    avg_spending_per_dosage_weighted = :avg_spending_per_dosage_weighted,
    outlier = :outlier;
  """
  with db.engine.connect() as conn:
    try:
      result = conn.execute(sqlalchemy.text(insertStmnt), 
      [{"year" : drug_year.year, "drug_id" : drug_id, 
      "total_dosage_units" : drug_year.total_dosage_units, 
      "total_claims" : drug_year.total_claims,
      "avg_spending_per_claim" : drug_year.avg_spending_per_claim, 
      "avg_spending_per_dosage_weighted" : drug_year.avg_spending_per_dosage_weighted,
      "total_spending" : drug_year.total_spending, 
      "outlier" : drug_year.outlier}])
      if result == None:
        print("Insert successful")
      else:
        print("Insert failed")
    except Exception as e:
      conn.rollback()
      print("An Error has occurred", str(e))

@router.post("/delete_entry/{drug_id}", tags=["entry"])
def delete_entry(
  year: int = -1,
  drug_id: int = -1):
  """
  This endpoint will delete entries under the drug id. If no year is specified
  it will automatically delete all for that entry,
  if a year is given it will only delete information for that calendar year.
  """
  
  if year == -1:
    sql = """
    delete from drug_year
    where drug_id = :d"""
  else:
    sql = """
    delete from drug_year
    where drug_id = :d and year = :y"""

  json = []
  with db.engine.connect() as conn:
    try:
      result = conn.execute(sqlalchemy.text(sql), [{"d":drug_id, "y": year}])
      if result.status_code == 200:
        print("Delete successful")
      else:
        print("Delete failed")
    except Exception as e:
      conn.rollback()
      print("An Error has occurred", str(e))

