from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models import get_db, init_db, Familia, Entrega
from app.services import sanitizar_cpf, classificar_prioridade, verificar_elegibilidade_entrega

app = FastAPI(title="Gestão de Doações - Associação Comunitária Mãos Unidas da RMC")

@app.on_event("startup")
def on_startup():
    init_db()

class FamiliaCreate(BaseModel):
    nome_responsavel: str
    cpf: str
    renda_per_capita: float

class EntregaCreate(BaseModel):
    cpf: str
    itens: str = "Cesta Básica Padrão"

@app.get("/", response_class=HTMLResponse)
def interface_principal():
    return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mãos Unidas da RMC - Gestão de Doações (ODS 2)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-size: 16px; transition: all 0.2s; }
        body.fonte-grande { font-size: 20px; }
        body.alto-contraste { background-color: #000000 !important; color: #FFFF00 !important; }
        body.alto-contraste .card, body.alto-contraste .navbar, body.alto-contraste .table {
            background-color: #111111 !important; color: #FFFF00 !important; border: 2px solid #FFFF00 !important;
        }
        body.alto-contraste .form-control { background-color: #000 !important; color: #FFF !important; border: 2px solid #FFFF00 !important; }
        body.alto-contraste .btn-primary, body.alto-contraste .btn-success {
            background-color: #FFFF00 !important; color: #000000 !important; font-weight: bold; border: none;
        }
    </style>
</head>
<body class="bg-light">
<nav class="navbar navbar-dark bg-success px-4 py-3 mb-4" role="navigation" aria-label="Barra superior e acessibilidade">
    <span class="navbar-brand fw-bold">Associação Comunitária Mãos Unidas da RMC • ODS 2</span>
    <div class="d-flex gap-2">
        <button id="btn-contraste" onclick="toggleContraste()" class="btn btn-warning btn-sm fw-bold" aria-pressed="false">Alto Contraste</button>
        <button id="btn-fonte" onclick="toggleFonte()" class="btn btn-light btn-sm fw-bold" aria-pressed="false">A+ Aumentar Fonte</button>
    </div>
</nav>

<main class="container">
    <div id="alerta-sistema" class="alert d-none" role="alert"></div>

    <div class="row g-4">
        <div class="col-md-5">
            <div class="card shadow-sm mb-4">
                <div class="card-header fw-bold bg-white">1. Cadastrar Família Beneficiária</div>
                <div class="card-body">
                    <div class="mb-2">
                        <label class="form-label" for="nome">Nome do Responsável</label>
                        <input id="nome" class="form-control" value="Maria Aparecida da Silva">
                    </div>
                    <div class="mb-2">
                        <label class="form-label" for="cpf">CPF</label>
                        <input id="cpf" class="form-control" value="123.456.789-00">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="renda">Renda Per Capita (R$)</label>
                        <input id="renda" type="number" class="form-control" value="180">
                    </div>
                    <button onclick="cadastrarFamilia()" class="btn btn-success w-100">Salvar Cadastro e Calcular Prioridade</button>
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-header fw-bold bg-white">2. Registrar Entrega de Cesta Básica</div>
                <div class="card-body">
                    <div class="mb-2">
                        <label class="form-label" for="cpf_entrega">CPF do Beneficiário</label>
                        <input id="cpf_entrega" class="form-control" value="123.456.789-00">
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="itens">Kit / Itens Entregues</label>
                        <input id="itens" class="form-control" value="Cesta Básica Completa + Hortifrúti">
                    </div>
                    <button onclick="registrarEntrega()" class="btn btn-primary w-100">Confirmar Entrega (Regra 30 dias)</button>
                </div>
            </div>
        </div>

        <div class="col-md-7">
            <div class="card shadow-sm">
                <div class="card-header fw-bold bg-white">Painel de Prioridade de Entrega e Famílias Atendidas</div>
                <div class="card-body">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Responsável</th>
                                <th>CPF</th>
                                <th>Renda</th>
                                <th>Prioridade</th>
                            </tr>
                        </thead>
                        <tbody id="tabela-familias">
                            <tr>
                                <td>João Carlos Pereira</td>
                                <td>98765432100</td>
                                <td>R$ 150,00</td>
                                <td><span class="badge bg-danger">Alerta Urgente</span></td>
                            </tr>
                            <tr>
                                <td>Ana Beatriz Souza</td>
                                <td>45678912300</td>
                                <td>R$ 420,00</td>
                                <td><span class="badge bg-secondary">Regular</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</main>

<script>
function toggleContraste() {
    document.body.classList.toggle('alto-contraste');
}
function toggleFonte() {
    document.body.classList.toggle('fonte-grande');
}
function mostrarAlerta(msg, tipo) {
    const el = document.getElementById('alerta-sistema');
    el.className = 'alert alert-' + tipo;
    el.textContent = msg;
}
async function cadastrarFamilia() {
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value;
    const renda = parseFloat(document.getElementById('renda').value);
    const res = await fetch('/familias', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nome_responsavel: nome, cpf: cpf, renda_per_capita: renda})
    });
    const data = await res.json();
    if (res.ok) {
        const badge = data.prioridade === 'Alerta Urgente' ? 'bg-danger' : 'bg-secondary';
        document.getElementById('tabela-familias').insertAdjacentHTML('afterbegin',
            `<tr><td>${nome}</td><td>${data.cpf}</td><td>R$ ${renda.toFixed(2)}</td><td><span class="badge ${badge}">${data.prioridade}</span></td></tr>`
        );
        mostrarAlerta('Família cadastrada com sucesso! Classificação: ' + data.prioridade, 'success');
    } else {
        mostrarAlerta(data.detail || 'Erro ao cadastrar', 'danger');
    }
}
async function registrarEntrega() {
    const cpf = document.getElementById('cpf_entrega').value;
    const itens = document.getElementById('itens').value;
    const res = await fetch('/entregas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cpf: cpf, itens: itens})
    });
    const data = await res.json();
    if (res.ok) {
        mostrarAlerta('Entrega registrada com sucesso para o CPF ' + cpf + '!', 'success');
    } else {
        mostrarAlerta('Bloqueio de Segurança: ' + (data.detail || 'Entrega já realizada neste mês.'), 'warning');
    }
}
</script>
</body>
</html>
"""

@app.post("/familias")
def cadastrar_familia(dados: FamiliaCreate, db: Session = Depends(get_db)):
    cpf_limpo = sanitizar_cpf(dados.cpf)
    if len(cpf_limpo) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    prioridade = classificar_prioridade(dados.renda_per_capita, None)
    nova = Familia(nome_responsavel=dados.nome_responsavel, cpf=cpf_limpo, renda_per_capita=dados.renda_per_capita)
    db.add(nova)
    db.commit()
    return {"cpf": cpf_limpo, "prioridade": prioridade}

@app.post("/entregas")
def registrar_entrega(dados: EntregaCreate, db: Session = Depends(get_db)):
    cpf_limpo = sanitizar_cpf(dados.cpf)
    familia = db.query(Familia).filter(Familia.cpf == cpf_limpo).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Família não encontrada")
    ultima = db.query(Entrega).filter(Entrega.familia_id == familia.id).order_by(Entrega.data_entrega.desc()).first()
    data_ultima = ultima.data_entrega if ultima else None
    if not verificar_elegibilidade_entrega(data_ultima):
        raise HTTPException(status_code=400, detail="Bloqueado: família já recebeu cesta básica nos últimos 30 dias.")
    entrega = Entrega(familia_id=familia.id, itens=dados.itens)
    db.add(entrega)
    db.commit()
    return {"status": "Entrega registada com sucesso"}
