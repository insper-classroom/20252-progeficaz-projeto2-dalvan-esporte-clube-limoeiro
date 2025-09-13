import sqlite3

def connect_db():
    return sqlite3.connect('imoveis.sql')

def row_to_imovel(row):
    return {
        "id": row[0],
        "logradouro": row[1],
        "tipo_logradouro": row[2],
        "bairro": row[3],
        "cidade": row[4],
        "cep": row[5],
        "tipo": row[6],
        "valor": row[7],
        "data_aquisicao": row[8]
    }