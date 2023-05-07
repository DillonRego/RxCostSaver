from fastapi import APIRouter, HTTPException
from src import database as db
from src.datatypes import Drug, Manufacturer, Gross_Cost, Drug_year

from fastapi.params import Query
from pydantic import BaseModel
import sqlalchemy

router = APIRouter()

#maybe do SQL?

@router.post("/add_entry", tags=["add_entry"])
def add_entry():
    """
  This endpoint will insert a new row into the database with the given information, if the year is not specified it will default to the earliest year not already         filled. If a year is given it will only fill in the drug data for the given year, (all inputs after tot_mftr) 
    """

    
@router.post("/delete_entry", tags=["delete_entry"])
def delete_entry():
    """
  This endpoint will delete entries under the given brand name and generic drug name. If no year is specified it will automatically delete all for that entry, if a       year is given it will only delete information for that calendar year.
    """
       