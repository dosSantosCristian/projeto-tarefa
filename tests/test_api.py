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

def test_buscar_usuario(client):
    cadastro = client.post(
        "/usuarios",
        json={
            "nome": "Usuario Busca",
            "email": "busca@teste.com",
            "senha": "Teste1234"
        }
    )

    id_usuario = cadastro.json()["id"]

    resposta = client.get(f"/usuarios/{id_usuario}")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Usuario Busca"
    assert resposta.json()["email"] == "busca@teste.com"

def test_buscar_usuario_inexistente(client):
    resposta = client.get("/usuarios/9999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Usuário não encontrado"

def test_listar_usuarios(client):
    client.post(
        "/usuarios",
        json={
            "nome": "Usuario 1",
            "email": "usuario1@teste.com",
            "senha": "Teste1234"
        }
    )

    client.post(
        "/usuarios",
        json={
            "nome": "Usuario 2",
            "email": "usuario2@teste.com",
            "senha": "Teste1234"
        }
    )

    resposta = client.get("/usuarios")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 2
    assert resposta.json()[0]["nome"] == "Usuario 1"
    assert resposta.json()[1]["nome"] == "Usuario 2"

def test_atualizar_usuario(client):
    cadastro = client.post(
        "/usuarios",
        json={
            "nome": "Nome Antigo",
            "email": "atualizar@teste.com",
            "senha": "Teste1234"
        }
    )

    id_usuario = cadastro.json()["id"]

    resposta = client.put(
        f"/usuarios/{id_usuario}",
        json={
            "nome": "Nome Novo"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Nome Novo"
    assert resposta.json()["email"] == "atualizar@teste.com"

def test_deletar_usuario_admin(client):
    cadastro = client.post(
        "/usuarios",
        json={
            "nome": "Usuario Alvo",
            "email": "alvo.delete@teste.com",
            "senha": "Teste1234"
        }
    )

    id_usuario = cadastro.json()["id"]

    client.post(
        "/usuarios",
        json={
            "nome": "Admin Delete",
            "email": "admin.delete@teste.com",
            "senha": "Teste1234"
        }
    )

    db = TestingSessionLocal()

    admin = db.query(UsuarioDB).filter(
        UsuarioDB.email == "admin.delete@teste.com"
    ).first()

    admin.role = "administrador"

    db.commit()
    db.close()

    login = client.post(
        "/login",
        json={
            "email": "admin.delete@teste.com",
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

    assert resposta.status_code == 200
    assert resposta.json()["id"] == id_usuario