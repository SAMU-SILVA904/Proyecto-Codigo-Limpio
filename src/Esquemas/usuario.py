"""Esquemas de validación Pydantic para la entidad Usuario según el SQL real."""

from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., examples=["Joaquín Laura"])
    rol_id: int = Field(..., description="5 para Gerente, 6 para Empleado", examples=[6])

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    model_config = {"from_attributes": True}
    
    