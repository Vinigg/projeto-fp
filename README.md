# Sistema de Gestão Escolar Comunitária

O objetivo é criar um sistema web que auxilie escolas públicas ou comunitárias na organização e gestão de seus recursos educacionais, contribuindo com o ODS 4 – Educação de Qualidade.

## Desafio

O sistema permite o cadastro, consulta, atualização e exclusão (CRUD) de informações referentes a:

👨‍🎓 Alunos

👩‍🏫 Professores

🏫 Turmas

Além disso, o projeto inclui relatórios que exibem:

Listagem de alunos por turma

Média geral de desempenho dos alunos

## Tecnologias Utilizadas

Frontend: Bootstrap

Backend / API: Python

Banco de Dados: PostgreSQL

## Lider
- Pedro Augusto Carvalho Araujo

## Equipe

- Vinícius Wagner Gomes Germano
- Emily Raquel Marques da Silva
- Cecilia Victoria Lopes dos Santos
- Vitoria Gabrielly Gomes da Silva
- Pedro Augusto Carvalho Araujo
- Matheus do Nascimento Gomes Vaz

## Requisitos

- Windows 10/11 com PowerShell 5.1 (padrão) ou superior
- Python 3.10+ (recomendado; o projeto usa ambiente virtual)
- Pip (gerenciador de pacotes do Python)
- Git (opcional, para clonar o repositório)

Observações:
- O projeto já possui um banco SQLite (`sistema_escolar/db.sqlite3`) pronto para uso local.
- PostgreSQL é suportado, mas opcional. Veja a seção “Usar PostgreSQL”.

## Estrutura do Projeto

- Backend (Django): `sistema_escolar/`
	- App: `gestao_escolar/`
	- Banco local: `db.sqlite3`
	- `manage.py`, `settings.py`, `urls.py`
- Frontend estático: `frontend/` (HTML, CSS, JS consumindo a API)

## Passo a Passo (Instalação e Execução)

Todas as instruções abaixo são para PowerShell no Windows.

1) Clonar o repositório (ou baixar os arquivos)

```powershell
git clone https://github.com/Vinigg/projeto-fp.git; cd projeto-fp
```

2) Recomenda-se usar ambiente virtual (venv) do Python

Por quê? Isola as dependências do projeto das do sistema.

Criar e ativar a venv:

```powershell
cd sistema_escolar
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Desativar a venv (quando terminar):

```powershell
deactivate
```

3) Instalar dependências do backend (com a venv ativa)

```powershell
pip install -r requirements.txt
```

4) Aplicar migrações do banco

```powershell
python .\manage.py migrate
```

5) (Opcional) Criar um superusuário para acessar o admin do Django

```powershell
python .\manage.py createsuperuser
```

6) Iniciar o servidor de desenvolvimento (API)

```powershell
python .\manage.py runserver
```

- A API ficará disponível em: `http://127.0.0.1:8000/api/v1/`
- Admin Django: `http://127.0.0.1:8000/admin/`

7) Abrir o frontend

O frontend são páginas estáticas em `frontend/` que consomem a API.

Recomendação: usar a extensão Live Server no VS Code para servir o `index.html`:

1. Abra o VS Code na pasta do projeto: `code .`
2. Instale a extensão “Live Server” (Ritwick Dey).
3. Abra `frontend/index.html` no VS Code.
4. Clique em “Go Live” (canto inferior direito) para iniciar.

Alternativa: abrir os arquivos diretamente no navegador, porém recursos de requisição podem ter restrições sem servidor.

- Página inicial (Dashboard): `frontend/index.html`
- Alunos: `frontend/alunos.html`
- Professores: `frontend/professores.html`
- Turmas: `frontend/turmas.html`
- Disciplinas: `frontend/disciplinas.html`
- Notas: `frontend/notas.html`
- Relatórios: `frontend/relatorios.html`

Certifique-se de que o backend esteja rodando, pois o frontend consome a API REST.

## Fluxo de Uso (Ordem recomendada)

1. Cadastrar Disciplinas
2. Cadastrar Professores (selecionando as Disciplinas)
3. Cadastrar Turmas (selecionando os Professores)
4. Cadastrar Alunos (escolhendo a Turma)
5. Lançar Notas (escolhendo Aluno e Disciplina)

## Endpoints Principais (API)

- `GET/POST /api/v1/disciplinas/`
- `GET/PUT/DELETE /api/v1/disciplinas/{id}/`
- `GET/POST /api/v1/professores/` (campo `disciplinas` como array de IDs)
- `GET/PUT/DELETE /api/v1/professores/{id}/`
- `GET/POST /api/v1/turmas/` (campo `professores` como array de IDs)
- `GET/PUT/DELETE /api/v1/turmas/{id}/`
- `GET/POST /api/v1/alunos/`
- `GET/PUT/DELETE /api/v1/alunos/{id}/`
- `GET/POST /api/v1/notas/`
- `GET/PUT/DELETE /api/v1/notas/{id}/`

Validações importantes:
- Turma deve possuir pelo menos 1 professor.
- Nota deve estar entre 0 e 10 e é única por (aluno, disciplina, data).
- A média geral do aluno é calculada dinamicamente (não é editável no frontend).

## Usar PostgreSQL (Opcional)

1) Instale e configure o PostgreSQL localmente.
2) Crie um banco e usuário, por exemplo:

```sql
CREATE DATABASE escola;
CREATE USER escola_user WITH ENCRYPTED PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE escola TO escola_user;
```

3) Configure o `settings.py` (em `sistema_escolar/sistema_escolar/settings.py`) para usar PostgreSQL:

```python
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'escola',
		'USER': 'escola_user',
		'PASSWORD': 'senha_segura',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}
```

4) Execute as migrações novamente:

```powershell
python .\manage.py migrate
```

## Dicas de Desenvolvimento

- Para atualizar dependências, edite `requirements.txt` e rode `pip install -r requirements.txt`.
- Use o admin do Django para verificar dados rapidamente.
- Se alterar modelos, gere novas migrações: `python .\manage.py makemigrations; python .\manage.py migrate`.
- Erros comuns da API geralmente são de serialização/validação — verifique `gestao_escolar/serializers.py`.

