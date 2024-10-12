# FAST imports
from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
# STARLETTE
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
# DATABASE
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
# OAuth
from oauth import oauth, discord
import secrets
import httpx
# MISC imports
from jose import JWTError, jwt
from datetime import datetime, timedelta
from templates import templates

SECRET_KEY = os.getenv("APP_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = APIRouter()

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Inactive user")

# ---------------- CORE Login

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login", response_class=HTMLResponse)
async def login_for_access_token(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...), 
    db: AsyncSession = Depends(get_db)
):
    from controllers.user import authorize_user
    user = await authorize_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse("/users/me", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    from controllers.user import create_user_from_email as create_user
    user = await create_user(
        db=db,
        email=email,
        password=password,
        username=username,
        full_name=full_name
    )
    if user:
        response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "error": "User registration failed"})

@app.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

# ---------------- Oauth

@app.get("/login/discord")
async def login(request: Request):
    # Generate a random state
    state = secrets.token_urlsafe(16)  # Generate a secure random state
    request.session['oauth_state'] = state  # Store it in the session
    redirect_uri = os.getenv("DISCORD_REDIRECT_URI")
    # Redirect to Discord with the state
    return await oauth.discord.authorize_redirect(request, redirect_uri, state=state)


@app.route("/auth")
async def auth(request: Request):
    token = await discord.authorize_redirectrize_access_token(request)
    user = await discord.parse_id_token(request, token)
    return {"user_info": user}


@app.get("/callback")
async def callback(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    from database import get_or_create_user
    try:
        token = await oauth.discord.authorize_access_token(request)
        if not token or "access_token" not in token:
            raise HTTPException(status_code=400, detail="Invalid OAuth token")
        async with httpx.AsyncClient() as client:
            headers = {'Authorization': f'Bearer {token["access_token"]}'}
            discord_user_info_response = await client.get("https://discord.com/api/users/@me", headers=headers)
        if discord_user_info_response.status_code == 200:
            user_data = discord_user_info_response.json()
            discord_id = user_data["id"]
            username = user_data["username"]
            email = user_data.get("email", None)
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{user_data['avatar']}.png"
            user = await get_or_create_user(db, discord_id, username, email, avatar_url, token)
            print(f"User info: {user_data}")
            ACCESS_TOKEN_EXPIRE_MINUTES = 1440
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            print(access_token_expires)
            print(token["access_token"])
            access_token = create_access_token(
                data={"sub": token["access_token"]}, expires_delta=access_token_expires
            )
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            return {"user_info": user_data}
        else:
            raise HTTPException(status_code=discord_user_info_response.status_code, detail="Failed to fetch user info")

    except Exception as e:
        print(f"Error during callback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ---------------- MISC

@app.get("/users/me", response_class=HTMLResponse)
async def read_users_me(request: Request, token: str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

async def send_message_to_discord_channel(token, channel_id, message):
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://discord.com/api/channels/{channel_id}/messages",
            headers=headers,
            json={"content": message}
        )
    return response.json()


@app.get("/protected")
async def protected_route(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in user_sessions:
        user_id = user_sessions[session_id]
        return {"message": f"Welcome back, user {user_id}!"}    
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})
