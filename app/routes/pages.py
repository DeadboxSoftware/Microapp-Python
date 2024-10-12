
from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
import httpx
from jose import JWTError, jwt
from templates import templates

app = APIRouter()

@app.get("/test", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("test.html", {"request": request, "error": error})