
from fastapi.testclient import TestClient
from app import APP, TAREFAS
from unittest.mock import patch

CLIENT = TestClient(APP)

def limpar_tarefas():
    TAREFAS.clear()

def test_listar_tarefas():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Estudar Python",
        "descricao": "Estudar testes unitários"
    })

    resposta = CLIENT.get("/tarefas")

    assert resposta.status_code == 200
    assert resposta.json() == [{"0": "Estudar Python"}]


def test_criar_tarefa():
    limpar_tarefas()

    resposta = CLIENT.post("/tarefas", params={
        "titulo": "Estudar FastAPI",
        "descricao": "Aprender testes com TestClient"
    })

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "OK"}
    assert len(TAREFAS) == 1
    assert TAREFAS[0]["titulo"] == "Estudar FastAPI"
    assert TAREFAS[0]["descricao"] == "Aprender testes com TestClient"


def test_concluir_tarefa():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Finalizar projeto",
        "descricao": "Concluir atividade"
    })

    with patch("app.requests.post") as mock_post:
        resposta = CLIENT.put("/tarefas/0")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa atualizada"}
    assert TAREFAS[0]["concluida"] == True
    assert "concluida_em" in TAREFAS[0]
    mock_post.assert_called_once()


def test_visualizar_tarefa():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Aprender Python",
        "descricao": "Estudar FastAPI"
    })

    resposta = CLIENT.get("/tarefas/0")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == 0
    assert resposta.json()["titulo"] == "Aprender Python"
    assert resposta.json()["descricao"] == "Estudar FastAPI"


def test_apagar_tarefa():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Tarefa para excluir",
        "descricao": "Essa tarefa será removida"
    })

    resposta = CLIENT.delete("/tarefas/0")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa apagada"}
    assert len(TAREFAS) == 0

# Teste da rota inicial
def test_index():
    resposta = CLIENT.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Olá, mundo!"}


# Teste GET /tarefas/{id} com tarefa inexistente
def test_visualizar_tarefa_inexistente():
    limpar_tarefas()

    resposta = CLIENT.get("/tarefas/999")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# Teste PUT /tarefas/{id} com tarefa inexistente
def test_concluir_tarefa_inexistente():
    limpar_tarefas()

    resposta = CLIENT.put("/tarefas/999")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# Teste PUT /tarefas/{id} com tarefa já concluída
def test_concluir_tarefa_ja_concluida():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Estudar Python",
        "descricao": "Finalizar atividade"
    })

    # Marca a tarefa como concluída antes da requisição
    TAREFAS[0]["concluida"] = True

    resposta = CLIENT.put("/tarefas/0")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa não existe"}
    assert TAREFAS[0]["concluida"] == True


# Teste DELETE /tarefas/{id} com tarefa inexistente
def test_apagar_tarefa_inexistente():
    limpar_tarefas()

    resposta = CLIENT.delete("/tarefas/999")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

# Teste DELETE /tarefas/{id} excluindo a segunda tarefa
def test_apagar_segunda_tarefa():
    limpar_tarefas()

    CLIENT.post("/tarefas", params={
        "titulo": "Primeira tarefa",
        "descricao": "Não será excluída"
    })

    CLIENT.post("/tarefas", params={
        "titulo": "Segunda tarefa",
        "descricao": "Será excluída"
    })

    resposta = CLIENT.delete("/tarefas/1")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa apagada"}
    assert len(TAREFAS) == 1
    assert TAREFAS[0]["titulo"] == "Primeira tarefa"
