from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import boto3
import uuid
import os
from botocore.exceptions import BotoCoreError, ClientError

app = FastAPI()

BUCKET_NAME = "jsdhekale-snehal-photo-uploads-ap-south-1"
AWS_REGION = "ap-south-1"

s3 = boto3.client("s3", region_name=AWS_REGION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://snehaldigitalphoto.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Rajiv Digital Photo Studio API is running"}


@app.get("/health")
def health():
    return {"status": "healthy", "application": "rajiv-photo-platform"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        ext = os.path.splitext(file.filename)[1] if file.filename else ""
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}{ext}"

        file_bytes = await file.read()

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=file_bytes,
            ContentType=file.content_type or "application/octet-stream",
        )

        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_name},
            ExpiresIn=3600,
        )

        return {
            "message": "File uploaded successfully",
            "file_name": file_name,
            "s3_url": presigned_url,
        }

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/photos")
def list_photos():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = []

        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                presigned_url = s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": BUCKET_NAME, "Key": key},
                    ExpiresIn=3600,
                )
                files.append({
                    "file_name": key,
                    "url": presigned_url
                })

        return {"photos": files}

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list photos: {str(e)}")
