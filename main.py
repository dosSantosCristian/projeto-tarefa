from fastapi import FastAPI, HTTPException

from database import engine, Base
from models import UsuarioDB, Usuario
from pydantic import BaseModel
from services import (
    buscar_usuario, 
    listar_usuarios, 
    deletar_usuario,
    atualizar_usuario,
    criar_usuario
)

Base.metadata.create_all(bind=engine)

# Criando uma instância da aplicação FastAPI
app = FastAPI()

# Dados
tasks = [
    {
        "id": 1,
        "title": "Estudar FastAPI",
        "completed": False
    },
    {
        "id": 2,
        "title": "Criar minha primeira API",
        "completed": True
    }
]

# Models
class TaskCreate(BaseModel):
    title: str
    completed: bool

# Rotas
@app.get("/")
def home():
    # Retorna o dicionário que será convertido em json
    return {"message": "Vai, Corinthians!"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
        
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.get("/usuarios/{id}")
def buscar_usuario_route(id: int):

    usuario = buscar_usuario(id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

    if id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID inválido"
        )
    
    return buscar_usuario(id)

@app.get("/usuarios")
def listar_usuarios_route():
    return listar_usuarios()

@app.post("/tasks")
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)

    return new_task

@app.post("/usuarios")
def criar_usuario_route(usuario: Usuario):
    return criar_usuario(usuario.nome)

@app.delete("/usuarios/{id}")
def deletar_usuario_route(id: int):

    usuario = deletar_usuario(id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@app.put("/usuarios/{id}")
def atualizar_usuario_route(id: int, usuario: Usuario):

    usuario_atualizado = atualizar_usuario(
        id,
        usuario.nome
    )

    if usuario_atualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario_atualizado