from datetime import date

def classificar_alerta_validade(data_validade: date, data_referencia: date | None = None) -> str:
    hoje = data_referencia or date.today()
    dias_restantes = (data_validade - hoje).days
    if dias_restantes <= 7:
        return "URGENTE"
    if dias_restantes <= 30:
        return "ALERTA"
    return "REGULAR"

def validar_elegibilidade_entrega(familia_ativa: bool, ja_recebeu_no_mes: bool) -> tuple[bool, str]:
    if not familia_ativa:
        return False, "Cadastro inativo. Encaminhar para atualização cadastral."
    if ja_recebeu_no_mes:
        return False, "Bloqueado: família já retirou a cesta básica neste mês."
    return True, "Apta para retirada da cesta básica."
