from fastapi import APIRouter, Depends, Request, HTTPException, status

from src.schemas import User
from src.services.auth import get_current_user
from datetime import timedelta, datetime, timezone

router = APIRouter(prefix="/users", tags=["users"])

rate_limit_store = {}

MAX_REQUESTS = 2
TIME_WINDOW = timedelta(minutes=1)


@router.get("/me", response_model=User)
async def me(request: Request, user: User = Depends(get_current_user)):
    ip = request.client.host
    now = datetime.now(timezone.utc)

    if ip not in rate_limit_store:
        rate_limit_store[ip] = []

    rate_limit_store[ip] = [
        t for t in rate_limit_store[ip] if now - t < TIME_WINDOW]

    if len(rate_limit_store[ip]) >= MAX_REQUESTS:
        raise HTTPException(status_code=status.HTTP_429_MAX_REQUESTS,
                            detail="Too many requests")

    rate_limit_store[ip].append(now)
    return user
