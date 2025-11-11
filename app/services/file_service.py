import uuid
from app.models.file_model import FileMetadata

async def handle_file_upload(file):
    file_id = str(uuid.uuid4())
    filename = file.filename
    content_type = file.content_type

    metadata = FileMetadata(
        id=file_id,
        filename=filename,
        content_type=content_type,
        status="UPLOADED"
    )
    return metadata.dict()
