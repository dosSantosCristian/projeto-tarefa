from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)

class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioUpdate(BaseModel):
    nome: str
    email: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    model_config = {
        "from_attributes": True
    }