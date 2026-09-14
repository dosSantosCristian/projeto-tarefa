from database import SessionLocal
from models import UsuarioDB

def listar_usuarios():
    db = SessionLocal()

    usuarios = db.query(UsuarioDB).all()

    db.close()
    
    return usuarios

def buscar_usuario(id: int):
    db = SessionLocal()

    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    db.close()

    return usuario

def deletar_usuario(id: int):
    db = SessionLocal()

    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if usuario is None:
        db.close()
        return None

    db.delete(usuario)
    db.commit()

    db.close()

    return usuario

def atualizar_usuario(id: int, nome: str):
    db = SessionLocal()

    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()

    if usuario is None:
        db.close()
        return None

    usuario.nome = nome

    db.commit()
    db.refresh(usuario)

    db.close()

    return usuario

def criar_usuario(nome: str):
    db = SessionLocal()

    novo_usuario = UsuarioDB(nome=nome)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    db.close()

    return novo_usuario