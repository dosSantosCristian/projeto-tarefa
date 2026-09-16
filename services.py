from database import SessionLocal
from models import UsuarioDB

def listar_usuarios():
    db = SessionLocal()

    usuarios = db.query(UsuarioDB).all()

    db.close()
    
    return usuarios

def buscar_usuario(id: int):
    db = SessionLocal()

    try:
        usuario = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.id == id)
            .first()
        )

        return usuario

    except Exception:
        db.rollback()
        raise

    finally:
        db.close() 

def deletar_usuario(id: int):
    db = SessionLocal()

    try:
        usuario = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.id == id)
            .first()
        )

        if usuario is None:
            return None

        db.delete(usuario)
        db.commit()

        return usuario

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def atualizar_usuario(id: int, nome: str):
    db = SessionLocal()

    try:
        usuario = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.id == id)
            .first()
        )

        if usuario is None:
            return None

        usuario.nome = nome

        db.commit()
        db.refresh(usuario)

        return usuario

    except Exception:
        db.rollback
        raise

    finally:
        db.close()

def criar_usuario(nome: str):
    db = SessionLocal()

    try:
        novo_usuario = UsuarioDB(nome=nome)

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
