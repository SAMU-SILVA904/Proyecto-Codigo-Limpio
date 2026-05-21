import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

url: str = os.environ.get("Supabase_URL")
key : str = os.environ.get("Supabase¿_key")

# inicializar cliente
supabase: Client = create_client(url, key)

def consultar_datos():
    # leer datos de la tabla users
    response = supabase.table("users").select("*").execute()

