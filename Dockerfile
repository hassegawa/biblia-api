# --- Stage 1: Build das dependências Python e Geração do DB ---
FROM python:3.13-alpine AS builder

# Variáveis de ambiente para o build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para COMPILAR as bibliotecas Python
# e o cliente sqlite3. Limpa o cache imediatamente.
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    sqlite-dev \
    sqlite \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copia os arquivos de dados e scripts SQL para o estágio de build
COPY files/sql/aa.sql /app/files/sql/

# *** NOVIDADE AQUI: Gera o nvi.db neste estágio do build ***
# Certifique-se de que 'nvi.db' será gerado na pasta /app
RUN sqlite3 nvi.db < /app/files/sql/aa.sql \
    && sqlite3 nvi.db "UPDATE verses SET book = book + 1;"

# --- Stage 2: Imagem final de produção ---
FROM python:3.13-alpine

# Instala apenas o CLIE sqlite3 na imagem final.
# Embora o banco de dados já venha pronto, o aplicativo pode precisar do cliente SQLite
# em tempo de execução para interagir com o banco de dados.
# Limpa o cache logo em seguida.
RUN apk add --no-cache \
    sqlite \
    && rm -rf /var/cache/apk/*

# Cria um usuário não-root com UID explícito e dá permissão à pasta /app
RUN mkdir -p /app && adduser -D -u 5678 appuser && chown -R appuser /app

WORKDIR /app

# Copia apenas o requirements.txt primeiro para otimizar o cache da camada
COPY requirements.txt .

# Instala as dependências Python. --no-cache-dir garante que o cache do pip não seja salvo.
RUN pip install --no-cache-dir -r requirements.txt

# *** NOVIDADE AQUI: Copia o nvi.db gerado do estágio 'builder' ***
COPY --from=builder /app/nvi.db /app/nvi.db

# Copia o código da aplicação (main.py e daily.json)
COPY main.py .
COPY daily.json .

# Define a porta da aplicação
EXPOSE 8000

# Muda para o usuário não-root para segurança
USER appuser

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]