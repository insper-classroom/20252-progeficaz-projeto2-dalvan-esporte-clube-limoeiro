from flask import Flask, jsonify, request
import views

app = Flask(__name__)

@app.route("/imoveis", methods=["GET"])
def listar_imoveis():
    imoveis = views.listar_imoveis()
    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/<id>", methods=["GET"])
def get_imovel_por_id(id):
    imovel = views.get_imovel_por_id(id)
    if imovel is None:
        return jsonify({"imovel": None}), 404
    return jsonify({"imovel": imovel})

@app.route("/imoveis", methods=["POST"])
def cria_imovel():
    dados = request.get_json()
    try:
        views.cria_imovel_db(dados)
        return jsonify({"mensagem": "Imóvel criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def get_imoveis_por_tipo(tipo):
    imoveis = views.get_imoveis_por_tipo(tipo)
    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/cidade/<cidade>", methods=["GET"])
def get_imoveis_por_cidade(cidade):
    imoveis = views.get_imoveis_por_cidade(cidade)
    return jsonify({"imoveis": imoveis})

@app.route("/imoveis/<int:id>", methods=["PUT"])
def atualiza_imoveis(id):
    data = request.get_json()
    imovel = views.atualiza_imovel(id, data)
    if imovel is None:
        return jsonify({"imovel": None}), 404
    return jsonify({"imovel": imovel})

@app.route("/imoveis/<int:id>", methods=["DELETE"])
def delete_imovel(id):
    sucesso = views.delete_imovel(id)
    if not sucesso:
        return jsonify({"imovel": None}), 404
    return jsonify({"mensagem": "Imóvel removido com sucesso."}), 200
