import utils
def listar_imoveis():
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    conn.close()
    return imoveis

def get_imovel_por_id(id):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id =?", (id,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return None
    return utils.row_to_imovel(rows[0])

def cria_imovel_db(dados):
    conn = utils.connect_db()
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
    conn.commit()
    conn.close()
    return True

def get_imoveis_por_tipo(tipo):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo =?", (tipo,))
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    conn.close()
    return imoveis

def get_imoveis_por_cidade(cidade):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade =?", (cidade,))
    rows = cursor.fetchall()
    imoveis = [utils.row_to_imovel(row) for row in rows]
    conn.close()
    return imoveis

def atualiza_imovel(id, data):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=?", (id,))
    rows = cursor.fetchall()
    if not rows:
        conn.close()
        return None
    cursor.execute("""
        UPDATE imoveis
        SET logradouro=?, tipo_logradouro=?, bairro=?, cidade=?, cep=?, tipo=?, valor=?, data_aquisicao=?
        WHERE id=?
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
    cursor.execute("SELECT * FROM imoveis WHERE id=?", (id,))
    row = cursor.fetchone()
    imovel = utils.row_to_imovel(row)
    conn.close()
    return imovel

def delete_imovel(id):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id=?", (id,))
    rows = cursor.fetchall()
    if not rows:
        conn.close()
        return False
    cursor.execute("DELETE FROM imoveis WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return True