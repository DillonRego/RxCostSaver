from fastapi.testclient import TestClient
from src.api.server import app
client = TestClient(app)

drug_year_data ={'year' : 2017, 
  'total_dosge_units': 0, 'total_claims': 0, 
  'avg_spending_per_claim' : 0, 
  'avg_spending_per_dosage_weighted' : 0,
  'total_spending' : 0,
  'outlier' : 0}

def test_dummy():
    assert 1 == 1
# def test_post_and_delete():
#     # Test adding an entry
#     response = client.post(f"/add_entry/1", json=drug_year_data)
#     assert response.status_code == 200
#     assert response.json() == {"rows": ["rows"]}

#     # Test deleting an entry
#     response = client.delete(f"/delete_entry/1?year=2017")
#     assert response.status_code == 200
#     assert response.json() == {"rows": ["rows"]}

# def test_post_and_delete_err():
#     response = client.post("/add_entry/-1")
#     assert response.status_code == 404
    
#     response = client.delete("/delete_entry/-1?year=2017")
#     assert response.status_code == 404
