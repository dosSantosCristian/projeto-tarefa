from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from sqlalchemy import Column, Integer, String
from database import Base
from typing import Optional

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)
    role = Column(String, default="cliente")

class Usuario(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr
    senha: str = Field(
        min_length=8,
        pattern=r"^[a-zA-Z0-9]+$"
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("O nome não pode conter apenas espaços")

        return valor

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("O nome não pode conter apenas espaços")

        return valor

    @model_validator(mode="after")
    def validar_atualizacao(self):
        if self.nome is None and self.email is None:
            raise ValueError("Informe pelo menos um campo para atualizar")

        return self

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }

class UsuarioLogin(BaseModel):
    email: str
    senha: str