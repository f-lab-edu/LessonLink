from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status

app = FastAPI()
zone_info = ZoneInfo("Asia/Seoul")
post_id = 0
app.posts = {}


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> str:
    return "I'm alive!"


class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime = datetime.now(tz=zone_info)


class CreatePostRequest(BaseModel):
    title: str
    content: str


class CreatePostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime


@app.post(
    "/posts", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED
)
def create_post(request: CreatePostRequest) -> CreatePostResponse:
    global post_id
    post = Post(
        id=post_id,
        title=request.title,
        content=request.content,
    )
    app.posts[post_id] = post
    post_id += 1
    return CreatePostResponse(
        id=post.id, title=post.title, content=post.content, created_at=post.created_at
    )


class GetPostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime


@app.get(
    "/posts/{post_id}", response_model=GetPostResponse, status_code=status.HTTP_200_OK
)
def get_post(post_id: int) -> GetPostResponse:
    post = app.posts.get(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GetPostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
    )


@app.get("/posts", response_model=List[GetPostResponse], status_code=status.HTTP_200_OK)
def get_posts() -> List[GetPostResponse]:
    return sorted(
        [
            GetPostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
            )
            for post in app.posts.values()
        ],
        key=lambda post: -post.id,
    )


if __name__ == "__main__":
    uvicorn.run(app)
