import pytest
import views
from unittest.mock import patch, MagicMock
from servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("servidor.connect_db")  
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
    expected_response =[
        {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "Judymouth",
                "cep": "85184",
                "tipo": "casa em condominio",
                "valor": 488423.52,
                "data_aquisicao": "2017-07-29",
                "z_links": {
                    "self": {
                        "href": "http://localhost/imoveis/1",
                        "method": "GET"
                    }
                }
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
                "data_aquisicao": "2021-11-30",
                "z_links": {
                    "self": {
                        "href": "http://localhost/imoveis/2",
                        "method": "GET"
                    }
                }
                
            }
        ]
    assert response.get_json() == expected_response
    
@patch("servidor.connect_db")  
def test_get_imovel_por_id(mock_connect_db, client):
    """Testa a rota GET /imoveis/id sem acessar o banco de dados real"""
    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchone.return_value = (
        2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', 
        '93354', 'casa em condominio', 260069.89, '2021-11-30'
    )

    response = client.get("/imoveis/2")

    assert response.status_code == 200
    
    expected_response = {
        "id": 2,
        "logradouro": "Price Prairie",
        "tipo_logradouro": "Travessa",
        "bairro": "Colonton",
        "cidade": "North Garyville",
        "cep": "93354",
        "tipo": "casa em condominio",
        "valor": 260069.89,
        "data_aquisicao": "2021-11-30",
        "z_links": {
            "self": {"href": "http://localhost/imoveis/2", "method": "GET"},
            "update": {"href": "http://localhost/imoveis/2", "method": "PUT"},
            "delete": {"href": "http://localhost/imoveis/2", "method": "DELETE"},
            "collection": {"href": "http://localhost/imoveis", "method": "GET"}
        }
    }
    
    assert response.get_json() == expected_response

@patch("servidor.connect_db")
def test_atualiza_imoveis_sucesso(mock_connect_db, client):
    """Testa PUT /imoveis/<id> quando o imóvel existe"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.return_value = [
        (1, "Rua Velha", "Rua", "Centro", "São Paulo", "01000-000", "apartamento", 400000.0, "2020-01-01")
    ]

    
    mock_cursor.fetchone.return_value = (
        1, "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000",
        "apartamento", 500000.0, "2023-01-01"
    )

    
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

    response = client.put("/imoveis/1", json=dados_atualizados)

    
    assert response.status_code == 200
    expected_response = {
        "id": 1,
        **dados_atualizados,
        "z_links": {
            "self": {"href": "http://localhost/imoveis/1", "method": "GET"},
            "update": {"href": "http://localhost/imoveis/1", "method": "PUT"},
            "delete": {"href": "http://localhost/imoveis/1", "method": "DELETE"},
            "collection": {"href": "http://localhost/imoveis", "method": "GET"}
        }
    }
    assert response.get_json() == expected_response
    

    
    mock_cursor.execute.assert_any_call(
        """
        UPDATE imoveis
        SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s, cep=%s, tipo=%s, valor=%s, data_aquisicao=%s
        WHERE id=%s
    """, (
        "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000",
        "apartamento", 500000.0, "2023-01-01", 1
    ))
    mock_conn.commit.assert_called_once()


@patch("servidor.connect_db")
def test_atualiza_imoveis_nao_encontrado(mock_connect_db, client):
    """Testa PUT /imoveis/<id> quando o imóvel não existe"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.return_value = []

    
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

    response = client.put("/imoveis/999", json=dados_atualizados)

    
    assert response.status_code == 404
    assert response.get_json() == {"mensagem": "imóvel não encontrado"}

    
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis WHERE id=%s", (999,))
    mock_conn.commit.assert_not_called()


@patch("servidor.connect_db")  
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

    views.cria_imovel_db(mock_conn, dados_imovel)

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

@patch("servidor.connect_db")
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
    expected_response = [
            {
                "id": 1,
                "logradouro": "Nicole Common",
                "tipo_logradouro": "Travessa",
                "bairro": "Lake Danielle",
                "cidade": "Judymouth",
                "cep": "85184",
                "tipo": "casa em condominio",
                "valor": 488423.52,
                "data_aquisicao": "2017-07-29",
                "z_links": { "self": {"href": "http://localhost/imoveis/1","method": "GET"}}
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
                "data_aquisicao": "2021-11-30",
                "z_links": { "self": {"href": "http://localhost/imoveis/2","method": "GET"}}
            }
        ]
    assert response.get_json() == expected_response

@patch("servidor.connect_db")
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
    expected_response = [
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
    assert response.get_json() == expected_response
    
@patch("servidor.connect_db")
def test_delete_imovel_sucesso(mock_connect_db, client):
    """Testa DELETE /imoveis/<id> quando o imóvel existe"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.return_value = [
        (1, "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000",
         "apartamento", 500000.0, "2023-01-01")
    ]

    response = client.delete("/imoveis/1")

    
    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "imóvel removido com sucesso."}

    
    mock_cursor.execute.assert_any_call("DELETE FROM imoveis WHERE id=%s", (1,))
    mock_conn.commit.assert_called_once()


@patch("servidor.connect_db")
def test_delete_imovel_nao_encontrado(mock_connect_db, client):
    """Testa DELETE /imoveis/<id> quando o imóvel não existe"""

    
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.return_value = []

    response = client.delete("/imoveis/999")

    
    assert response.status_code == 404
    assert response.get_json() == {"mensagem": "imóvel não encontrado"}

    
    mock_cursor.execute.assert_called_once_with("SELECT * FROM imoveis WHERE id=%s", (999,))
    mock_conn.commit.assert_not_called()

@patch("servidor.connect_db")
def test_get_imovel_por_id_retorna_links_hateoas(mock_connect_db, client):
    """Testa se a rota GET /imoveis/<id> retorna os links HATEOAS corretos."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    
    mock_cursor.fetchone.return_value = (
    2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', 
    '93354', 'casa em condominio', 260069.89, '2021-11-30'
    )
    
    response = client.get("/imoveis/1")
    data = response.get_json()

    assert response.status_code == 200
    
    assert "z_links" in data
    links = data["z_links"]
    assert "self" in links
    assert "update" in links
    assert "delete" in links
    assert "collection" in links
    
    assert links["self"]["href"] == "http://localhost/imoveis/1"
    assert links["collection"]["href"] == "http://localhost/imoveis"

@patch("servidor.connect_db")    
def test_cria_imovel_retorna_header_location(mock_connect_db, client):
    """Testa se a rota POST /imoveis retorna o cabeçalho Location."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    mock_cursor.lastrowid = 101

    novo_imovel_data = {"logradouro": "Rua TDD", "tipo": "casa", "cidade": "Teste", "valor": 1, "data_aquisicao": "2025-01-01", "tipo_logradouro":"Rua", "bairro": "Centro", "cep":"123456"}

    response = client.post("/imoveis", json=novo_imovel_data)

    assert response.status_code == 201
    assert "Location" in response.headers
    assert response.headers["Location"] == "http://localhost/imoveis/101"
    
@patch("servidor.connect_db")
def test_listar_imoveis_retorna_links_em_cada_item(mock_connect_db, client):
    """Testa se GET /imoveis retorna uma lista onde cada item tem seu link HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    mock_cursor.fetchall.return_value = [
        (1, 'Rua das Flores', 'Rua', 'Jardim', 'Campinas', '13000-000', 'casa', 250000, '2022-01-15'),
        (2, 'Avenida Principal', 'Avenida', 'Centro', 'São Paulo', '01000-000', 'apartamento', 500000, '2021-05-20'),
    ]

    response = client.get("/imoveis")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list) 
    assert len(data) == 2         

    assert "z_links" in data[0]
    assert "self" in data[0]["z_links"]
    assert data[0]["z_links"]["self"]["href"] == "http://localhost/imoveis/1"

    assert "z_links" in data[1]
    assert "self" in data[1]["z_links"]
    assert data[1]["z_links"]["self"]["href"] == "http://localhost/imoveis/2"
    
    
@patch("servidor.connect_db")
def test_atualiza_imoveis_sucesso_retorna_links_em_cada_item(mock_connect_db, client):
    """Testa se GET /imoveis retorna uma lista onde cada item tem seu link HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    
    
    mock_cursor.fetchall.return_value = [
        (1, "Rua Velha", "Rua", "Centro", "São Paulo", "01000-000", "apartamento", 400000.0, "2020-01-01")
    ]

    
    mock_cursor.fetchone.return_value = (
        1, "Rua Nova", "Avenida", "Centro", "São Paulo", "01000-000",
        "apartamento", 500000.0, "2023-01-01"
    )

    
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
    
    
    response = client.put("/imoveis/1", json=dados_atualizados)

    assert response.status_code == 200
    data = response.get_json()
    
    assert data["id"] == 1
    for key, value in dados_atualizados.items():
        assert data[key] == value

    
    assert "z_links" in data
    links = data["z_links"]

    assert "self" in links
    assert links["self"]["href"] == "http://localhost/imoveis/1"
    assert links["self"]["method"] == "GET"

    assert "update" in links
    assert links["update"]["href"] == "http://localhost/imoveis/1"
    assert links["update"]["method"] == "PUT"

    assert "delete" in links
    assert links["delete"]["href"] == "http://localhost/imoveis/1"
    assert links["delete"]["method"] == "DELETE"

    assert "collection" in links
    assert links["collection"]["href"] == "http://localhost/imoveis"
    assert links["collection"]["method"] == "GET"
    

     
@patch("servidor.connect_db")
def test_lista_imovel_por_tipo_retorna_links_em_cada_item(mock_connect_db, client):
    """Testa a rota GET /imoveis/tipo/<tipo> verificando dados e links HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn
    

    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', 488423.52, '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', 260069.89, '2021-11-30'),
    ]
    
    response = client.get("/imoveis/tipo/casa em condominio")
    data = response.get_json()

    
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    
    imovel1 = data[0]
    assert imovel1["id"] == 1
    assert imovel1["logradouro"] == "Nicole Common"
    assert imovel1["tipo_logradouro"] == "Travessa"
    assert imovel1["bairro"] == "Lake Danielle"
    assert imovel1["cidade"] == "Judymouth"
    assert imovel1["tipo"] == "casa em condominio"
    assert imovel1["valor"] == 488423.52
    assert imovel1["data_aquisicao"] == "2017-07-29"

    assert "z_links" in imovel1
    links1 = imovel1["z_links"]
    assert links1["self"]["href"] == "http://localhost/imoveis/1"
    assert links1["self"]["method"] == "GET"

    imovel2 = data[1]
    assert imovel2["id"] == 2
    assert imovel2["logradouro"] == "Price Prairie"
    assert imovel2["cidade"] == "North Garyville"

    assert "z_links" in imovel2
    links2 = imovel2["z_links"]
    assert links2["self"]["href"] == "http://localhost/imoveis/2"
    assert links2["self"]["method"] == "GET"
   


@patch("servidor.connect_db")
def test_lista_imoveis_por_cidade_retorna_links(mock_connect_db, client):
    """Testa se GET /imoveis/cidade/<cidade> retorna imóveis com links HATEOAS."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    
    mock_cursor.fetchall.return_value = [
        (1, 'Rua A', 'Rua', 'Bairro A', 'Campinas', '13000-000', 'casa', 250000, '2022-01-15'),
        (2, 'Avenida B', 'Avenida', 'Bairro B', 'Campinas', '13000-111', 'apartamento', 500000, '2021-05-20'),
    ]

    response = client.get("/imoveis/cidade/Campinas")
    data = response.get_json()

    
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    
    imovel1 = data[0]
    assert imovel1["id"] == 1
    assert imovel1["cidade"] == "Campinas"
    assert "z_links" in imovel1
    assert imovel1["z_links"]["self"]["href"] == "http://localhost/imoveis/1"
    assert imovel1["z_links"]["self"]["method"] == "GET"

    
    imovel2 = data[1]
    assert imovel2["id"] == 2
    assert imovel2["cidade"] == "Campinas"
    assert "z_links" in imovel2
    assert imovel2["z_links"]["self"]["href"] == "http://localhost/imoveis/2"
    assert imovel2["z_links"]["self"]["method"] == "GET"
