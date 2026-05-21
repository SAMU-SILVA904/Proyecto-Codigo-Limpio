"""
Cliente HTTP para comunicarse con la API FastAPI del Supermercado.
Centraliza toda comunicación entre Streamlit y el backend.
"""

import httpx
from src.core.config import settings

_TIMEOUT = 10.0

class ApiClient:
    """Cliente HTTP liviano sobre httpx para consumir la API FastAPI."""

    def __init__(self) -> None:
        self.base_url = settings.api_base_url.rstrip("/")


    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _handle(response: httpx.Response) -> tuple[dict | list | None, str | None]:
        """Procesa una respuesta HTTP y retorna (data, error)."""
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return None, None
            return response.json(), None
        except httpx.HTTPStatusError:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            return None, str(detail)


    def get(self, path: str) -> tuple[list | dict | None, str | None]:
        """GET al path indicado."""
        try:
            r = httpx.get(self._url(path), timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def post(self, path: str, body: dict = None, params: dict = None) -> tuple[dict | None, str | None]:
        """POST al path indicado."""
        try:
            r = httpx.post(self._url(path), json=body, params=params, timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"

    def delete(self, path: str) -> tuple[None, str | None]:
        """DELETE al path indicado."""
        try:
            r = httpx.delete(self._url(path), timeout=_TIMEOUT)
            return self._handle(r)
        except httpx.RequestError as e:
            return None, f"No se pudo conectar con la API: {e}"
    
    def patch(self, endpoint: str, data: dict = None, body: dict = None):
        """
        Realiza una petición HTTP PATCH al backend.
        Soporta 'data' o 'body' para evitar conflictos con el formulario de Streamlit.
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            payload = body if body is not None else data
            
            import requests
            response = requests.patch(url, json=payload)
            
            if response.status_code in [200, 204]:
                return response.json() if response.text else {}, None
                
            return None, response.text
        except Exception as e:
            return None, str(e)