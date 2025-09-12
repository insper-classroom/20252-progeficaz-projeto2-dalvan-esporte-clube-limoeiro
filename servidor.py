# servidor.py
from flask import Flask, jsonify
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
