from collections.abc import Callable
from typing import Any, TypeVar

from supabase import Client, create_client

from src.core.config import settings
from src.core.excepciones import StorageError

T = TypeVar("T")


class BaseRepository:
    """Clase base que todos los repositorios concretos deben heredar.
    
    Provee:
    self.client: cliente Supabase listo para usar.
    
    self._execute(operation, fn): ejecuta una llamada al SDK y
    atrapa excepciones convirtiendolas en StorageError.
    """

    def __init__(self) -> None:
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key,
        )

    def _execute(self, operation: str, fn: Callable[[], Any]) -> Any:
        """Ejecuta fn y convierte excepciones del SDK en StorageError.

        Args:
            operation: Nombre descriptivo de la operacion (para logs/errores).
            fn: Callable sin argumentos que realiza la llamada al SDK.

        Returns:
            El resultado de fn() si no hay errores.

        Raises:
            StorageError: Si el SDK lanza cualquier excepcion.
        """
        try:
            return fn()
        except StorageError:
            raise
        except Exception as exc:
            raise StorageError(operation=operation, detail=str(exc)) from exc

    @staticmethod
    def _require_data(response: Any, operation: str) -> list[dict]:
        """Valida que la respuesta del SDK contenga datos.

        El SDK de Supabase devuelve un objeto con atributo .data.
        Este helper extrae esa lista y lanza StorageError si esta vacia
        o ausente, indicando un fallo silencioso de la BD.

        Args:
            response: Objeto de respuesta devuelto por el SDK.
            operation: Nombre de la operacion, usado en el mensaje de error.

        Returns:
            Lista de diccionarios con los registros devueltos.

        Raises:
            StorageError: Si response.data esta vacio o es None.
        """
        
        data: list[dict] | None = getattr(response, "data", None)
        if not data:
            raise StorageError(
                operation=operation,
                detail="La operacion no retorno datos. Verifique los parametros.",
            )
        return data
