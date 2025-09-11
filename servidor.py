from flask import Flask, request, jsonify
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv('.env')

config = {
    'host': os.getenv('DB_HOST', 'localhost'), 
    'user': os.getenv('DB_USER'),  
    'password': os.getenv('DB_PASSWORD'), 
    'database': os.getenv('DB_NAME', 'db_escola'), 
    'port': int(os.getenv('DB_PORT', 3306)),  
    'ssl_ca': os.getenv('SSL_CA_PATH') 
}


def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        print(f"Erro: {err}")
        return None
    

@app.route("/imoveis", methods=['GET'])
def get_imoveis():
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()

    sql = "SELECT * FROM imoveis"
    cursor.execute(sql)

    results = cursor.fetchall()
    if not results:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    else: 
        imoveis = []
        for imovel in results:
            imovel_dict = {
                "id": imovel[0],
                "logradouro": imovel[1],
                "tipo_logradouro": imovel[2],
                "bairro": imovel[3],
                "cidade": imovel[4],
                "cep": imovel[5],
                "tipo": imovel[6],
                "valor": imovel[7],
                "data_aquisicao": imovel[8],
            }
            imoveis.append(imovel_dict)
        
        resp = {"imoveis": imoveis}
        return resp, 200


@app.route("/imoveis/<int:id>", methods=["GET"])
def get_imovel(id):
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()

    sql = "SELECT * FROM imoveis WHERE id = %s" 
    cursor.execute(sql, (id,))

    imovel = cursor.fetchone()
    

    if not imovel:
        resp = {"erro": "Nenhum imovel encontrado"}
        return resp, 404
    else:
        resp = {
            "imoveis": [
                {
                    "id": imovel[0],
                    "logradouro": imovel[1],
                    "tipo_logradouro": imovel[2],
                    "bairro": imovel[3],
                    "cidade": imovel[4],
                    "cep": imovel[5],
                    "tipo": imovel[6],
                    "valor": imovel[7],
                    "data_aquisicao": imovel[8],
                }
            ]
        }
        return resp, 200

@app.route("/imoveis", methods=["POST"])
def add_imovel():
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    data = request.get_json()

    cursor = conn.cursor()

    sql = "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, (
        data["logradouro"],
        data["tipo_logradouro"],
        data["bairro"],
        data["cidade"],
        data["cep"],
        data["tipo"],
        data["valor"],
        data["data_aquisicao"]
    ))

    conn.commit()
    return jsonify({"mensagem": "imovel criado com sucesso"}), 200



@app.route("/imoveis/<int:id>", methods=["PUT"])
def update_imovel(id):

    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500

    cursor = conn.cursor()
    data = request.get_json()

    sql = "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s"

    cursor.execute(sql,(data["logradouro"],
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

    return jsonify({"mensagem": "imovel atualizado com sucesso"}), 201

@app.route('/imoveis/delete/<int:id>', methods=['DELETE'])
def delete_imovel(id):
    conn = connect_db()

    if conn is None:
        resp = {"erro": "Erro ao conectar ao banco de dados"}
        return resp, 500
    
    cursor = conn.cursor()

    sql = "DELETE FROM imoveis WHERE id =%s"
    cursor.execute(sql,(id,))

    conn.commit()

    resp = {"mensagem": "imovel deletado com sucesso"}

    return resp, 200














if __name__ == '__main__':
    app.run(debug=True)