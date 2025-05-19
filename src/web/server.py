from src.utilities import configuration
from src.core import manager

from starlette.middleware.sessions import SessionMiddleware
from starlette.websockets import WebSocketDisconnect

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from typing import Optional
import os
import threading


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
templates = Jinja2Templates(directory="src/web/templates")

app.add_middleware(
    SessionMiddleware,
    secret_key='super_secret',
    session_cookie='session_cookie',
    max_age=3600
)

current_port = configuration.get_web_server_port()
security = HTTPBasic()

async def get_current_username(request: Request):
    username = request.session.get('username')
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    form_username = form_data.get('username')
    form_password = form_data.get('password')

    # TODO: implement db authentication
    if form_username == form_password == 'root':
        request.session['username'] = form_username
        return RedirectResponse(url="/", status_code=303)
    
    return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('username', None)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})

def run():
    web_server_thread = WebServerThread()
    web_server_thread.daemon = True
    web_server_thread.start()
    
    return web_server_thread

class WebServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = None
        
    def run(self):
        try:
            import uvicorn
            manager.web_server_status = 'on'
            self.server = uvicorn.run(
                app, 
                host="0.0.0.0", 
                port=int(current_port), 
                log_level="warning"
            )
            manager.web_server_status = 'off'
        except Exception as e:
            manager.web_server_thread = f'error: {e}'
        
    # TODO: proper shutdown mechanism
    def stop(self):
        if not self.server:
            return False
         
        self.server = None
        manager.web_server_thread = None
        return True
