from fastapi import APIRouter, Depends, HTTPException

from functions.security import get_access_token
from cache.redis_init import redis_client
from functions.student import StudentFunction
from schema.request import PutInBucketRequest, PutOutBucketRequest

router = APIRouter(prefix="/bucket")

@router.get("/{id}", status_code=200, tags=["Bucket"])
def get_bucket_by_id_handler(
    id: str,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends()
):
    payload = student_func.decode_jwt(access_token)
    id_logged_in = payload['sub']
    role = payload['role']

    if not id_logged_in == id:
        raise HTTPException(status_code=401, detail="Not Allowed.")
    
    if role == 'instructor':
        raise HTTPException(status_code=401, detail="Not Allowed.")


    return redis_client.smembers(f"user:student:{id}:bucket")


@router.post("/", status_code=201, tags=["Bucket"])
def post_bucket_by_id_handler(
    request: PutInBucketRequest,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends()
):
    payload = student_func.decode_jwt(access_token)
    id_logged_in = payload['sub']
    role = payload['role']

    if not id_logged_in == request.id:
        raise HTTPException(status_code=401, detail="Not Allowed.")
    
    if role == 'instructor':
        raise HTTPException(status_code=401, detail="Not Allowed.")
    
    redis_client.sadd(f"user:student:{request.id}:bucket", request.course_id)
    redis_client.expire(f"user:student:{request.id}:bucket", 60*60)


@router.delete("/{id}/{course_id}", status_code=204, tags=["Bucket"])
def delete_bucket_by_id_handler(
    id: str,
    course_id: int,
    access_token: str = Depends(get_access_token),
    student_func: StudentFunction = Depends()
):
    payload = student_func.decode_jwt(access_token)
    role = payload['role']

    if role == 'instructor':
        raise HTTPException(status_code=401, detail="Not Allowed.")
    
    exists = redis_client.sismember(f"user:student:{id}:bucket", course_id)

    if not exists:
        raise HTTPException(status_code=404, detail="Not Found.")
    
    redis_client.srem(f"user:student:{id}:bucket", course_id)