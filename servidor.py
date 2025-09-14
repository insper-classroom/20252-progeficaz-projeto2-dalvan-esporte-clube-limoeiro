from flask import Flask, jsonify, request
import views
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv('.cred')

config = {
    'host': os.getenv('DB_HOST', 'localhost'),  
    'user': os.getenv('DB_USER'),  
    'password': os.getenv('DB_PASSWORD'),  
    'database': os.getenv('DB_NAME', 'db_escola'),  
    'port': int(os.getenv('DB_PORT', 3306)),  
    'ssl_ca': os.getenv('SSL_CA_PATH')  
}

def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro: {err}")
        return None

app = Flask(__name__)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        imoveis = views.listar_imoveis(conn)
        return jsonify({"imoveis": imoveis})
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route("/imoveis/<int:id>", methods=["GET"])
def get_imovel_por_id(id):
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        imovel = views.get_imovel_por_id(conn, id)
        if imovel is None:
            return jsonify({"imovel": None}), 404
        return jsonify({"imovel": imovel})
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
        
@app.route("/imoveis", methods=["POST"])
def cria_imovel():
    dados = request.get_json()
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        views.cria_imovel_db(conn, dados)
        return jsonify({"mensagem": "Imóvel criado com sucesso"}), 201
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def get_imoveis_por_tipo(tipo):
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        imoveis = views.get_imoveis_por_tipo(conn, tipo)
        return jsonify({"imoveis": imoveis})
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def get_imoveis_por_cidade(cidade):
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        imoveis = views.get_imoveis_por_cidade(conn, cidade)
        return jsonify({"imoveis": imoveis})
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()


@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualiza_imoveis(id):
    data = request.get_json()
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        imovel = views.atualiza_imovel(conn, id, data)
        if imovel is None:
            return jsonify({"imovel": None}), 404
        return jsonify({"imovel": imovel})
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route("/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    conn = None
    try:
        conn = connect_db()
        if not conn:
            return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
        sucesso = views.delete_imovel(conn, id)
        if not sucesso:
            return jsonify({"imovel": None}), 404
        return jsonify({"mensagem": "Imóvel removido com sucesso."}), 200
    except Error as e:
        return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
    finally:
        if conn and conn.is_connected():
            conn.close()
