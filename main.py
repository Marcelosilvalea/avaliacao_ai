from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

from gemini_service import GeminiService
from models import Interacao, HistoricoInteracoes

app = FastAPI(
    title="Quiz IA",
    description="Aplicação FastAPI que gera quizzes usando IA",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

gemini = GeminiService()
historico = HistoricoInteracoes(limite=50)


# 🔹 Página inicial
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 🔹 Página com formulário do quiz
@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


# 🔹 Processa quiz
@app.post("/gerar-quiz", response_class=HTMLResponse)
async def gerar_quiz(
    request: Request,
    tema: Annotated[str, Form()],
    quantidade: Annotated[int, Form()] = 5
):
    try:
        prompt = f"""
        Gere um quiz de {quantidade} perguntas sobre o tema: {tema}.
        O formato DEVE ser exatamente este:

        PERGUNTA 1: texto
        A) alternativa
        B) alternativa
        C) alternativa
        D) alternativa
        RESPOSTA: letra correta

        Repita o formato para todas.

        IMPORTANTE:
        - NUNCA quebre o formato
        - Sempre coloque a resposta em "RESPOSTA:"
        - Não escreva nada além do quiz
        """

        resultado = gemini.gerar_conteudo(prompt)

        interacao = Interacao(
            usuario_input=f"Quiz sobre {tema}",
            ia_resposta=resultado,
            categoria="quiz"
        )
        historico.adicionar(interacao)

        return templates.TemplateResponse(
            "resultado.html",
            {
                "request": request,
                "titulo": f"Quiz sobre {tema}",
                "resultado": resultado
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "resultado.html",
            {"request": request, "erro": str(e)}
        )


# 🔹 Página de histórico
@app.get("/historico", response_class=HTMLResponse)
async def ver_historico(request: Request):
    return templates.TemplateResponse(
        "historico.html",
        {
            "request": request,
            "interacoes": historico.obter_todas(),
            "total": historico.total()
        }
    )


@app.post("/limpar-historico")
async def limpar_historico():
    historico.limpar()
    return {"mensagem": "Histórico apagado!"}
