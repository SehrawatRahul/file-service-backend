from permit import Permit

permit = Permit(  # in production, you might need to change this url to fit your deployment
    pdp="https://cloudpdp.api.permit.io",  # your api key
    token="permit_key_A7fcSuEtekjPP8wqrBbCllnvZ5eIm0xqJ4y550SC4cAgivpqhcGWttS8Sr92SMjqKSr5NfP8EU4JXf6FnMBA72",
)

user = {
    "id": "John@Doe.com",
    "firstName": "John",
    "lastName": "Doe",
    "email": "John@Doe.com",
}  # in a real app, you would typically decode the user id from a JWT token

async def assign_role():
    await permit.api.assign_role("viewer", "John@Doe.com")






