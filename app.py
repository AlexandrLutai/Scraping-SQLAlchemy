from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import Database, Job
from scraper.hh_scraper import HH_Scraper

app = FastAPI()
db = Database()  # Инициализация базы данных
scraper = HH_Scraper()  # Инициализация парсера
templates = Jinja2Templates(directory="templates")  # Папка для шаблонов

@app.get("/", response_class=HTMLResponse)
def read_jobs(request: Request):
    """
    Отображает все записи из базы данных в виде таблицы.
    """
    session = db.Session()
    try:
        jobs = session.query(Job).all()
        return templates.TemplateResponse("index.html", {"request": request, "jobs": jobs})
    finally:
        session.close()

@app.post("/scrape", response_class=HTMLResponse)
def scrape_city(request: Request, city: str = Form(...)):
    """
    Запускает парсер для указанного города и сохраняет данные в базу.
    """
    html = scraper.fetch_jobs(city=city, page=0)
    if not html:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Не удалось получить данные для города {city}."},
        )
    
    jobs = scraper.parse_jobs(html)
    print(f"Найдено {len(jobs)} вакансий для города {city}.")
    db.save_jobs(jobs)
    return RedirectResponse("/", status_code=303)