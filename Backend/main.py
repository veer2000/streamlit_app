from fastapi import FastAPI
import os
from src.routes.login import login_router as login_router
from src.routes.admin import admin_routes as admin_routes
from src.routes.emailstatus import email_router as email_router

app = FastAPI(title="Streamlit UI API's FastAPI")

app.include_router(login_router)
app.include_router(admin_routes)
app.include_router(email_router)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
