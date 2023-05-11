from fastapi import FastAPI
from src.api import get_endpoints, post_endpoints, pkg_util

tags_metadata = [
    {
        "name": "claims",
        "description": "Access information on claims.",
    },
    {
        "name": "manufacturer",
        "description": "Access information on drug manufacturers.",
    },
    {
        "name": "gross_cost",
        "description": "Access information on medicaid costs.",
    },
    {
        "name": "change_avg_spend",
        "description": "Access information on conversations."
    },
    {
        "name": "entry",
        "description": "manipulate entries in the table."
    }
]

app = FastAPI(
    title="RX API",
    description="",
    version="0.0.1",
    contact={
        "name": "Dillon Rego",
        "email": "drego@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
app.include_router(get_endpoints.router)
app.include_router(post_endpoints.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Rx API. See /docs for more information."}
