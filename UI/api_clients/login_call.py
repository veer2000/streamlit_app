from Backend.src.routes.login import loginUser



async def validate_user(email:str, password:str):
    response = await loginUser(email,password)
    if response:
        return True
    else:
        return False