from datetime import date
from typing import Optional
from pydantic import BaseModel


# ---------- Aluno ----------

class AlunoBase(BaseModel):
    id_personal: Optional[int] = None
    nome: str
    data_nascimento: date
    peso: Optional[float] = None
    altura: Optional[float] = None
    telefone: Optional[int] = None


class AlunoCreate(AlunoBase):
    id_aluno: int


class AlunoUpdate(AlunoBase):
    pass


# ---------- Pagamento ----------

class PagamentoBase(BaseModel):
    id_aluno: int
    data_pagamento: date
    status: str
    valor: int
    metodo: str


class PagamentoCreate(PagamentoBase):
    id_pagamento: int


class PagamentoUpdate(PagamentoBase):
    pass