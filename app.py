
from fastapi import FastAPI
from datetime import datetime
import httpx

app = FastAPI(title="ServicoTarefa")

TAREFAS = []

URL_NOTIFICACAO = "http://127.0.0.1:8002/notificacoes"


async def enviar_notificacao(mensagem: str):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                URL_NOTIFICACAO,
                json={"mensagem": mensagem},
                timeout=2.0
            )
    except httpx.RequestError:
        print("Servico de notificacao indisponivel.")


def criar_tarefa(titulo: str, descricao: str):
    return {
        "id": max(
            (tarefa["id"] for tarefa in TAREFAS),
            default=0
        ) + 1,
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False,
        "criado_em": datetime.now().isoformat()
    }


@app.get("/")
async def index():
    return {"mensagem": "Servico de tarefas funcionando!"}


@app.get("/tarefas")
async def listar_tarefas():
    return [
        {"id": tarefa["id"], "titulo": tarefa["titulo"]}
        for tarefa in TAREFAS
    ]


@app.get("/tarefas/{id_tarefa}")
async def buscar_tarefa(id_tarefa: int):
    for tarefa in TAREFAS:
        if tarefa["id"] == id_tarefa:
            return tarefa

    return {"mensagem": "A tarefa nao existe."}


@app.post("/tarefas")
async def adicionar_tarefa(titulo: str, descricao: str):
    tarefa = criar_tarefa(titulo, descricao)
    TAREFAS.append(tarefa)

    await enviar_notificacao(
        f"Tarefa criada: {tarefa['titulo']}"
    )

    return {
        "mensagem": "Tarefa criada com sucesso!",
        "tarefa": tarefa
    }


@app.put("/tarefas/{id}")
async def concluir_tarefa(id: int):
    for tarefa in TAREFAS:
        if tarefa["id"] == id:
            tarefa["concluida"] = True
            tarefa["concluida_em"] = datetime.now().isoformat()

            await enviar_notificacao(
                f"Tarefa concluida: {tarefa['titulo']}"
            )

            return {
                "mensagem": "Tarefa concluida com sucesso!",
                "tarefa": tarefa
            }

    return {"mensagem": "A tarefa nao existe."}


@app.delete("/tarefas/{id}")
async def apagar_tarefa(id: int):
    for tarefa in TAREFAS:
        if tarefa["id"] == id:
            TAREFAS.remove(tarefa)

            await enviar_notificacao(
                f"Tarefa excluida: {tarefa['titulo']}"
            )

            return {"mensagem": "Tarefa excluida com sucesso!"}

    return {"mensagem": "A tarefa nao existe."}
