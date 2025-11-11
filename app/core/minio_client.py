import boto3
import os

def _env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")

def get_minio_client():
    """
    Returns a boto3 s3 client configured to talk to MinIO (or real S3).
    Reads MINIO_ENDPOINT, MINIO_SECURE, MINIO_ACCESS_KEY, MINIO_SECRET_KEY.
    If MINIO_ENDPOINT is not set, boto3 will use default AWS endpoints.
    """
    endpoint = os.getenv("MINIO_ENDPOINT")
    secure = _env_bool("MINIO_SECURE", False)

    endpoint_url = None
    if endpoint:
        scheme = "https" if secure else "http"
        endpoint_url = f"{scheme}://{endpoint}"

    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
        region_name=os.getenv("MINIO_REGION", "us-east-1"),
    )
