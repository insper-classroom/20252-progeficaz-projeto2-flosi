import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client    
        
@patch("servidor.connect_db")
def test_get_imoveis(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Ronaldo", "Rua", "Moema", "Sao Paulo", 12345, "apartamento", 10000.42, "2014-11-23")
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {"id":1,"logradouro":"Ronaldo", "tipo_logradouro":"Rua", "bairro": "Moema", "cidade":"Sao Paulo", "cep":12345, "tipo":"apartamento", "valor":10000.42, "data_aquisicao":"2014-11-23"}
        ]
    }

    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_get_imovel(mock_connect_db, client):
    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "Ronaldo", "Rua", "Moema", "Sao Paulo", 12345, "apartamento", 10000.42, "2014-11-23")
       


    mock_connect_db.return_value = mock_conn
    response = client.get("/imoveis/1")

    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {"id":1,"logradouro":"Ronaldo", "tipo_logradouro":"Rua", "bairro": "Moema", "cidade":"Sao Paulo", "cep":12345, "tipo":"apartamento", "valor":10000.42, "data_aquisicao":"2014-11-23"}
        ]
    }

    assert response.get_json() == expected_response


@patch("servidor.connect_db")
def test_add_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    

    response = client.post("/imoveis", json= {
        "logradouro": "Jose",
        "tipo_logradouro": "Rua",
        "bairro": "Itaim Bibi",
        "cidade": "São Paulo",
        "cep": "29312852",
        "tipo": "apartamento",
        "valor": "300000",
         "data_aquisicao": "2015-05-07"
    })

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "imovel criado com sucesso"}


@patch("servidor.connect_db")
def test_update_imovel(mock_connect_db, client):
    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    response = client.put("/imoveis/1", json= {"id":1,
                                                "logradouro":"Ronaldo",
                                                "tipo_logradouro":"Rua",
                                                "bairro": "Moema",
                                                "cidade":"Sao Paulo",
                                                "cep":12345,
                                                "tipo":"apartamento",
                                                "valor":10000.42,
                                                "data_aquisicao":"2014-11-23"})
    
    assert response.status_code == 201
    assert response.get_json() == {"mensagem": "imovel atualizado com sucesso"}


@patch("servidor.connect_db")
def test_delete_imovel(mock_connect_db, client):

    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    mock_cursor.rowcount = 1 

    response = client.delete("/imoveis/delete/1")

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "imovel deletado com sucesso"}


@patch("servidor.connect_db")
def test_get_imovel_by_type(mock_connect_db, client):

    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchall.return_value = [
    (1, "Ronaldo", "Rua", "Moema", "São Paulo", 12345, "apartamento", 10000.42, "2014-11-23")
    ]

    response = client.get("/imoveis/tipo/apartamento")

    assert response.status_code == 200

    expected_response = {
        "imoveis": [
            {"id": 1, "logradouro": "Ronaldo", "tipo_logradouro": "Rua", "bairro": "Moema",
             "cidade": "São Paulo", "cep": 12345, "tipo": "apartamento", "valor": 10000.42,
             "data_aquisicao": "2014-11-23"}
            ]
        }
    
    assert response.get_json()== expected_response
