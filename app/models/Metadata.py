from sqlalchemy import Column, String
from app.db.database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    content_type = Column(String)
    status = Column(String)
