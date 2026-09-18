from database import SessionLocal
from models import UsuarioDB
from security import gerar_hash_senha

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

def criar_usuario(nome: str, email: str, senha: str):
    db = SessionLocal()

    try:
        senha_hash = gerar_hash_senha(senha)

        novo_usuario = UsuarioDB(
            nome=nome,
            email=email,
            senha_hash=senha_hash
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
