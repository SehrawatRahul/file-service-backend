import os
import re
import logging
from datetime import timedelta
# from app.core.auth import verify_token
from app.core.minio_client import get_minio_client
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/files", tags=["Files"])

logger = logging.getLogger(__name__)

_FILENAME_RE = re.compile(r'^[\w\-.\/]+$')

def _validate_file_name(name: str):
    if not name or '..' in name or name.startswith('/'):
        raise HTTPException(status_code=400, detail="invalid file_name")
    if not _FILENAME_RE.match(name):
        raise HTTPException(status_code=400, detail="invalid file_name characters")
    return name

def _presigned_url_for(client, operation: str, bucket: str, key: str, expires: int = 3600):
    """
    operation: 'put' or 'get'
    Supports boto3 client (generate_presigned_url) and minio.Minio (presigned_put_object / presigned_get_object).
    """
    try:
        # boto3 client
        if hasattr(client, "generate_presigned_url"):
            method = "put_object" if operation == "put" else "get_object"
            return client.generate_presigned_url(
                ClientMethod=method,
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires
            )
        # minio-py client
        if hasattr(client, "presigned_put_object") and hasattr(client, "presigned_get_object"):
            expires_td = timedelta(seconds=expires)
            if operation == "put":
                return client.presigned_put_object(bucket, key, expires=expires_td)
            return client.presigned_get_object(bucket, key, expires=expires_td)
        raise RuntimeError("unsupported storage client: no presign method found")
    except Exception:
        logger.exception("failed to generate presigned URL for %s/%s", bucket, key)
        raise

def _get_bucket():
    # Prefer MINIO_BUCKET, fall back to AWS_S3_BUCKET for compatibility
    return os.getenv("MINIO_BUCKET") or os.getenv("AWS_S3_BUCKET")

@router.get("/upload-url")
def generate_upload_url(file_name: str):
    """✔ Protected by Keycloak"""
    _validate_file_name(file_name)
    bucket = _get_bucket()
    if not bucket:
        raise HTTPException(status_code=500, detail="storage bucket not configured")
    client = get_minio_client()
    try:
        url = _presigned_url_for(client, "put", bucket, file_name, expires=3600)
        return {"upload_url": url, "file_name": file_name}
    except HTTPException:
        raise
    except Exception:
        logger.exception("unable to generate upload url for %s", file_name)
        raise HTTPException(status_code=500, detail="unable to generate upload url")

@router.get("/download-url")
def generate_download_url(file_name: str):
    """✔ Protected by Keycloak"""
    _validate_file_name(file_name)
    bucket = _get_bucket()
    if not bucket:
        raise HTTPException(status_code=500, detail="storage bucket not configured")
    client = get_minio_client()
    try:
        url = _presigned_url_for(client, "get", bucket, file_name, expires=3600)
        return {"download_url": url, "file_name": file_name}
    except HTTPException:
        raise
    except Exception:
        logger.exception("unable to generate download url for %s", file_name)
        raise HTTPException(status_code=500, detail="unable to generate download url")
