FROM python:3.13-slim

# Impede a criação de arquivos .pyc e não faz buffer da saída no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências de sistema (necessárias para o mysqlclient)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala os pacotes Python
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o restante do projeto
COPY . /app/

# Executa as migrações e a aplicação usando Daphne na porta definida pelo ambiente (ou 8000 como fallback)
CMD sh -c "python manage.py migrate && daphne -b 0.0.0.0 -p ${PORT:-8000} shopping_list_project.asgi:application"
