from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/blog")
async def get_blog(request: Request):
    return {"message": "Hello World"}
