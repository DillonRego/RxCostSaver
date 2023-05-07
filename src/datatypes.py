from dataclasses import dataclass

@dataclass
class Drug:
    Brand_Name: str
    Gen_Name: str
    Manufact_ID: int
    drug_id: int
    price_delta: int


@dataclass
class Manufacturer:
    manufac_name: str
    manufac_id: int

@dataclass
class Gross_Cost:
    cost: float
    year: int
    manufac_id: int
    
@dataclass
class Drug_year:
    year: int
    drug_id: int
    total_dosage_unit: int
    total_claims: int
    avg_spend_claim: int
    avg_spend_dose: int
    total_spend: int
    outlier: bool
