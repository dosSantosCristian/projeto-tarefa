from tests.conftest import TestingSessionLocal
from models import UsuarioDB

def test_home(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {"message": "Vai, Corinthians!"}

def test_criar_usuario(client):
    resposta = client.post(
        "/usuarios",
        json={
            "nome": "Usuario Teste",
            "email": "usuario.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"]== "Usuario Teste"
    assert resposta.json()["email"] == "usuario.teste@teste.com"

def test_login(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Login Teste",
            "email": "login.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    resposta = client.post(
        "/login",
        json={
            "email": "login.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    assert resposta.status_code == 200
    assert "access_token" in resposta.json()
    assert resposta.json()["token_type"] == "bearer"

def test_login_senha_invalida(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Login Inválido",
            "email": "login.invalido@teste.com",
            "senha": "Teste1234"
        }
    )

    resposta = client.post(
        "/login",
        json={
            "email": "login.invalido@teste.com",
            "senha": "SenhaErrada"
        }
    )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Email ou senha inválidos"

def test_perfil_sem_token(client):
    resposta = client.get("/perfil")

    assert resposta.status_code == 401

def test_perfil_com_token(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Perfil Teste",
            "email": "perfil.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    login = client.post(
        "/login",
        json={
            "email": "perfil.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    token = login.json()["access_token"]

    resposta = client.get(
        "/perfil",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Você está autenticado!"

def test_admin_usuario_comum(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Usuario Comum",
            "email": "usuario.comum@teste.com",
            "senha": "Teste1234"
        }
    )

    login = client.post(
        "/login",
        json={
            "email": "usuario.comum@teste.com",
            "senha": "Teste1234"
        }
    )

    token = login.json()["access_token"]

    resposta = client.get(
        "/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 403
    assert resposta.json()["detail"] == "Acesso permitido apenas para administradores"

def test_admin_usuario_admin(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Admin Teste",
            "email": "admin.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    db = TestingSessionLocal()

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.email == "admin.teste@teste.com"
    ).first()

    usuario.role = "administrador"

    db.commit()
    db.close()

    login = client.post(
        "/login",
        json={
            "email": "admin.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    token = login.json()["access_token"]

    resposta = client.get(
        "/admin",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Bem vindo à área administrativa!"

def test_deletar_usuario_sem_permissao(client):
    cadastro = client.post(
        "/usuarios",
        json={
            "nome": "Usuario Alvo",
            "email": "alvo@teste.com",
            "senha": "Teste1234"
        }
    )

    id_usuario = cadastro.json()["id"]

    client.post(
        "/usuarios",
        json={
            "nome": "Usuario Comum",
            "email": "comum.delete@teste.com",
            "senha": "Teste1234"
        }
    )

    login = client.post(
        "/login",
        json={
            "email": "comum.delete@teste.com",
            "senha": "Teste1234"
        }
    )

    token = login.json()["access_token"]

    resposta = client.delete(
        f"/usuarios/{id_usuario}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert resposta.status_code == 403