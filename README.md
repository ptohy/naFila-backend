
# naFila - Backend API

**API RESTful para gerenciar sua fila de conteúdos!**  
Gerencie livros, vídeos, podcasts, séries, artigos e muito mais, com controle de status, progresso e organização.

---

## Visão Geral

Este repositório contém a API do projeto **naFila**, desenvolvida em **Python com Flask**, como parte do MVP da pós-graduação em **Desenvolvimento Full Stack na PUC RIO**.

A API oferece um conjunto de endpoints RESTful para gerenciar conteúdos, permitindo operações como criação, leitura, atualização, remoção e organização.

---

## Funcionalidades da API

- ✅ Cadastrar conteúdos (livros, vídeos, podcasts, etc).
- ✅ Listar todos os conteúdos.
- ✅ Filtrar conteúdos por status, tipo ou título.
- ✅ Atualizar informações de um conteúdo (status, progresso, título, tipo).
- ✅ Deletar conteúdos.
- ✅ Suporte a organização com drag & drop (posição/ordem).
- ✅ Persistência de dados via **SQLite**.
- ✅ Documentação automática via **Swagger (OpenAPI)**.

---

**Swagger disponível em:**  
`http://127.0.0.1:5000/apidocs/`

---

## Como Executar o Projeto

### Pré-requisitos:
- Python 3.x instalado.

### Instalação:

1. Clone o repositório:

```bash
git clone https://github.com/ptohy/nafila-backend.git
```

2. Acesse a pasta do projeto:

```bash
cd nafila-backend
```

3. Crie um ambiente virtual (recomendado):

```bash
python -m venv venv
```

4. Ative o ambiente virtual:

- No Windows:

```bash
venv\Scripts\activate
```

- No macOS/Linux:

```bash
source venv/bin/activate
```

5. Instale as dependências:

```bash
pip install -r requirements.txt
```

6. Execute a aplicação:

```bash
python app.py
```

7. Acesse a API no navegador ou via ferramentas como Postman em:  
`http://127.0.0.1:5000`

8. Para acessar a documentação Swagger:  
`http://127.0.0.1:5000/apidocs/`

---

## Integração com o Frontend

O frontend consome todos os endpoints desta API.  
[Repositório do Frontend](https://github.com/ptohy/naFila-frontend)

---
