# servidor.py
from flask import Flask, jsonify, request
import utils

app = Flask(__name__)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis")
    rows = cursor.fetchall()

    # transformar tuplas do banco em dicionários
    imoveis = []
    for row in rows:      #Varre uma lista de tuplas.
        imoveis.append({
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": row[7],
            "data_aquisicao": row[8]
        })

    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/<id>", methods=["GET"])
def get_imovel_por_id(id):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE id =?",(id,))
    rows = cursor.fetchall()
    if not rows:
        return jsonify({"imovel": None}), 404
    row = rows[0]
    imovel = {
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
    return jsonify({"imovel": imovel})

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

@app.route("/imoveis", methods=["POST"])
def cria_imovel():
    dados = request.get_json()
    try:
        cria_imovel_db(dados)
        return jsonify({"mensagem": "Imóvel criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def get_imoveis_por_tipo(tipo):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE tipo =?", (tipo,))
    rows = cursor.fetchall()
    imoveis = []
    for row in rows:
        imoveis.append({
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": row[7],
            "data_aquisicao": row[8]
        })
    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def get_imoveis_por_cidade(cidade):
    conn = utils.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imoveis WHERE cidade =?", (cidade,))
    rows = cursor.fetchall()
    imoveis = []
    for row in rows:
        imoveis.append({
            "id": row[0],
            "logradouro": row[1],
            "tipo_logradouro": row[2],
            "bairro": row[3],
            "cidade": row[4],
            "cep": row[5],
            "tipo": row[6],
            "valor": row[7],
            "data_aquisicao": row[8]
        })
    return jsonify({"imoveis": imoveis})
