from fastapi import APIRouter
from notifications.services import event_logger


router = APIRouter(prefix="/notifications",tags=["notifications"])

@router.get("/profile/{user_id}")
async def get(user_id:int):
    content = {'user_id':user_id,'title':"Profile Setup Complete",'description':'Congrats! You have successfully setup your profile'}
    await event_logger.log_event('PROFILE_SETUP', content)
    return content

@router.get("/subscription/{user_id}")
async def get(user_id:int):
    content = {'user_id':user_id,'title':"Subscription Expiring Soon",'description':'Hurry up! Your subscription is expiring soon'}
    await event_logger.log_event('SUBSCRIPTION_EXPIRY', content)
    return content