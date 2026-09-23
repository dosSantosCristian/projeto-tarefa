from fastapi import FastAPI, HTTPException, Depends
from datetime import timedelta

from security import criar_token, usuario_autenticado, somente_admin

from database import engine, Base, get_db
from models import (
    UsuarioDB,
    Usuario,
    UsuarioResponse,
    UsuarioUpdate,
    UsuarioLogin
)
from pydantic import BaseModel
from services import (
    buscar_usuario, 
    listar_usuarios, 
    deletar_usuario,
    atualizar_usuario,
    criar_usuario,
    autenticar_usuario
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

@app.get("/usuarios/{id}", response_model=UsuarioResponse)
def buscar_usuario_route(id: int, db = Depends(get_db)):

    if id <= 0:
            raise HTTPException(
                status_code=400,
                detail="ID inválido"
            )
        
    usuario = buscar_usuario(id, db)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario

@app.post("/tasks")
def create_task(task: TaskCreate):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "completed": task.completed
    }

    tasks.append(new_task)

    return new_task

@app.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario_route(usuario: Usuario):

    try:
        return criar_usuario(
            usuario.nome,
            usuario.email,
            usuario.senha
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        )

@app.delete("/usuarios/{id}")
def deletar_usuario_route(
    id: int,
    usuario = Depends(somente_admin)
):

    usuario_deletado = deletar_usuario(id)

    if usuario_deletado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario_deletado

@app.put("/usuarios/{id}", response_model=UsuarioResponse)
def atualizar_usuario_route(id: int, usuario: UsuarioUpdate):

    try:
        usuario_atualizado = atualizar_usuario(
            id,
            usuario.nome,
            usuario.email
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=409,
            detail=str(erro)
        )

    if usuario_atualizado is None:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario_atualizado

@app.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios_route(db = Depends(get_db)):
    return listar_usuarios(db)

@app.post("/login")
def login(usuario: UsuarioLogin):

    usuario_autenticado = autenticar_usuario(
        usuario.email,
        usuario.senha
    )

    if usuario_autenticado is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    token = criar_token(
        {
            "sub": str(usuario_autenticado.id),
            "role": usuario_autenticado.role
        },
        timedelta(minutes=30)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/perfil")
def perfil(usuario = Depends(usuario_autenticado)):
    return {
        "mensagem": "Você está autenticado!",
        "usuario": usuario
    }

@app.get("/admin")
def area_admin(usuario = Depends(somente_admin)):
    return {
        "mensagem": "Bem vindo à área administrativa!",
        "usuario": usuario
    }