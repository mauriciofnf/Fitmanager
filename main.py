from fastapi import FastAPI, HTTPException
from psycopg2 import errors

from .database import get_connection
from .models import (
    AlunoCreate,
    AlunoUpdate,
    PagamentoCreate,
    PagamentoUpdate,
)

app = FastAPI(title="API - Sistema de Academia (Entrega 4)")
@app.post("/alunos", status_code=201)
def criar_aluno(aluno: AlunoCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Aluno (id_aluno, id_personal, nome, data_nascimento, peso, altura, telefone)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (aluno.id_aluno, aluno.id_personal, aluno.nome, aluno.data_nascimento,
                 aluno.peso, aluno.altura, aluno.telefone),
            )
        conn.commit()
        return {"mensagem": "Aluno criado com sucesso", "id_aluno": aluno.id_aluno}
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="id_aluno já existe")
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


@app.get("/alunos")
def listar_alunos():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Aluno ORDER BY id_aluno")
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/alunos/{id_aluno}")
def buscar_aluno(id_aluno: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Aluno WHERE id_aluno = %s", (id_aluno,))
            aluno = cur.fetchone()
            if not aluno:
                raise HTTPException(status_code=404, detail="Aluno não encontrado")
            return aluno
    finally:
        conn.close()


@app.put("/alunos/{id_aluno}")
def atualizar_aluno(id_aluno: int, aluno: AlunoUpdate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Aluno
                SET id_personal = %s, nome = %s, data_nascimento = %s,
                    peso = %s, altura = %s, telefone = %s
                WHERE id_aluno = %s
                """,
                (aluno.id_personal, aluno.nome, aluno.data_nascimento,
                 aluno.peso, aluno.altura, aluno.telefone, id_aluno),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Aluno não encontrado")
        conn.commit()
        return {"mensagem": "Aluno atualizado com sucesso"}
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


@app.delete("/alunos/{id_aluno}")
def remover_aluno(id_aluno: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Aluno WHERE id_aluno = %s", (id_aluno,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Aluno não encontrado")
        conn.commit()
        return {"mensagem": "Aluno removido com sucesso"}
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


# ============================================================
# PAGAMENTO - CRUD completo
# ============================================================

@app.post("/pagamentos", status_code=201)
def criar_pagamento(pagamento: PagamentoCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Pagamento (id_pagamento, id_aluno, data_pagamento, status, valor, metodo)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (pagamento.id_pagamento, pagamento.id_aluno, pagamento.data_pagamento,
                 pagamento.status, pagamento.valor, pagamento.metodo),
            )
        conn.commit()
        return {"mensagem": "Pagamento registrado com sucesso"}
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="id_pagamento já existe")
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


@app.get("/pagamentos")
def listar_pagamentos():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Pagamento ORDER BY id_pagamento")
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/pagamentos/{id_pagamento}")
def buscar_pagamento(id_pagamento: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
            pagamento = cur.fetchone()
            if not pagamento:
                raise HTTPException(status_code=404, detail="Pagamento não encontrado")
            return pagamento
    finally:
        conn.close()


@app.put("/pagamentos/{id_pagamento}")
def atualizar_pagamento(id_pagamento: int, pagamento: PagamentoUpdate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE Pagamento
                SET id_aluno = %s, data_pagamento = %s, status = %s, valor = %s, metodo = %s
                WHERE id_pagamento = %s
                """,
                (pagamento.id_aluno, pagamento.data_pagamento, pagamento.status,
                 pagamento.valor, pagamento.metodo, id_pagamento),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        conn.commit()
        return {"mensagem": "Pagamento atualizado com sucesso"}
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


@app.delete("/pagamentos/{id_pagamento}")
def remover_pagamento(id_pagamento: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        conn.commit()
        return {"mensagem": "Pagamento removido com sucesso"}
    except errors.InsufficientPrivilege:
        conn.rollback()
        raise HTTPException(status_code=403, detail="Usuário sem permissão de escrita (somente leitura)")
    finally:
        conn.close()


# ============================================================
# RELATÓRIOS - leitura das visões (Entrega 4)
# ============================================================

@app.get("/relatorios/financeiro-aluno")
def relatorio_financeiro_aluno():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vw_financeiro_aluno")
            return cur.fetchall()
    finally:
        conn.close()


@app.get("/relatorios/evolucao-desempenho")
def relatorio_evolucao_desempenho():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vw_evolucao_desempenho")
            return cur.fetchall()
    finally:
        conn.close()