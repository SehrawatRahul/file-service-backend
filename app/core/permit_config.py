import os
from permit import Permit
from dotenv import load_dotenv

load_dotenv()

permit = Permit(  # in production, you might need to change this url to fit your deployment
    pdp=os.getenv('PDP_URL'),  # your api key
    token=os.getenv('PERMIT_TOKEN'),
)

user = {
    "id": "John@Doe.com",
    "firstName": "John",
    "lastName": "Doe",
    "email": "John@Doe.com",
}  # in a real app, you would typically decode the user id from a JWT token

async def assign_role():
    await permit.api.assign_role("viewer", "John@Doe.com")






