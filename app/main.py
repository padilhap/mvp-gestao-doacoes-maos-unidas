from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.services import classificar_alerta_validade, validar_elegibilidade_entrega

app = FastAPI(title="MVP Gestão de Doações — Associação Mãos Unidas da RMC")

class ConsultaCPFRequest(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")

class ItemValidadeRequest(BaseModel):
    nome: str
    data_validade: date

@app.get("/")
def menu_inicial():
    return {
        "associacao": "Associação Comunitária Mãos Unidas da RMC",
        "status": "online",
        "modulos": ["Atendimento por CPF", "Controle de Estoque", "Alertas de Validade"]
    }

@app.post("/api/alertas/classificar")
def verificar_validade(item: ItemValidadeRequest):
    status = classificar_alerta_validade(item.data_validade)
    return {"item": item.nome, "status": status}

@app.post("/api/atendimentos/validar")
def checar_atendimento(dados: ConsultaCPFRequest, ja_recebeu: bool = False):
    if dados.cpf == "00000000000":
        raise HTTPException(status_code=404, detail="CPF não encontrado no cadastro.")
    apto, mensagem = validar_elegibilidade_entrega(familia_ativa=True, ja_recebeu_no_mes=ja_recebeu)
    return {"cpf": dados.cpf, "apto": apto, "mensagem": mensagem}
