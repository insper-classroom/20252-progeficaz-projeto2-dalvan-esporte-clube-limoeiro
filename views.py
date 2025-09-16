import utils
from mysql.connector import Error

def listar_imoveis(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    cursor.close()
    return imoveis

def get_imovel_por_id(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id =%s", (id,))
    row = cursor.fetchone()
    cursor.close()
    if not row:
        return None
    return utils.row_to_imovel(row)

def cria_imovel_db(conn, dados):
    required_params = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor', 'data_aquisicao']
    for param in required_params:
        if param not in dados:
            return [param]
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            dados["logradouro"],
            dados["tipo_logradouro"],
            dados["bairro"],
            dados["cidade"],
            dados["cep"],
            dados["tipo"],
            dados["valor"],
            dados["data_aquisicao"]
        )
    )
    
    novo_id = cursor.lastrowid
    
    conn.commit()
    cursor.close()
    
    dados['id'] = novo_id
    return dados

def get_imoveis_por_tipo(conn, tipo):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo =%s", (tipo,))
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    cursor.close()
    return imoveis

def get_imoveis_por_cidade(conn, cidade):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade =%s", (cidade,))
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    cursor.close()
    return imoveis

def atualiza_imovel(conn, id, data):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=%s", (id,))
    rows = cursor.fetchall()
    if not rows:
        cursor.close()
        return None
    
    required_params = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor', 'data_aquisicao']
    for param in required_params:
        if param not in data:
            return [param]
   
    cursor.execute("""
        UPDATE imoveis
        SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, cep=%s, tipo=%s, valor=%s, data_aquisicao=%s
        WHERE id=%s
    """, (
        data["logradouro"],
        data["tipo_logradouro"],
        data["bairro"],
        data["cidade"],
        data["cep"],
        data["tipo"],
        data["valor"],
        data["data_aquisicao"],
        id
    ))
    conn.commit()
    cursor.execute("SELECT * FROM imoveis WHERE id=%s", (id,))
    row = cursor.fetchone()
    imovel = utils.row_to_imovel(row)
    cursor.close()
    return imovel

def delete_imovel(conn, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=%s", (id,))
    rows = cursor.fetchall()
    if not rows:
        cursor.close()
        return False
    cursor.execute("DELETE FROM imoveis WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    return True