"""
Conexão com o banco PostgreSQL.

Ajuste as variáveis abaixo (ou defina variáveis de ambiente com os
mesmos nomes) com os dados reais do seu banco no pgAdmin/PostgreSQL.

Para testar com o usuário SOMENTE LEITURA, basta trocar DB_USER e
DB_PASSWORD para 'readonly_user' e rodar a aplicação de novo: as
operações de POST/PUT/DELETE devem passar a falhar com erro de
permissão vindo do próprio PostgreSQL.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "bancotrabalhofinal"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
}


def get_connection():
    """Abre uma nova conexão com o banco. Use sempre dentro de um try/finally."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)