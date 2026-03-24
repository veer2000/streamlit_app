import functools
import bcrypt
import httpx
from fastapi import HTTPException
# from Backend.src.services.database import SessionLocal
from ..services.database import SessionLocal


def with_access_token(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            print(f'Entered function {func.__name__}')
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=None,
                    data=None,
                )
                response.raise_for_status()
                token_data = response.json()
                token = token_data.get("access_token")

            kwargs["valid_access_token"] = str(token)
            # kwargs["valid_access_token"] = str(token_data.get("access_token"))
            return await func(*args, **kwargs)

        except Exception as e:
            # Replicate your original error handling
            raise HTTPException(status_code=400, detail=f"Token Error: {str(e)}")

    return wrapper


#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


def hash_pass(password):
    try:
        print(f'Enterted method {hash_pass.__name__}')
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        print(f'Hashed Password: {hashed_password}')
        # return hashed_password.decode('utf-8')
        return hashed_password
    except Exception as e:
        print(f"Error at {hash_pass.__name__}error: {str(e)}")
        raise


def validate_password(password : bytes, hashed_password : bytes):
    try:
        print(f'Db Password : {password}')
        print(f'Entered and coinverted  Password : {hashed_password}')
        # NOTE: for now lets convert passowrd to bytes to match
        if bcrypt.checkpw(password, hashed_password):
            print("Password match!")
            return True
        else:
            print("Incorrect password.")
            return False
    except Exception as e:
        print(f"Error at {validate_password.__name__} error: {str(e)}")
        raise