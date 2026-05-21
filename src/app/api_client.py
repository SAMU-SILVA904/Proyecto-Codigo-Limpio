"""
Cliente HTTP para comunicarse con la API FastAPI del Supermercado.
Centraliza toda comunicación entre Streamlit y el backend.
"""

import httpx
# Importamos el objeto settings oficial que acabamos de revisar
from src.core.config import settings

# Timeout en segundos para evitar congelamientos en la UI
_TIMEOUT = 10.0

class ApiClient:
    """Cliente HTTP liviano sobre httpx para consumir la API FastAPI."""

    def __init__(self) -> None:
        # Apunta de forma estricta y limpia a la URL base de tu FastAPI local (http://127.0.0.1:8000)
        self.base_url = settings.api_base_url.rstrip("/")

    # ── Helpers privados ──────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        # Limpia y construye la URL concatenando la barra de manera segura
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
                # FastAPI encapsula los mensajes de error en el campo 'detail'
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            return None, str(detail)

    # ── Métodos HTTP públicos ─────────────────────────────────────────────────

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