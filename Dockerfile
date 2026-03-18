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

# Executa a aplicação usando Daphne (suporte para WebSockets)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "shopping_list_project.asgi:application"]
