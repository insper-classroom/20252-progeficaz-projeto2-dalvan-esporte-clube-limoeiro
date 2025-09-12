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
