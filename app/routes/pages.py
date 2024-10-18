
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
# from routes.auth import oauth2_scheme

app = APIRouter()

@app.get("/test", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("test.html", {"request": request, "error": error})


@app.get(
    "/users/me", 
    response_class=HTMLResponse
)
async def read_users_me(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    # print(oauth2_scheme)
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    from controllers.user import get_current_user
    user = await get_current_user(db, token)
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("auth/user.html", {"request": request, "user": user})

