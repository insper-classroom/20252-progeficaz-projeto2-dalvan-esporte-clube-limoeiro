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

@patch("utils.connect_db")
def test_atualiza_imoveis(mock_connect_db, client):
    """Testa a rota PUT /imoveis/<id> sem acessar o banco real"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.side_effect = [
        [(1, "Rua Velha", "Rua", "Centro", "São Paulo", "01000-000", "apartamento", 400000.0, "2020-01-01")],  # SELECT antes do update
        [(1, "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000", "apartamento", 500000.0, "2023-01-01")]  # SELECT depois do update
    ]

    
    dados_atualizados = {
        "logradouro": "Rua Nova",
        "tipo_logradouro": "Avenida",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01000-000",
        "tipo": "apartamento",
        "valor": 500000.0,
        "data_aquisicao": "2023-01-01"
    }

    
    response = client.put(
        "/imoveis/1",
        json=dados_atualizados
    )

    
    assert response.status_code == 200
    expected_response = {
        "imovel": {
            "id": 1,
            **dados_atualizados
        }
    }
    assert response.get_json() == expected_response

    # garante que UPDATE e COMMIT foram chamados
    mock_cursor.execute.assert_any_call(
        """
        UPDATE imoveis
        SET logradouro=?, tipo_logradouro=?, bairro=?, cidade=?, cep=?, tipo=?, valor=?, data_aquisicao=?
        WHERE id=?
    """, (
        "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000",
        "apartamento", 500000.0, "2023-01-01", 1
    ))
    mock_conn.commit.assert_called_once()


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

@patch("utils.connect_db")
def test_lista_imovel_por_cidade(mock_connect_db, client):
    """Testa a rota GET /imoveis/cidade/<cidade> sem acessar o banco de dados real"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'North Garyville', '85184', 'casa', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]
    response = client.get("/imoveis/cidade/North Garyville")
    assert response.status_code == 200
    expected_response = {
        "imoveis": [
            {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "North Garyville",
                "cep": "85184",
                "tipo": "casa",
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
    
    