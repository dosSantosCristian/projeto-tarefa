from sqlalchemy import text
from database import engine

with engine.connect() as conexao:
    conexao.execute(
        text(
            "UPDATE usuarios "
            "SET role = 'administrador' "
            "WHERE email = 'admin@teste.com'" 
        )
    )
    conexao.commit()

print("Usuário agora é administrador!")