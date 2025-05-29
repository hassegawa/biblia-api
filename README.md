# Bíblia API

API REST para consulta de versículos bíblicos, leitura diária e sorteio de versículos, baseada em FastAPI e SQLite.

## Como executar em docker

  * docker run -d -p 8000:8000 -e ROOT_PATH=/api hassegawa/biblia-api
  # Use a variável de ambiente ROOT_PATH para definir o prefixo dos endpoints (opcional)


## Como usar com Docker Compose

1. **Crie o arquivo `docker-compose.yml`** na raiz do projeto:

    ```yaml
    version: '3.8'
    services:
      biblia-api:
        build: .
        container_name: biblia-api
        ports:
          - "8000:8000"
        volumes:
          - .:/app
        environment:
          - TZ=America/Sao_Paulo
          - ROOT_PATH=/api  # Define o prefixo dos endpoints (opcional)
    ```

2. **Crie o arquivo `Dockerfile`** na raiz do projeto:

    ```Dockerfile
    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 8000

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

3. **Crie o arquivo `requirements.txt`** (se ainda não existir):

    ```
    fastapi
    uvicorn
    ```

4. **Certifique-se de que o arquivo do banco de dados `nvi.db` e o arquivo `daily.json` estejam na raiz do projeto.**

5. **Suba o serviço:**

    ```sh
    docker-compose up --build
    ```

A API estará disponível em [http://localhost:8000](http://localhost:8000).

---

## Endpoints da API

### 1. Listar todos os livros

```
GET /
```

**Resposta:**
```json
{
  "books": [
    {
      "id": 1,
      "name": "Gênesis",
      "abbrev": "gn",
      ...
    },
    ...
  ]
}
```

---

### 2. Buscar versículo(s)

```
GET /verse?book=Gênesis&chapter=1&verse=1
```

**Parâmetros:**
- `book` (opcional): Nome do livro
- `chapter` (opcional): Número do capítulo
- `verse` (opcional): Número do versículo
- `endverse` (opcional): Número do último versículo (para intervalo)

**Resposta:**
```json
{
  "verse": [
    {
      "name": "Gênesis",
      "chapter": 1,
      "verse": 1,
      "text": "No princípio criou Deus os céus e a terra."
    }
  ]
}
```

---

### 3. Versículo do dia

```
GET /daily
```

Retorna o(s) versículo(s) correspondente(s) ao dia atual, conforme definido em `daily.json`.

---

### 4. Versículo do dia (formato mensagem)

```
GET /today
```

Retorna o(s) versículo(s) do dia em formato de mensagem única.

---

### 5. Versículo aleatório

```
GET /random
```

Retorna um versículo aleatório da lista `daily.json`.

---

### 6. Checar integridade dos versículos do dia

```
GET /check
```

Retorna uma lista de itens de `daily.json` que não foram encontrados no banco de dados.

---

## Observações

- Para alterar o prefixo dos endpoints da API (por exemplo, servir em `/api` ao invés de `/`), defina a variável de ambiente `ROOT_PATH`.  
  Exemplo: `ROOT_PATH=/api`
- Certifique-se de que os arquivos `nvi.db` (banco SQLite) e `daily.json` estejam presentes na raiz do projeto.
- Para acessar a documentação interativa da API, acesse [http://localhost:8000/docs](http://localhost:8000/docs) após subir o container.

---
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 
[Docker hub](https://hub.docker.com/r/hassegawa/biblia-api)

---

[![Foo](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/hassegawa)    
