import sqlite3
from decouple import Config, RepositoryEnv
from langchain_core.tools import tool
from datetime import datetime

# Appoint to enviroment variables
config = Config(RepositoryEnv("/home/nophaieviscente/my-projects/debt-chatbot/.env"))
DATABASE = config("DATABASE")


@tool
def verify_debt(cpf: str, date_birth: str) -> list[dict]:
    "Tool to get information from user."
    date = datetime.strptime(date_birth, "%d/%m/%Y")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT 
        cs.cpf_cnpj,
        cs.nome,
        cs.data_nascimento,
        cs.data_origem,
        cs.valor_vencido,
        cs.valor_multa,
        cs.valor_juros,
        cs.produto
    FROM 
        customers as cs
    WHERE 
        cs.cpf_cnpj = ? AND cs.data_nascimento = ?
    """
    cursor.execute(query, (cpf, date))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def verify_plots(cpf: str, date_birth: str) -> list[dict]:
    "Tool to get information from plots debt."
    date = datetime.strptime(date_birth, "%d/%m/%Y")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT 
        cs.cpf_cnpj,
        cs.nome,
        cs.data_nascimento,
        po.valor_entrada,
        po.valor_parcela,
        po.valor_desconto,
        po.valor_negociado,
        po.quantidade_parcelas,
        po.data_primeiro_boleto
    FROM 
        customers as cs
        JOIN payment_options as po
        ON po.cpf_cnpj = cs.cpf_cnpj
    WHERE 
        cs.cpf_cnpj = ? AND cs.data_nascimento = ?
    """
    cursor.execute(query, (cpf, date))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def verify_cpf(cpf: str) -> list[dict]:
    "Tool to verify cpf into database."
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = """
    SELECT
        *
    FROM
        customers
    WHERE
        customers.cpf_cnpj = ?
    """
    cursor.execute(query, (cpf,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    if len(results) == 0:
        return False
    return True


@tool
def verify_date_birth(cpf: str, date_birth: str) -> list[dict]:
    "Tool to verify date of birth"
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    date = datetime.strptime(date_birth, "%d/%m/%Y")
    print(date)
    query = """
    SELECT 
        *
    FROM 
        customers
    WHERE 
        customers.cpf_cnpj = ? AND customers.data_nascimento = ?
    """
    cursor.execute(
        query,
        (cpf, date),
    )
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    if len(results) == 0:
        return False
    return True
