from permit import Permit
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.core.permit_config import user, permit

router = APIRouter(prefix="/permit", tags=["Permit"])

@router.get("/")
async def check_permissions():  # After we created this user in the previous step, we also synced the user's identifier # to permit.io servers with permit.write(permit.api.syncUser(user)). The user identifier # can be anything (email, db id, etc) but must be unique for each user. Now that the # user is synced, we can use its identifier to check permissions with 'permit.check()'.
    permitted = await permit.check(user["id"], "read", "Document")
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
            "success": False,
            "result": f"{user.get('firstName')} {user.get('lastName')} is NOT PERMITTED to read document!"
        })
 
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "success": True,
        "result": f"{user.get('firstName')} {user.get('lastName')} is PERMITTED to read document!"
    })


@router.get("/debug/resources")
async def debug_resources():
    return await permit.api.resources.list()

@router.get("/debug/roles")
async def debug_roles():
    return await permit.api.roles.list()

@router.get("/debug/actions")
async def debug_actions():
    return await permit.api.actions.list()