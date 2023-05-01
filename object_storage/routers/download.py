import os
import boto3
import tempfile
from loguru import logger
from fastapi import APIRouter, HTTPException, Response

router = APIRouter(
    prefix="/download",
    tags=["download"],
    responses={200: {"description": "Success"},
               500: {"description": "Internal Server Error"},
               404: {"description": "Not Found"},
               },
)

@router.get("/")
def download_get():
    return {"Message": "object-storage is up!"}

@router.post("/")
def download_post(name: str):
    try:
        # get bucket
        s3_resource = boto3.resource(
            "s3",
            endpoint_url=os.getenv('S3_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
        )
        bucket = s3_resource.Bucket(os.getenv('S3_BUCKET'))
    except Exception as e:
        logger.error(f'Cannot Connect to S3 Instance: {e}')
        raise HTTPException(status_code=503, detail="S3 Unavailable")
    try:
        with tempfile.TemporaryDirectory() as directory_path:
            file_location = f"{directory_path}/{name}"
            bucket.download_file(
                    name,
                    file_location)
            with open(file_location, "rb") as zip_bytes:
                response = Response(content=zip_bytes.read(), media_type="application/x-zip-compressed")
                # response = StreamingResponse(iter([io.getvalue()]), media_type="application/x-zip-compressed")
                response.headers["Content-Disposition"] = f"attachment; filename={name}"
                logger.debug('Download Success, Returning Zip')
                return response
    except Exception as e:
        logger.error(f'Zip file download failed: {e}')
        raise HTTPException(status_code=404, detail="File Not Found")
