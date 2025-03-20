# Usa Python 3.12 como base
FROM python:3.12

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências primeiro (otimiza o cache do Docker)
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da API
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Iniciar o servidor de desenvolvimento do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
