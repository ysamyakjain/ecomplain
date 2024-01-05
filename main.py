import logging
from fastapi import FastAPI
from pydantic import BaseModel 
from typing import Optional
import phonenumbers
import re
from fastapi.middleware.cors import CORSMiddleware



from database_connection import Database

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class NewRequest(BaseModel):
    user_name: str
    user_email: str
    user_phone: Optional[str] = None
    user_problem: str


def valid_phone_number(phone_number: str, country: str = 'IN') -> bool:
    try:
        parsed_number = phonenumbers.parse(phone_number, country)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def valid_email_checker(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(email_regex, email))

@app.get("/")
async def home():
    db_instance = Database()
    return {"message": "APIs are up and running"}

@app.post("/newrequest")
async def new_request(user_info: NewRequest):
    # Check if the email is valid
    if not valid_email_checker(user_info.user_email):
        return {"message": "Invalid email address"}
    
    if user_info.user_phone is not None:
        # Check if the phone number is valid
        if not valid_phone_number(user_info.user_phone):
            return {"message": "Invalid phone number"}
        
    # Connect to the database
    db_instance = Database()
    await db_instance.db_connect()
    # Insert the user info into the database
    query = f"""insert into user_queries.user_stuff(user_name, user_email, user_phone, user_problem) 
                values('{user_info.user_name}',
                '{user_info.user_email}',
                '{user_info.user_phone}',
                '{user_info.user_problem}'
                );"""
    await db_instance.db_execute_query(query)
    await db_instance.db_disconnect()
    return {"message": "Request received"}

@app.get("/fetchrequest")
async def all_requests():
    # Connect to the database
    db_instance = Database()
    await db_instance.db_connect()
    # Get all the requests from the database
    query = f"select * from user_queries.user_stuff;"
    result = await db_instance.db_fetch_results(query)
    logging.info(f'result from db: {result}')
    await db_instance.db_disconnect()
    return result
