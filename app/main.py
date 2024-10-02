from fastapi import FastAPI, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from routes.auth import app as router

SECRET_KEY = os.getenv("APP_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Load Env
# load_dotenv()
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# Template rendering
# templates = Jinja2Templates(directory="templates")
app.include_router(router)
