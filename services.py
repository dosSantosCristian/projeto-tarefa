from database import SessionLocal
from models import UsuarioDB
from security import gerar_hash_senha, verificar_senha
from sqlalchemy.exc import IntegrityError

def listar_usuarios(db):
    try:
        usuarios = db.query(UsuarioDB).all()
        return usuarios

    except Exception:
        db.rollback()
        raise  
    
def buscar_usuario(id: int, db):
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

def deletar_usuario(id: int, db):

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

def atualizar_usuario(id: int, nome: str | None, email: str | None, db):

    try:
        usuario = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.id == id)
            .first()
        )

        if usuario is None:
            return None

        if nome is not None:
            usuario.nome = nome
            
        if email is not None:
            usuario.email = email

        db.commit()
        db.refresh(usuario)

        return usuario

    except IntegrityError:
        db.rollback()
        raise ValueError("Email já cadastrado")
    
    except Exception:
        db.rollback()
        raise

def criar_usuario(nome: str, email: str, senha: str, db):

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

    except IntegrityError:
        db.rollback()
        raise ValueError("Email já cadastrado")

    except Exception:
        db.rollback()
        raise

def buscar_usuario_por_email(email: str, db):
    
    try:
        usuario = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.email == email)
            .first()
        )

        return usuario

    except Exception:
        db.rollback()
        raise

def autenticar_usuario(email: str, senha: str, db):
    usuario = buscar_usuario_por_email(email, db)

    if usuario is None:
        return None

    senha_valida = verificar_senha(
        senha,
        usuario.senha_hash
    )

    if not senha_valida:
        return None

    return usuario