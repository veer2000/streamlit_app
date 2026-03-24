from fastapi import FastAPI
import os
from src.routes.login import login_router as login_router


app = FastAPI(title="Streamlit UI API's FastAPI")

app.include_router(login_router)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
