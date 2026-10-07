Task API

API REST desenvolvida com FastAPI para gerencimaneto de usuários e tarefas.

O projeto conta com cadastro e atualização de usuários, autenticação com JWT, controle de aceso por níveis de usuários e testes automatizados.

🛠️ Tecnologias

• Python
• FastAPI
• SQLAlchemy
• SQLite
• Pydantic
• JWT
• Pytest
• Git e GitHub

📁 Estrutura do projeto

task-api/
├── main.py
├── database.py
├── models.py
├── services.py
├── security.py
├── migrar_banco.py
├── tornar_admin.py
├── requirements.txt
├── .gitignore
├── README.md
└── tests/
    ├── conftest.py
    └── test_api.py

Os arquivos .env, usuarios.db e teste.db são criados localmente e não são versionados pelo Git.


⚙️ Instalação

1. Clone o repositório
git clone https://github.com/dosSantosCristian/projeto-tarefa.git
cd projeto-tarefa

2. Crie o ambiente virtual

No Windows:

python -m venv .venv
.venv\Scripts\activate

No Linux:

python3 -m venv .venv
source .venv/bin/activate

3. Instale as dependências

python -m pip install -r requirements.txt

🔐 4. Coonfigure o arquivo .env

Crie um arquivo chamado .env na raiz do projeto:

SECRET_KEY=sua-chave-secreta

A SECRET_KEY é utilizada para assinar os tokens JWT.

▶️ Executando a API

Com o ambiente virtual ativado, execute:

uvicorn main:app --reload

A API estará disponível em:
http://127.0.0.1:8000

📚 Documentação da API

O FastAPI disponibiliza automaticamente a documentação interativa:

http://127.0.0.1:8000/redoc

🧪 Testes

O projeto possui testes automatizados utilizando Pytest.

Para executar os testes:

python -m pytest

Os testes verificam funcionalidades como:

• Cadastro de usuários
• Login
• Autenticação com JWT
• Acesso a área administrativa
• Busca de usuários
• Listagem de usuários
• Atualização de usuários
• Exclusão de usuários
• Validação de permissões
• Tratamento de usuários inexistentes.

📚 Principais endpoints

👤 Usuários

Método	    Endpoint	        Descrição
POST	    /usuarios	        Cadastra um novo usuário
GET	        /usuarios	        Lista todos os usuários
GET	        /usuarios/{id}	    Busca um usuário pelo ID
PUT	        /usuarios/{id}	    Atualiza um usuário
DELETE	    /usuarios/{id}	    Exclui um usuário

🔐 Autenticação

Método	 Endpoint	    Descrição
POST	 /login	        Realiza login e gera um token JWT
GET	     /perfil	    Retorna os dados do usuário autenticado
GET	     /admin	        Acessa a área exclusiva de administradores

📝 Tarefas
Método	Endpoint	Descrição
GET	    /tasks	    Lista as tarefas

🔐 Autenticação e permissões

A API utiliza JWT (JSON Web Token) para autenticação.

Após realizar o login através de:

POST /login

a API retorna um access_token.

Esse token deve ser enviado nas requisições protegidas utilizando o cabeçalho:

Authorization: Bearer SEU_TOKEN

👥 Níveis de acesso

A API possui dois níveis de usuário:

• cliente - acesso às funcionalidades comuns.
• administrador - acesso às funcionalidades administrativas.

A rota:

GET /admin

é protegida e pode ser acessada somente por usuários com a função administrador.

A exclusão de usuários também exige permissão de administrador.

🎯 Objetivo

Este projeto foi desenvolvido com o bjetivo de praticar e consolidar conhecimentos em desenvolvimentoo de APIs REST com Python e FastAPI.

Durante o desenvolvimento foram aplicados conceitos de:

• Desenvolvimento de APIs REST
• Banco de dados com SQLAlchemy e SQLite
• Validação de dados com Pydantic
• Autenticação e autorização com JWT
• Controle de acesso por níveis de usuário
• Testes automatizados com Pytest
• Organização e versionamento de código com Git e GitHub
