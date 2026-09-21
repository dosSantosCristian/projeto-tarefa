from sqlalchemy import text
from database import engine

with engine.connect() as conexao:
    conexao.execute(
        text(
            "ALTER TABLE usuarios "
            "ADD COLUMN role VARCHAR DEFAULT 'cliente'"
        )
    )
    conexao.commit()

print("Banco atualizado com sucesso!")