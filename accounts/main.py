from typing import Optional

from fastapi import FastAPI, Request, APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import secrets

token = secrets.token_urlsafe(48)

app = FastAPI()

SIGNIN_V1 = "/signin/v1"

public_router = APIRouter(prefix=SIGNIN_V1)
"""Public facing endpoints the user is exposed to. Responses are HTML."""

api_router = APIRouter(prefix=SIGNIN_V1 + "/_")

templates = Jinja2Templates(directory="templates")


@public_router.get("/identifier", response_class=HTMLResponse)
def identifier(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@api_router.get("/accountLookup", response_class=RedirectResponse)
def account_lookup():
    RedirectResponse()


@public_router.post("/challenge/pwd")
def password(request: Request, identifier: str = Form(...)):
    return templates.TemplateResponse("password.html", {"request": request, "identifier": identifier})


@public_router.get("/callback", response_class=HTMLResponse)
def callback(code: str, state: Optional[str] = None):
    """ The callback url. """
    # https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#2-users-are-redirected-back-to-your-site-by-github
    # Parses query parameters and requests an AuthToken from GitHub
    "https://api.github.com/user"


app.include_router(public_router)
app.include_router(api_router)
