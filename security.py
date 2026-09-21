from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException

SECRET_KEY = "uma-chave-secreta-muito-dificil-123"
ALGORITHM = "HS256"

security = HTTPBearer()

password_hash = PasswordHash.recommended()

def gerar_hash_senha(senha: str):
    return password_hash.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return password_hash.verify(senha, senha_hash)

def criar_token(dados: dict, tempo_expiracao: timedelta):
    dados_token = dados.copy()

    expiracao = datetime.now(timezone.utc) + tempo_expiracao
    dados_token.update({"exp": expiracao})

    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

    return token

def verificar_token(token: str):
    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return dados

    except jwt.InvalidTokenError:
        return None

def usuario_autenticado(
    credenciais = Depends(security)
):
    token = credenciais.credentials

    dados = verificar_token(token)

    if dados is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    return dados

def somente_admin(usuario = Depends(usuario_autenticado)):
    if usuario.get("role") != "administrador":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores"
        )

    return usuario