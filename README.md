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
- **SQLite3** → Banco de dados
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
pip install flask pytest
```

### 4. Inicializar banco de dados
```bash
sqlite3 imoveis.db < imoveis.sql
```

### 5. Executar o servidor
```bash
python servidor.py
```

O servidor rodará em **http://127.0.0.1:5000**

---

## 🌐 Endpoints da API

### 🔹 Listar todos os imóveis
```http
GET /imoveis
```

Resposta:
```json
[
  {"id": 1, "nome": "Casa A", "valor": 500000},
  {"id": 2, "nome": "Apartamento B", "valor": 350000}
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
  "nome": "Terreno X",
  "valor": 150000
}
```

### 🔹 Atualizar imóvel
```http
PUT /imoveis/<id>
```
Body (JSON):
```json
{
  "valor": 200000
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
