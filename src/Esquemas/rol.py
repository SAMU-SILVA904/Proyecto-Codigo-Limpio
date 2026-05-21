from pydantic import BaseModel, Field

class RolBase(BaseModel):
    nombre: str = Field(..., max_length=50)

class Rol(RolBase):
    rol_id: int
    
    class Config:
        from_attributes = True

