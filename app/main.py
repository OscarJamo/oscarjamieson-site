import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_NAME = os.getenv("APP_NAME", "oscarjamieson")

app = FastAPI(title=APP_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "contact_email": os.getenv("PUBLIC_CONTACT_EMAIL", "hello@oscarjamieson.com"),
        },
    )


@app.post("/api/contact")
def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    name = name.strip()
    email = email.strip()
    message = message.strip()

    if len(name) < 2:
        return JSONResponse({"ok": False, "error": "Name is too short."}, status_code=400)
    if "@" not in email or "." not in email:
        return JSONResponse({"ok": False, "error": "Please enter a valid email."}, status_code=400)
    if len(message) < 10:
        return JSONResponse({"ok": False, "error": "Message is too short."}, status_code=400)

    # For v1: don't store anything server-side. Just acknowledge.
    # (Later we can email you via SendGrid/Mailgun or store in a database.)
    return {"ok": True}
