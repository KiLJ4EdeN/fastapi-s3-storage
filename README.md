# Object Storage Service

# Docker Installation
```bash
DOCKER_BUILDKIT=1 docker build . -t object-storage-service
docker run -d --restart=always -p 8000:8000 object-storage-service
```

# Development Installation
```bash
python3 -m venv env
pip install -r requirements.txt
uvicorn api:app
```

# Usage

### Uploading to S3
assume a sample.zip we wanna upload under the name myFile
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/upload/?name=myFile' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample.zip;type=application/x-zip-compressed'
```

### Downloading from S3
download the same file by name
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/download/?name=myFile' \
  -H 'accept: application/json' \
  -d ''
```

# S3 info
remember to update s3 information in the .env file:
```
S3_ACCESS_KEY_ID=''
S3_SECRET_ACCESS_KEY=''
S3_BUCKET=''
S3_ENDPOINT_URL=''
SHARED_VOLUME_PATH='/tmp'
```
