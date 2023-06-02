from flask import Flask, jsonify, request
from conexao import conn

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/clientes/')
def clientes():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM INFO_CLIENTES")
    resultado = cursor.fetchall()
    dados_clientes = []
    for linha in resultado:
        dados = {"id": linha[0], "nome": linha[1], "cpf": linha[2], "estado": linha[3],
               "email": linha[4], "data_nasc": linha[5]}
        dados_clientes.append(dados)
    return jsonify(dados_clientes)


@app.route('/clientes/', methods=['POST'])
def add_cliente():
    try:
        info = request.get_json()
        sql = """INSERT INTO INFO_CLIENTES (nome, cpf, estado, email, data_nasc) 
        values ("{}", "{}", "{}", "{}", "{}")"""\
            .format(info['nome'], info['cpf'], info['estado'], info['email'], info['data_nasc'])
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return 'Dados recebidos e inseridos no banco de dados com sucesso!'
    except Exception as e:
        return 'Erro ao inserir os dados: ' + str(e), 500


@app.route('/clientes/<int:id>', methods=['PUT'])
def att_cliente(id):
    info = request.get_json()
    sql = "SELECT * FROM INFO_CLIENTES WHERE ID = {}".format(id)
    cursor = conn.cursor()
    cursor.execute(sql)
    resposta = cursor.fetchone()
    if resposta[0] > 0:
        if 'nome' in info:
            sql = f"UPDATE INFO_CLIENTES SET NOME = '{info['nome']}' WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
        if 'cpf' in info:
            sql = f"UPDATE INFO_CLIENTES SET CPF = '{info['cpf']}' WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
        if 'estado' in info:
            sql = f"UPDATE INFO_CLIENTES SET ESTADO = '{info['estado']}' WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
        if 'email' in info:
            sql = f"UPDATE INFO_CLIENTES SET EMAIL = '{info['email']}' WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
        if 'data_nasc' in info:
            sql = f"UPDATE INFO_CLIENTES SET DATA_NASC = '{info['data_nasc']}' WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
        return 'Dados Atualizados com sucesso!'
    else:
        return 'ID não foi encontrado!'


@app.route('/clientes/<int:id>', methods=['DELETE'])
def del_clientes(id):
    try:
        cursor = conn.cursor()
        sql = f"SELECT COUNT(*) FROM INFO_CLIENTES WHERE ID = {id}"
        cursor.execute(sql)
        res = cursor.fetchone()
        if res[0] > 0:
            sql1 = f"SELECT NOME FROM INFO_CLIENTES WHERE ID = {id}"
            cursor.execute(sql1)
            res = cursor.fetchone()
            nome = res[0]
            sql = f"DELETE FROM INFO_CLIENTES WHERE ID = {id}"
            cursor.execute(sql)
            conn.commit()
            return f'Cliente: {nome} excluído com sucesso!'
    except Exception as e:
        return 'Erro ao excluir cliente. ' + str(e)


if __name__ == '__main__':
    app.run(debug=True)
