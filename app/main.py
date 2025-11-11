from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.v1.routes import file_routes

load_dotenv()

app = FastAPI(
    title="MinIO File Service",
    version="1.0.0",
    description="Upload and download files securely using presigned URLs from MinIO."
)

# 👇 This is critical
app.include_router(file_routes.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "MinIO File Service is running 🚀"}





# from fastapi import FastAPI, Request, status
# from permit import Permit
# from pydantic import BaseModel, EmailStr, ValidationError
# import os
# from fastapi.responses import JSONResponse
# from app.api.v1.routes import file_routes
# from app.db.database import Base, engine
# from app.models.Metadata import FileMetadata

# # Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="File Service API",
#     version="1.0.0",
#     description="Handles file upload, metadata, and scan results."
# )

# # app.include_router(file_routes.router, prefix="/api/v1/files", tags=["Files"])

# class UserIn(BaseModel):
#     email: EmailStr
#     first_name: str
#     last_name: str
# permit = Permit(
#     token=os.getenv("PERMIT_API_KEY"),
#     pdp=os.getenv("PERMIT_PDP_KEY")
# )
# @app.get("/")
# def root():
#     return {"message": "File Service is running "}

# # main.py
# @app.post("/register")
# async def register(user_in: UserIn):
#     try:
#         user = await permit.api.users.sync(
#             {
#                 "key": user_in.email,
#                 "email": user_in.email,
#                 "first_name": user_in.first_name,
#                 "last_name": user_in.last_name,
#             }
#         )
#         # Assign role as part of registration
#         role_assignment = await permit.api.users.assign_role({
#             "user": user_in.email,
#             "role": "Reader",
#             "tenant": "default",
#         })
#         return {
#             "message": "User registered and role assigned",
#             "user": user,
#             "role_assignment": role_assignment
#         }
#     except ValidationError as e:
#         return JSONResponse(content=e.errors(), status_code=422)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000, reload=True)
