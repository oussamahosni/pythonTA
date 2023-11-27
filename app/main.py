from fastapi import FastAPI
from .scraper import Scraper
from fastapi.responses import JSONResponse
import json 
from pymongo import MongoClient
from fastapi.testclient import TestClient

app = FastAPI()

scraper=Scraper()

mongo_client = MongoClient("mongodb://db:27017")
db = mongo_client["ScrapingDB"]
collection = db["PageLyceena"]

results=scraper.scrapedata()

@app.get("/") 
def scraping_app():
    collection.insert_one(results) 
    return {"scraping Completed":"Results are stored in MongoDB"}   

def test_scraping_app():
    client=TestClient(app)
    response= client.get('/')
    assert response.status_code==200
    assert response.json() == {"scraping Completed":"Results are stored in MongoDB"}  