# 🏠 Projeto 2 – Dalvan-Esporte-Clube-Limoeiro (Programação Eficaz / Insper)

Este projeto implementa uma **API RESTful em Flask** com integração a banco de dados **SQLite**, destinada ao gerenciamento de **imóveis**.  
Inclui operações de criação, leitura, atualização e exclusão (CRUD), além de **testes automatizados** com `pytest` e `unittest.mock`.

---

## 📂 Estrutura do Projeto

```plaintext
📦 projeto2-dalvan-esporte-clube-limoeiro
 ┣ 📜 servidor.py        # Código principal da API Flask
 ┣ 📜 utils.py           # Funções auxiliares (conexão DB, conversões, etc.)
 ┣ 📜 views.py           # Organização das rotas
 ┣ 📜 test_servidor.py   # Testes automatizados da API
 ┣ 📜 imoveis.sql        # Script SQL para criar e popular o banco
 ┣ 📜 README.md          # Documentação do projeto
 ┣ 📜 .gitignore
 ┗ 📂 __pycache__
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** → Framework web
- **MySQL** → Banco de dados
- **pytest** → Framework de testes
- **unittest.mock** → Mock de dependências externas

---

## 🚀 Executando o Projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/insper-classroom/20252-progeficaz-projeto2-dalvan-esporte-clube-limoeiro.git
cd 20252-progeficaz-projeto2-dalvan-esporte-clube-limoeiro
```

### 2. Criar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente:**
    -   Crie uma cópia do arquivo `template.cred` e renomeie para `.cred`.
    -   Preencha o arquivo `.cred` com as suas credenciais de acesso ao banco de dados MySQL.
    
    _Exemplo de arquivo `.cred`:_
    ```ini
    DB_HOST=localhost
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=db_escola
    DB_PORT=3306
    ```

### 5. Crie a tabela no banco de dados:**
    -   Certifique-se de que o banco de dados (`db_escola` ou outro nome que você definiu) exista.
    -   Execute um script SQL para criar a tabela `imoveis`. (Ex: `schema.sql`).
    ```bash
    # Exemplo de como executar o script
    mysql -u seu_usuario -p db_escola < schema.sql
    ```

O servidor rodará em **http://18.209.61.5**

---

## 🌐 Endpoints da API

### 🔹 Listar todos os imóveis
```http
GET /imoveis
```

Resposta:
```json
[
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
                        "href": "http://18.209.61.5/imoveis/1",
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
                        "href": "http://18.209.61.5/imoveis/2",
                        "method": "GET"
                    }
                }
                
            }
        ]
```

### 🔹 Buscar imóvel por ID
```http
GET /imoveis/<id>
```

### 🔹 Criar novo imóvel
```http
POST /imoveis
```
Body (JSON):
```json
{
    "logradouro": "Avenida Paulista",
    "tipo_logradouro": "Avenida",
    "bairro": "Bela Vista",
    "cidade": "São Paulo",
    "cep": "01310-200",
    "tipo": "Apartamento",
    "valor": 1200000.00,
    "data_aquisicao": "2025-08-15"
}
```

### 🔹 Atualizar imóvel
```http
PUT /imoveis/<id>
```
Body (JSON):
```json
{
    "logradouro": "Avenida Paulista",
    "tipo_logradouro": "Avenida",
    "bairro": "Bela Vista",
    "cidade": "Belo Horizonte",
    "cep": "01310-200",
    "tipo": "Apartamento",
    "valor": 1200000.00,
    "data_aquisicao": "2025-08-15"
}
```

### 🔹 Deletar imóvel
```http
DELETE /imoveis/<id>
```

---

## 🧪 Testes

Rodar todos os testes:
```bash
pytest -v
```

Os testes utilizam **mock de banco de dados**, garantindo independência da API em relação ao SQLite durante execução.

---

## 📖 Conceitos Importantes

- **Flask + REST** → Permite expor o banco de dados via rotas HTTP.  
- **SQLite** → Banco leve, baseado em arquivo, ideal para protótipos.  
- **fetchall() e fetchone()** → Recuperam múltiplos ou um único registro do banco.  
- **jsonify() e request.get_json()** → Serializam/desserializam dados entre **cliente ↔ servidor**.  
- **Mocks** → Substituem funções externas em testes (ex: conexão ao DB).  

---

## 👥 Autores

Projeto desenvolvido para a disciplina **Programação Eficaz – Insper**  

👤 Dalvan – Esporte Clube Limoeiro
