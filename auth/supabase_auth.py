from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



#===================================Register User================================================================
######

def sign_up(email: str, password: str):

    try:
        response = supabase.auth.sign_up({
        "email" : email,
        "password" : password
        })
        return response
    except Exception as e:
        print("❌ Signup Error:", str(e))
        return None

    
    


#=========================================================Login User===============================================


def login(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print("❌ Login Error:", str(e))
        return None

#========================================================Log Out====================================================

def logout():
    try:
        supabase.auth.sign_out()
        print("✅ Logged out")
    except Exception as e:
        print("❌ Logout Error:", str(e))


#==================================================== Get User ID=================================================

def get_user_id(session):
    try:
        return session.user.id
    except:
        return None

