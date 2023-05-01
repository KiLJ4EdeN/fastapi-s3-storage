import os 
import boto3
import shutil
import tempfile
from loguru import logger
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={200: {"description": "Success"},
               500: {"description": "Internal Server Error"},
               422: {"description": "Unprocessable Entity"}},
)

@router.get("/")
def upload_get():
    return {"Message": "object-storage is up!"}

@router.post("/")
def upload_post(name: str, file: UploadFile = File()):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=422, detail="Item not found")
    
    logger.debug('Incoming Request Being Processed...')

    # save the incoming zip
    try:
        directory_path = tempfile.mkdtemp()
        file_location = f"{directory_path}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
            logger.debug(f'Zip File Saved to: {file_location}')
    except Exception as e:
        logger.error(f'error when writing zip file: {e}')
        raise HTTPException(status_code=422, detail="Bad Zip")

    logger.debug('Uploading to S3')
    # uploads dicom zip to object storage
    try:
        s3_resource = boto3.resource(
            "s3",
            endpoint_url=os.getenv('S3_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
        )
        bucket = s3_resource.Bucket(os.getenv('S3_BUCKET'))

        with open(file_location, "rb") as file:
            bucket.put_object(
                ACL="private", Body=file, Key=name
            )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=422, detail="Bad Zip")
    logger.info("S3 attachment upload task done.")

    # delete zip after usage
    try:
        shutil.rmtree(directory_path)
        logger.debug(f'Removing Original Zip File at: {file_location}')
    except Exception as e:
        logger.error(f'Zip Files at {file_location} Could not be Deleted!')

    # if all went well
    return {"Message": "Upload Success"}
