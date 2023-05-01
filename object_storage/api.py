from fastapi import FastAPI
from object_storage.routers import upload, download
from dotenv import load_dotenv

# load .env variables
load_dotenv()

# create app instance
app = FastAPI()

# add routes
app.include_router(upload.router)
app.include_router(download.router)
