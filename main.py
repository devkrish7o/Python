from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mock database - Simple list of dictionaries
sports_data = [
    {"id": 1, "name": "Football", "coach": "John Doe", "timing": "4:00 PM - 6:00 PM", "venue": "Main Ground"},
    {"id": 2, "name": "Basketball", "coach": "Jane Smith", "timing": "5:00 PM - 7:00 PM", "venue": "Indoor Court"},
    {"id": 3, "name": "Cricket", "coach": "Mike Ross", "timing": "3:30 PM - 6:30 PM", "venue": "Cricket Field"},
]

registrations = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "sports": sports_data})

@app.get("/register/{sport_id}", response_class=HTMLResponse)
async def register_page(request: Request, sport_id: int):
    sport = next((s for s in sports_data if s["id"] == sport_id), None)
    return templates.TemplateResponse("register.html", {"request": request, "sport": sport})

@app.post("/submit-registration")
async def submit_registration(request: Request, student_name: str = Form(...), student_id: str = Form(...), sport_name: str = Form(...)):
    new_reg = {"name": student_name, "sid": student_id, "sport": sport_name}
    registrations.append(new_reg)
    return templates.TemplateResponse("success.html", {"request": request, "reg": new_reg})

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "registrations": registrations})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
