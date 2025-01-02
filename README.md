# API Flask com MongoDB

Este projeto é uma API RESTful desenvolvida com Flask e MongoDB. Ele permite realizar operações CRUD (Create, Read, Update, Delete) em coleções armazenadas no banco de dados MongoDB.

## Funcionalidades

- **Criar Entidades:** Inserção de novos documentos em coleções do MongoDB.
- **Listar Entidades:** Obtenção de todos os documentos de uma coleção com suporte a projeção de campos.
- **Obter Entidade por ID:** Busca de um documento específico pelo seu identificador.
- **Atualizar Entidade:** Atualização de documentos existentes.
- **Paginar Listagem:** Consulta de documentos com suporte a paginação e filtragem.

## Requisitos

- Python 3.8+
- MongoDB

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git](https://github.com/imetropoledigital/trabalho-ii-unidade-daniel-limaverde.git
   cd trabalho-ii-unidade-daniel-limaverde.git
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências listadas no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. Certifique-se de que o MongoDB está em execução na porta padrão (27017).

5. Execute a aplicação:
   ```bash
   python app.py
   ```

A API estará acessível em `http://127.0.0.1:5000`.

## Endpoints

### Criar Entidade
**POST** `/colecao`

Cria um novo documento na coleção especificada.

- **Exemplo de Corpo da Requisição:**
  ```json
  {
      "nome": "João",
      "idade": 30
  }
  ```
- **Resposta:**
  ```json
  {
      "id": "63a1b2c3d4e5f67890123456"
  }
  ```

### Listar Entidades
**GET** `/colecao`

Lista os documentos de uma coleção.

- **Parâmetros de Consulta:**
  - `consulta` (opcional): String JSON com filtros.
  - `campos` (opcional): Campos a serem projetados, separados por vírgula.

- **Resposta:**
  ```json
  [
      {
          "_id": "63a1b2c3d4e5f67890123456",
          "nome": "João",
          "idade": 30
      }
  ]
  ```

### Obter Entidade por ID
**GET** `/colecao/<entidade_id>`

Retorna os dados de um documento específico.

- **Resposta:**
  ```json
  {
      "_id": "63a1b2c3d4e5f67890123456",
      "nome": "João",
      "idade": 30
  }
  ```

### Atualizar Entidade
**PUT** `/colecao/<entidade_id>`

Atualiza os dados de um documento existente.

- **Exemplo de Corpo da Requisição:**
  ```json
  {
      "idade": 31
  }
  ```
- **Resposta:**
  ```json
  {
      "mensagem": "Entidade atualizada"
  }
  ```

### Listar Entidades com Paginação
**GET** `/colecao`

Lista os documentos de uma coleção com suporte a paginação.

- **Parâmetros de Consulta:**
  - `consulta` (opcional): String JSON com filtros.
  - `campos` (opcional): Campos a serem projetados, separados por vírgula.
  - `pagina` (opcional): Número da página (padrão: 1).
  - `tamanho_pagina` (opcional): Tamanho da página (padrão: 10).

- **Resposta:**
  ```json
  [
      {
          "_id": "63a1b2c3d4e5f67890123456",
          "nome": "João",
          "idade": 30
      }
  ]
  ```

## Estrutura do Projeto

```
.
├── app.py             # Arquivo principal da aplicação
├── requirements.txt   # Lista de dependências
└── README.md          # Documentação do projeto
```

## Dependências

- Flask
- PyMongo
