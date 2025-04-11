from pydantic import BaseModel
from typing import List

class MisionBase(BaseModel):
    descripcion: str
    experiencia: int

class MisionCreate(MisionBase):
    pass

class Mision(MisionBase):
    id: int

    class Config:
        orm_mode = True

class PersonajeBase(BaseModel):
    nombre: str

class PersonajeCreate(PersonajeBase):
    pass

class Personaje(PersonajeBase):
    id: int
    experiencia: int
    misiones: List[Mision] = []

    class Config:
        orm_mode = True