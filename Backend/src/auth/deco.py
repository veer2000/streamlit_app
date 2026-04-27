import functools
import bcrypt
import httpx
from functools import wraps
import inspect
from fastapi import HTTPException
from ..services.database import SessionLocal



def with_access_token(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # print(f'Entered function {func.__name__}')
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=None,
                    data=None,
                )
                response.raise_for_status()
                token_data = response.json()
                token = token_data.get("access_token")

            kwargs["valid_access_token"] = str(token)
            return await func(*args, **kwargs)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Token Error: {str(e)}")

    return wrapper


#Dependency
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()


def hash_arg(arg_name):
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(fun)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            if arg_name in bound_args.arguments:
                raw_password = bound_args.arguments[arg_name]
                bound_args.arguments["password_original"] = raw_password

                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)

                bound_args.arguments[arg_name] = hashed.decode('utf-8')

            return fun(*bound_args.args, **bound_args.kwargs)

        return wrapper

    return decorator