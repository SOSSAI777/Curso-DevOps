# Curso-DevOps: API de Lista de Tarefas

API REST para gerenciamento de tarefas, desenvolvida na disciplina de Extensão DevOps (PUCPR, 2026/2). O projeto integra desenvolvimento, testes automatizados, empacotamento em container, integração e entrega contínuas (CI/CD) e implantação em nuvem.

## Descrição da aplicação

A aplicação permite criar, listar, consultar, concluir e remover tarefas. Cada tarefa possui identificador, título, descrição opcional, data de criação e indicação de conclusão. Os dados são persistidos em um banco PostgreSQL.

A documentação interativa é gerada automaticamente pelo FastAPI e fica disponível em `/docs`.

### Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Rota raiz, retorna uma mensagem de boas-vindas |
| GET | `/autor` | Retorna o nome do autor da aplicação |
| GET | `/tarefas` | Lista todas as tarefas |
| POST | `/tarefas` | Cria uma tarefa (parâmetros de query: `titulo`, obrigatório, e `descricao`, opcional) |
| GET | `/tarefas/{id_tarefa}` | Consulta uma tarefa pelo id |
| PUT | `/tarefas/{id_tarefa}` | Marca uma tarefa como concluída |
| DELETE | `/tarefas/{id_tarefa}` | Remove uma tarefa |

## Tecnologias utilizadas

- **Python 3.14** e **FastAPI**: API REST e documentação automática
- **SQLModel / SQLAlchemy** com **PostgreSQL** (driver `psycopg`): persistência de dados
- **pytest**: testes automatizados
- **pylint**: análise estática de código
- **Docker** e **Docker Hub**: empacotamento e publicação da imagem
- **GitHub Actions**: integração e entrega contínuas
- **Render**: implantação da aplicação e do banco de dados

## Execução local

### Pré-requisitos

- Python 3.14
- Docker (para subir o PostgreSQL localmente)

### 1. Clonar o repositório e instalar as dependências

```bash
git clone https://github.com/SOSSAI777/Curso-DevOps.git
cd Curso-DevOps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Subir um banco PostgreSQL

```bash
docker run --name postgres-tarefas \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=senha \
  -e POSTGRES_DB=tarefas \
  -p 5432:5432 -d postgres:16
```

### 3. Definir as variáveis de ambiente

A aplicação encerra na inicialização se alguma destas variáveis estiver ausente:

```bash
export DATABASE_USERNAME=usuario
export DATABASE_PASSWORD=senha
export DATABASE_ADDRESS=localhost:5432
export DATABASE=tarefas
```

### 4. Iniciar a API

```bash
fastapi dev app/api.py
```

A API fica disponível em `http://localhost:8000`, e a documentação em `http://localhost:8000/docs`. As tabelas são criadas automaticamente na inicialização.

### Executar com Docker

```bash
docker build -t tarefas .
docker run -p 8000:8000 \
  -e DATABASE_USERNAME=usuario \
  -e DATABASE_PASSWORD=senha \
  -e DATABASE_ADDRESS=<host-do-banco>:5432 \
  -e DATABASE=tarefas \
  tarefas
```

O endereço do banco deve ser alcançável a partir do container.

### Testes e análise estática

```bash
pylint app
pytest --rootdir app
```

Os testes substituem a conexão com o PostgreSQL por um banco SQLite, portanto não exigem banco externo.

## Pipeline de CI/CD

O workflow `.github/workflows/python-app.yml` é executado em *pushes* e *pull requests* para a branch `main`, e também pode ser disparado manualmente.

1. **build** (CI): instala as dependências, executa o `pylint` e o `pytest`.
2. **entrega** (CD): executa somente na `main`, após o sucesso do `build`. Constrói a imagem Docker e a publica no Docker Hub (`sossai18/tarefas`), com duas tags: o SHA do commit e `latest`. Em seguida, aciona o deploy no Render.

Em *pull requests*, apenas o job `build` é executado, e o job `entrega` é ignorado.

### Configuração necessária no repositório

| Tipo | Nome | Uso |
|------|------|-----|
| Variável | `DOCKERHUB_USER` | Usuário do Docker Hub |
| Secret | `DOCKERHUB_TOKEN` | Token de acesso do Docker Hub |
| Secret | `RENDER_DEPLOY_HOOK` | URL do *deploy hook* do serviço no Render |

## Implantação

A aplicação é executada no Render como um serviço web baseado na imagem do Docker Hub, conectado a um banco PostgreSQL gerenciado pelo Render. As variáveis `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_ADDRESS`, `DATABASE` e `PORT` são configuradas no painel do serviço.

URL pública: https://api-jy5p.onrender.com (documentação em `/docs`).

No plano gratuito do Render, o serviço hiberna após um período de inatividade, e a primeira requisição pode levar cerca de um minuto.

## Autor

Matheus Ricordi Sossai