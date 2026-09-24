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