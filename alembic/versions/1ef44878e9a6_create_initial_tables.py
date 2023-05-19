"""create initial tables

Revision ID: 1ef44878e9a6
Revises: 
Create Date: 2023-05-17 20:26:00.487713

"""
from alembic import op
import sqlalchemy as sa
from src import database as db


# revision identifiers, used by Alembic.
revision = '1ef44878e9a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
  query = """create table drug (
  drug_id bigint generated by default as identity primary key,
  brand_name text,
  generic_name text,
  manufacturer_id bigint,
  price_delta bigint
  );
  
  insert into drug(brand_name, generic_name, manufacturer_id)
  select "Brnd_Name" as brand_name, "Gnrc_Name" as generic_name, manufacturer_id
  from "Medicaid database"
  join manufacturer on manufacturer_name = "Mftr_Name"
  order by manufacturer_id, brand_name, generic_name;
  create table manufacturer(
    manufacturer_id bigint generated by default as identity primary key,
    manufacturer_name text
  );

  insert into manufacturer(manufacturer_name)
  select distinct "Mftr_Name" as manufacturer_name
  from "Medicaid database"
  order by "Mftr_Name";
  public.Medicaid database (
    Brnd_Name text not null,
    Gnrc_Name text not null,
    Tot_Mftr double precision null,
    Mftr_Name text not null,    Chg_Avg_Spnd_Per_Dsg_Unt_20_21 double precision null,
    CAGR_Avg_Spnd_Per_Dsg_Unt_17_21 text null,
    constraint Medicaid database_pkey primary key ("Brnd_Name", "Gnrc_Name", "Mftr_Name")
  ) tablespace pg_default;
"""
with db.engine.connect() as conn:
  result = conn.execute(sa.text(query))

    


def downgrade() -> None:
    pass