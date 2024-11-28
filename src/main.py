# src/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import Settings
from src.scraper import Scraper

app = FastAPI()
security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your_static_token":
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: Settings):
    scraper = Scraper(settings)
    scraper.scrape_products()
    return {"message": "Scraping completed successfully"}
