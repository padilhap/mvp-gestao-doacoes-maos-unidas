from datetime import date, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.services import classificar_alerta_validade, validar_elegibilidade_entrega

client = TestClient(app)

def test_classificacao_alerta_urgente():
    hoje = date(2026, 11, 16)
    assert classificar_alerta_validade(hoje + timedelta(days=5), hoje) == "URGENTE"

def test_classificacao_alerta_regular():
    hoje = date(2026, 11, 16)
    assert classificar_alerta_validade(hoje + timedelta(days=45), hoje) == "REGULAR"

def test_bloqueio_entrega_duplicada_mes():
    apto, msg = validar_elegibilidade_entrega(familia_ativa=True, ja_recebeu_no_mes=True)
    assert apto is False
    assert "Bloqueado" in msg

def test_endpoint_validacao_cpf():
    response = client.post("/api/atendimentos/validar", json={"cpf": "12345678901"})
    assert response.status_code == 200
    assert response.json()["apto"] is True
