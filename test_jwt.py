from datetime import timedelta

from security import criar_token

token = criar_token(
    {"sub": "1"},
    timedelta(minutes=30)
)

print(token)