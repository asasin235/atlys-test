# src/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import Settings
from src.scraper import Scraper
from fastapi import BackgroundTasks


app = FastAPI()
security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your_static_token":
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: Settings, background_tasks: BackgroundTasks):
    def scrape_and_log():
        scraper = Scraper(settings)
        scraper.scrape_products()
        print("Scraping completed successfully")

    background_tasks.add_task(scrape_and_log)
    return {"message": "Scraping started"}
