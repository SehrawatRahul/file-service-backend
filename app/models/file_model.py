from pydantic import BaseModel

class FileMetadata(BaseModel):
    id: str
    filename: str
    content_type: str
    status: str
