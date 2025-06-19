from fastapi import APIRouter, Depends, Request
from datetime import timedelta

from src.schemas import User
from src.services.auth import get_current_user
from limiter import limiter

router = APIRouter(prefix="/users", tags=["users"])

rate_limit_store = {}

MAX_REQUESTS = 2
TIME_WINDOW = timedelta(minutes=1)


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):

    return user
