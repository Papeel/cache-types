from fastapi import FastAPI, Response, Request
from asyncio import sleep
from datetime import datetime, timezone
from pydantic import UUID4
from apps.http.boot import Boot
from apps.http.cache import Cache
from src.shared.domain.date_utils import DateUtils
from src.users.application.search.service import UserSearcher
from src.users.domain.user import User
from src.users.domain.exceptions import UserDoesntExists


Boot()
app = FastAPI()


@app.get("/api/v1/browser-cache/header-cache-control")
async def header_cache_control(response: Response):
    await sleep(3)
    response.headers["Cache-Control"] = "max-age=3600, stale-while-revalidate=60"
    return {"message": "Sorry for the delay"}


@app.get("/api/v1/browser-cache/eTag")
async def header_cache_control_with_etag(response: Response, request: Request):
    etag = str(datetime.now(timezone.utc).minute)
    print(request.headers.get("If-None-Match"))

    print(etag)
    if request.headers.get("If-None-Match") == etag:
        response.status_code = 304
        return
    await sleep(3)
    return {"message": "Sorry for the delay"}


@app.get("/api/v1/reverse-proxy")
async def header_cache_control_with_reverse_proxy(response: Response, request: Request):
    await sleep(3)
    response.headers["Cache-Control"] = "max-age=3600, s-maxage=6000"
    return {"message": "Sorry for the delay"}


cache_ttl_in_seconds: int = 60
cache_in_memory: dict[str, Cache] = {}


@app.get("/api/v1/controler-cache-in-memory")
async def controler_cache_in_memory(response: Response, request: Request):
    cache_key = str(request.query_params)
    if cache_key in cache_in_memory:
        if (
            DateUtils.utc_now() - cache_in_memory[cache_key].created_at
        ).seconds < cache_ttl_in_seconds:
            return {"message": "Cached"}
    await sleep(3)
    cache_in_memory[cache_key] = Cache(data={"message": "No cache"})
    return {"message": "No cache"}


@app.get("/api/v1/users/{user_id}")
async def search_user_by_id(response: Response, request: Request, user_id: str):
    user_id = UUID4(user_id)
    service = Boot.get(UserSearcher)
    try:
        user: User = await service(user_id)
        return user.model_dump()
    except UserDoesntExists:
        response.status_code = 404
        return {"message": "Not found"}
