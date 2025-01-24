from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Przykładowe dane
data = [
    {"year": 2013, "industry": "Electronics", "sales_amount": 100000},
    {"year": 2014, "industry": "Electronics", "sales_amount": 120000},
    {"year": 2015, "industry": "Electronics", "sales_amount": 150000},
    {"year": 2013, "industry": "Home & Garden", "sales_amount": 80000},
    {"year": 2014, "industry": "Home & Garden", "sales_amount": 90000},
    {"year": 2015, "industry": "Home & Garden", "sales_amount": 110000},
]

@app.get("/sales")
def get_sales():
    return data


 