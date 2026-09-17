from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)

class Usuario(BaseModel):
    nome: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str

    model_config = {
        "from_attributes": True
    }