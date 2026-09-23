from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {"message": "Vai, Corinthians!"}

def teste_criar_usuario():
    resposta = client.post(
        "/usuarios",
        json={
            "nome": "Usuario Teste",
            "email": "usuario.teste@teste.com",
            "senha": "Teste1234"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Usuario Teste"
    assert resposta.json()["email"] == "usuario.teste@teste.com"