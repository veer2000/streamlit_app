# NOTE: app should be start with root directory named streamlit_ui
first enter in your Virtual environment based on terminal you used find the command and use 
I used = source .\.venv\Script\activate

prerequisite  = need to install requirement.txt
isntall command = pip install -r requiremets.txt 

first install Mysql database create a database and a table User 
I have used MysqlDatabase and database name streamlit and table name users 

create a .env file inside C:\Users\**\**\streamlit_ui\Backend and add this variable " DB_URL='mysql+pymysql://root:admin@localhost:3306/streamlit' "
definition = 'mysql+pymysql://user:password@localhost:port/databasename'

to run backend and UI as we need  one terminal it should be from root to execute Streamlit UI example "PS C:\Users\**\**\streamlit_ui>"
if you only want to run backend for api testing use second terminal  from Backend example "C:\Users\**\**\streamlit_ui\Backend>"

next run command to execute streamlit

streamlit = "PS C:\Users\**\**\streamlit_ui> streamlit run .\app.py'
result = "
PS C:\Users\**\**\streamlit_ui> streamlit run .\app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.91.0.96:8501

"

2nd terminal on only use backend to test database and api's

Backend = " PS C:\Users\**\**\streamlit_ui\Backend> uvicorn main:app --reload"
result = "
(.venv) PS C:\Users\**\**\streamlit_ui\Backend> uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\**\\**\\streamlit_ui\\Backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9860] using StatReload
INFO:     Started server process [24240]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
"
to access API's directly using Swagger a UI interface use endpoint "http://127.0.0.1:8000/docs#"
after running streamlit it opens automatically on default browser 

 " ** to stop repeated login you set ** "
ORIGINAL
"if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
"
UPDATED
"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
"  what this will do it will directly log you in without asking login details


if changes needed in UI you need to check/find
def card1():
def card2():

if changes needed in api's check Backend/src/services/curd.py
def get_draft_response():
def get_allocated_email():

login logic check Backend/src/routes/login.py
@login_router.get("/login")
async def loginUser(



pip install extra-streamlit-components
pip install streamlit-tinymce -> replacement is - pip install st-tiny-editor