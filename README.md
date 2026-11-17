# MVP — Gestão de Doações e Estoque (Associação Comunitária Mãos Unidas da RMC)

Sistema Web Responsivo / PWA desenvolvido para modernizar o controle de estoque, monitoramento preventivo de datas de validade e registro presencial de entrega de cestas básicas para 120 famílias vulneráveis atendidas pela **Associação Comunitária Mãos Unidas da RMC** (Região Metropolitana de Curitiba/PR).

## Alinhamento Social (ODS)
* **ODS 2 (Fome Zero e Agricultura Sustentável) — Meta 2.1:** Redução do desperdício de alimentos perecíveis através de alertas visuais e textuais de vencimento, garantindo o aproveitamento integral dos donativos.

## Tecnologias e Arquitetura
* **Arquitetura:** Em Camadas (Apresentação, Regras de Negócio e Banco de Dados).
* **Back-end:** Python com FastAPI e SQLAlchemy.
* **Banco de Dados:** SQLite (`Familia`, `ItemEstoque`, `Atendimento`).
* **Front-end:** HTML5, CSS3 e Bootstrap 5.3 (alto contraste e alertas com cor, ícone e texto).
* **Qualidade:** Versionamento no GitHub, Pull Requests, testes automatizados com `pytest` e GitHub Actions (CI).

## Funcionalidades Principais
* **Consulta por CPF:** Verificação rápida se a família está apta a receber a cesta básica.
* **Controle de Estoque e Validade:** Classificação automática dos alimentos (`URGENTE`, `ALERTA`, `REGULAR`).
* **Registro de Entrega:** Baixa da cesta básica com bloqueio automático de entrega duplicada no mesmo mês.
