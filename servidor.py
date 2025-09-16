from flask import Flask, jsonify, request, url_for, make_response
from functools import wraps
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

def db_connection_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        conn = None
        try:
            conn = connect_db()
            if not conn:
                return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500
            return f(conn, *args, **kwargs)
        except Error as e:
            return jsonify({"erro": f"Erro no banco de dados: {e}"}), 500
        finally:
            if conn and conn.is_connected():
                conn.close()
    return decorated_function

@app.route("/imoveis", methods=["GET"])
@db_connection_handler
def listar_imoveis(conn):
    imoveis = views.listar_imoveis(conn)
    return jsonify(imoveis)
    

@app.route("/imoveis/<int:id>", methods=["GET"])
@db_connection_handler
def get_imovel_por_id(conn, id):
    imovel = views.get_imovel_por_id(conn, id)
    if imovel is None:
        return jsonify({"mensagem": "imóvel não encontrado"}), 404
    
    imovel['_links'] = {
        'self': {'href': url_for('get_imovel_por_id', id=id, _external=True)},
        'update': {'href': url_for('atualiza_imoveis', id=id, _external=True)},
        'delete': {'href': url_for('delete_imovel', id=id, _external=True)},
        'collection': {'href': url_for('listar_imoveis', _external=True)}
    }
    
    return jsonify(imovel)
        
@app.route("/imoveis", methods=["POST"])
@db_connection_handler
def cria_imovel(conn):
    dados = request.get_json()
    imovel_criado = views.cria_imovel_db(conn, dados)
    
    location_url = url_for('get_imovel_por_id', id=imovel_criado['id'], _external=True)

    imovel_criado['_links'] = {'self': {'href': location_url}}

    response = make_response(jsonify(imovel_criado), 201)
    response.headers['Location'] = location_url
    return response

@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
@db_connection_handler
def get_imoveis_por_tipo(conn, tipo):
    imoveis = views.get_imoveis_por_tipo(conn, tipo)
    return jsonify(imoveis)

@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
@db_connection_handler
def get_imoveis_por_cidade(conn, cidade):
    imoveis = views.get_imoveis_por_cidade(conn, cidade)
    return jsonify(imoveis)


@app.route("/imoveis/<int:id>", methods=["PUT"])
@db_connection_handler
def atualiza_imoveis(conn, id):
    data = request.get_json()
    imovel = views.atualiza_imovel(conn, id, data)
    if imovel is None:
        return jsonify({"mensagem": "imóvel não encontrado"}), 404
    return jsonify(imovel)

@app.route("/imoveis/<int:id>", methods=["DELETE"])
@db_connection_handler
def delete_imovel(conn, id):
    sucesso = views.delete_imovel(conn, id)
    if not sucesso:
        return jsonify({"mensagem": "imóvel não encontrado"}), 404
    return jsonify({"mensagem": "imóvel removido com sucesso."}), 200

if __name__ == '__main__':
    app.run(debug=True)