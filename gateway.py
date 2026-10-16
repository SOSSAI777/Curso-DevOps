
from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
import httpx

app = FastAPI(title="Gateway")

URL_TAREFAS = "http://127.0.0.1:8001"
URL_NOTIFICACOES = "http://127.0.0.1:8002"


@app.get("/")
async def index():
    return {"mensagem": "Gateway funcionando!"}


async def encaminhar(request: Request, destino: str):
    url = f"{destino}{request.url.path}"

    try:
        async with httpx.AsyncClient() as client:
            resposta = await client.request(
                method=request.method,
                url=url,
                params=request.query_params,
                content=await request.body(),
                headers={
                    "content-type": request.headers.get(
                        "content-type", "application/json"
                    )
                },
                timeout=5.0
            )

        return Response(
            content=resposta.content,
            status_code=resposta.status_code,
            headers={
                "content-type": resposta.headers.get(
                    "content-type", "application/json"
                )
            }
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={
                "mensagem": "O servico solicitado esta indisponivel."
            }
        )


# Rotas de tarefas

@app.get("/tarefas")
async def gateway_listar_tarefas(request: Request):
    return await encaminhar(request, URL_TAREFAS)


@app.post("/tarefas")
async def gateway_criar_tarefa(
    request: Request,
    titulo: str,
    descricao: str
):
    return await encaminhar(request, URL_TAREFAS)


@app.get("/tarefas/{id_tarefa}")
async def gateway_buscar_tarefa(
    request: Request,
    id_tarefa: int
):
    return await encaminhar(request, URL_TAREFAS)


@app.put("/tarefas/{id}")
async def gateway_concluir_tarefa(
    request: Request,
    id: int
):
    return await encaminhar(request, URL_TAREFAS)


@app.delete("/tarefas/{id}")
async def gateway_apagar_tarefa(
    request: Request,
    id: int
):
    return await encaminhar(request, URL_TAREFAS)


# Rotas de notificações

@app.get("/notificacoes")
async def gateway_listar_notificacoes(request: Request):
    return await encaminhar(request, URL_NOTIFICACOES)


@app.post("/notificacoes")
async def gateway_criar_notificacao(request: Request):
    return await encaminhar(request, URL_NOTIFICACOES)
