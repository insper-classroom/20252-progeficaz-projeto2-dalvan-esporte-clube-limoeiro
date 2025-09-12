import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("utils.connect_db")  
def test_get_imoveis(mock_connect_db, client):
    """Testa a rota GET /imoveis sem acessar o banco de dados real"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn


    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]

    response = client.get("/imoveis")

    assert response.status_code == 200
    expected_response = {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "Judymouth",
                "cep": "85184",
                "tipo": "casa em condominio",
                "valor": 488423.52,
                "data_aquisicao": "2017-07-29"
            },
            {
                "id": 2,
                "logradouro": "Price Prairie",
                "tipo_logradouro": "Travessa",
                "bairro": "Colonton",
                "cidade": "North Garyville",
                "cep": "93354",
                "tipo": "casa em condominio",
                "valor": 260069.89,
                "data_aquisicao": "2021-11-30"
            }
        ]
    }
    assert response.get_json() == expected_response
    
@patch("utils.connect_db")  
def test_get_imovel_por_id(mock_connect_db, client):
    """Testa a rota GET /imoveis/id sem acessar o banco de dados real"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn


    mock_cursor.fetchall.return_value = [
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]

    response = client.get("/imoveis/2")

    assert response.status_code == 200
    expected_response = {
    "imovel": {
        "id": 2,
        "logradouro": "Price Prairie",
        "tipo_logradouro": "Travessa",
        "bairro": "Colonton",
        "cidade": "North Garyville",
        "cep": "93354",
        "tipo": "casa em condominio",
        "valor": 260069.89,
        "data_aquisicao": "2021-11-30"
    }
}
    assert response.get_json() == expected_response

@patch('utils.connect_db')
def test_atualiza_imoveis(mock_connect_db): #Para rota PUT /imoveis/<id>
    
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    
    dados_atualizados = {
        "logradouro": "Rua nova",
        "tipo_logradouro": "Avenida",
        "bairro": "Itaim",
        "cidade": "São Paulo",
        "cep": "40028-922",
        "tipo": "apartamento",
        "valor": 19000.99,
        "data_aquisicao": "2025-09-12"
    }
    
    response = client.put("/imoveis/1", json = dados_atualizados)
    
    assert response.status_code in [200,400]

@patch("utils.connect_db")  
def test_cria_imovel_db(mock_connect_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    dados_imovel = {
        "logradouro": "Price Prairie",
        "tipo_logradouro": "Travessa",
        "bairro": "Colonton",
        "cidade": "North Garyville",
        "cep": "93354",
        "tipo": "casa em condominio",
        "valor": 260069.89,
        "data_aquisicao": "2021-11-30"
    }

    from servidor import cria_imovel_db
    cria_imovel_db(dados_imovel)

    mock_cursor.execute.assert_called_with(
        """
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            "Price Prairie",
            "Travessa",
            "Colonton",
            "North Garyville",
            "93354",
            "casa em condominio",
            260069.89,
            "2021-11-30"
        )
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("utils.connect_db")
def test_lista_imovel_por_tipo(mock_connect_db, client):
    """Testa a rota GET /imoveis/tipo/<tipo> sem acessar o banco de dados real"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]
    response = client.get("/imoveis/tipo/casa em condominio")
    assert response.status_code == 200
    expected_response = {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "Judymouth",
                "cep": "85184",
                "tipo": "casa em condominio",
                "valor": 488423.52,
                "data_aquisicao": "2017-07-29"
            },
            {
                "id": 2,
                "logradouro": "Price Prairie",
                "tipo_logradouro": "Travessa",
                "bairro": "Colonton",
                "cidade": "North Garyville",
                "cep": "93354",
                "tipo": "casa em condominio",
                "valor": 260069.89,
                "data_aquisicao": "2021-11-30"
            }
        ]
    }
    assert response.get_json() == expected_response
    