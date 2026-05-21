import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("Supabase_URL")
key : str = os.environ.get("Supabase_key")


supabase: Client = create_client(url, key)

def consultar_datos():
    response = supabase.table("users").select("*").execute()

