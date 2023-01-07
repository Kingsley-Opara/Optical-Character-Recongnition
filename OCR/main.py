import uuid
import io
import pathlib
from fastapi import (
    FastAPI, 
    Depends,
    HTTPException, 
    Request,
    UploadFile,
    File,
    ) 
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
from pydantic import BaseSettings, BaseModel
from functools import lru_cache
from fastapi.requests import Request
from PIL import Image
import pytesseract
import secrets
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False

    class Config:
        env_file = '../.env'

@lru_cache        
def get_settings():
    return Settings()


DEBUG = get_settings().debug


BASE_DIR = pathlib.Path(__name__).parent

UPLOAD_DIR = BASE_DIR/'uploads'


templates = Jinja2Templates(directory=str(BASE_DIR/'templates'))

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root(request:Request, settings:Settings = Depends(get_settings)):
    img = f'{BASE_DIR}\images'
    print(img)
    return templates.TemplateResponse('home.html', {'request':request, 'abc':123})

@app.post('/upload', response_class=FileResponse)
async def upload(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    print(settings.echo_active)
    if not settings.echo_active:
        raise HTTPException (detail="This is not a valid endpoint", status_code=400)
    bytes_str = (io.BytesIO(await file.read()))
    fname = pathlib.Path(file.filename)
    # fsuffix = fname.suffix
    dest = UPLOAD_DIR/f'{secrets.token_urlsafe(4)}.{fname.suffix}'
    with open(str(dest), 'wb') as outh:
       outh.write(bytes_str.read())
    img = Image.open(dest)
    img_text = pytesseract.image_to_string(img)
    return {'text': img_text}