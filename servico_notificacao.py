
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="ServicoNotificacao")

NOTIFICACOES = []


@app.get("/")
async def index():
    return {"mensagem": "Servico de notificacao funcionando!"}


@app.post("/notificacoes")
async def receber_notificacao(dados: dict):
    notificacao = {
        "mensagem": dados["mensagem"],
        "recebida_em": datetime.now().isoformat()
    }

    NOTIFICACOES.append(notificacao)

    print(f"NOTIFICACAO: {notificacao['mensagem']}")

    return {
        "mensagem": "Notificacao recebida com sucesso!",
        "notificacao": notificacao
    }


@app.get("/notificacoes")
async def listar_notificacoes():
    return NOTIFICACOES
