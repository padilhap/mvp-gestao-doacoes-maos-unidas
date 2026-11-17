from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Familia(Base):
    __tablename__ = "familias"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), unique=True, index=True, nullable=False)
    responsavel = Column(String(120), nullable=False)
    ativa = Column(Boolean, default=True)

class ItemEstoque(Base):
    __tablename__ = "itens_estoque"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_validade = Column(Date, nullable=False)

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    familia_id = Column(Integer, ForeignKey("familias.id"), nullable=False)
    mes_referencia = Column(String(7), nullable=False)  # Formato YYYY-MM
    data_entrega = Column(DateTime, default=datetime.utcnow)
