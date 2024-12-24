from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import unquote

# Configuração do MongoDB
cliente = MongoClient("mongodb://localhost:27017/")  # Conecta ao banco de dados MongoDB na porta padrão
banco_de_dados = cliente["meu_banco_de_dados"]  # Define o banco de dados utilizado

# Inicialização do Flask
app = Flask(__name__)  # Inicializa a aplicação Flask


def analisar_consulta(consulta_str):
    """
    Função para analisar e converter uma string de consulta para um formato de dicionário.
    :param consulta_str: String de consulta a ser analisada.
    :return: Dicionário correspondente à consulta ou {} em caso de erro.
    """
    try:
        return eval(unquote(consulta_str))  # Converte a string de consulta para dicionário
    except Exception:
        return {}


@app.route('/<colecao>', methods=['POST'])
def criar_entidade(colecao):
    """
    Rota para criar uma nova entidade no banco de dados MongoDB.
    :param colecao: Nome da coleção onde a entidade será criada.
    :return: JSON com o ID da entidade criada.
    """
    dados = request.json  # Obtém os dados enviados no corpo da requisição
    resultado = banco_de_dados[colecao].insert_one(dados)  # Insere os dados na coleção especificada
    return jsonify({"id": str(resultado.inserted_id)}), 201  # Retorna o ID da entidade criada


@app.route('/<colecao>', methods=['GET'])
def listar_entidades(colecao):
    """
    Rota para listar entidades de uma coleção.
    :param colecao: Nome da coleção.
    :return: Lista de entidades encontradas em formato JSON.
    """
    consulta = request.args.get("consulta", "{}")  # Obtém a consulta da URL (se presente)
    campos = request.args.get("campos")  # Obtém os campos para projeção (se presentes)

    consulta = analisar_consulta(consulta)  # Converte a consulta para um dicionário
    projeção = {campo: 1 for campo in campos.split(',')} if campos else None  # Define os campos para projeção

    entidades = list(banco_de_dados[colecao].find(consulta, projeção))  # Obtém as entidades conforme consulta e projeção
    for entidade in entidades:
        entidade["_id"] = str(entidade["_id"])  # Converte o campo _id para string
    return jsonify(entidades), 200  # Retorna as entidades em formato JSON


@app.route('/<colecao>/<entidade_id>', methods=['GET'])
def obter_entidade(colecao, entidade_id):
    """
    Rota para obter uma entidade específica pelo seu ID.
    :param colecao: Nome da coleção.
    :param entidade_id: ID da entidade.
    :return: A entidade em formato JSON ou mensagem de erro.
    """
    entidade = banco_de_dados[colecao].find_one({"_id": ObjectId(entidade_id)})  # Busca a entidade pelo ID
    if entidade:
        entidade["_id"] = str(entidade["_id"])  # Converte o campo _id para string
        return jsonify(entidade), 200  # Retorna a entidade encontrada
    return jsonify({"erro": "Entidade não encontrada"}), 404  # Retorna erro caso a entidade não seja encontrada


@app.route('/<colecao>/<entidade_id>', methods=['PUT'])
def atualizar_entidade(colecao, entidade_id):
    """
    Rota para atualizar uma entidade existente.
    :param colecao: Nome da coleção.
    :param entidade_id: ID da entidade a ser atualizada.
    :return: Mensagem de sucesso ou erro.
    """
    dados = request.json  # Obtém os dados de atualização
    resultado = banco_de_dados[colecao].update_one({"_id": ObjectId(entidade_id)}, {"$set": dados})  # Atualiza a entidade

    if resultado.matched_count:
        return jsonify({"mensagem": "Entidade atualizada"}), 200  # Retorna mensagem de sucesso
    return jsonify({"erro": "Entidade não encontrada"}), 404  # Retorna erro caso a entidade não seja encontrada


@app.route('/<colecao>', methods=['GET'])
def listar_entidades_paginadas(colecao):
    """
    Rota para listar entidades com paginação.
    :param colecao: Nome da coleção.
    :return: Lista de entidades paginadas em formato JSON.
    """
    consulta = request.args.get("consulta", "{}")  # Obtém a consulta da URL
    consulta = analisar_consulta(consulta)  # Converte a consulta para um dicionário
    campos = request.args.get("campos")  # Obtém os campos para projeção (se presentes)
    pagina = int(request.args.get("pagina", 1))  # Obtém o número da página (padrão: 1)
    tamanho_pagina = int(request.args.get("tamanho_pagina", 10))  # Obtém o tamanho da página (padrão: 10)

    projeção = {campo: 1 for campo in campos.split(',')} if campos else None  # Define os campos para projeção
    pular = (pagina - 1) * tamanho_pagina  # Calcula o número de itens a serem pulados

    entidades = list(banco_de_dados[colecao].find(consulta, projeção).skip(pular).limit(tamanho_pagina))  # Obtém as entidades paginadas
    for entidade in entidades:
        entidade["_id"] = str(entidade["_id"])  # Converte o campo _id para string
    return jsonify(entidades), 200  # Retorna as entidades em formato JSON


if __name__ == '__main__':
    app.run(debug=True)  # Inicializa o servidor Flask em modo de depuração
