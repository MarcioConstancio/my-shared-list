# My Shared List

Este é um projeto Django para uma lista de compras compartilhada, utilizando WebSockets para atualizações em tempo real.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) (Recomendado)
- Git

---

## 🚀 Início Rápido (Com Docker - Recomendado)

A maneira mais fácil e rápida de rodar o projeto é utilizando o Docker. Ele configura automaticamente o banco de dados MySQL, o Redis e a aplicação Web.

1. Clone o repositório e entre na pasta:
   ```bash
   git clone https://github.com/seu-usuario/my-shared-list.git
   cd my-shared-list
   ```

2. Crie um arquivo `.env` na raiz do projeto (o Docker usará essas credenciais para configurar o MySQL):
   ```env
   SECRET_KEY=sua-chave-secreta-muito-segura
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   DB_NAME=my_shared_list
   DB_USER=my_shared_list
   DB_PASSWORD=secret
   ```
   *(Nota: O Docker cuidará de definir `DB_HOST` e `REDIS_HOST` sozinho).*

3. Suba os contêineres em segundo plano:
   ```bash
   docker compose up -d --build
   ```

4. Acesse o aplicativo no seu navegador em `http://localhost:8000`. As migrações do banco de dados são aplicadas automaticamente na inicialização!

---

## 💻 Instalação Local (Sem Docker)

Caso prefira rodar e configurar o ambiente manualmente em sua máquina, siga os passos abaixo:

### 1. Dependências do Sistema

Certifique-se de ter instalado:
- Python 3.8 ou superior
- MySQL Server
- Redis Server

Caso não tenha o MySQL e o Redis instalados, você pode instalá-los e iniciar os serviços com os comandos abaixo:

**MySQL:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**Redis:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**Verificando se estão rodando:**
- **MySQL:** `sudo systemctl status mysql` (deve mostrar como *active/running*)
- **Redis:** `redis-cli ping` (deve retornar `PONG`)

### 2. Preparando o Ambiente Python

1. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuração Local

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=my_shared_list
   DB_USER=seu_usuario_mysql
   DB_PASSWORD=sua_senha_mysql
   DB_HOST=localhost
   DB_PORT=3306
   ```

   Substitua os valores pelas suas configurações.

2. Certifique-se de que o MySQL e Redis estão rodando.

3. Crie o banco de dados no MySQL (Acesse o MySQL com `mysql -u root -p`):

   ```sql
   CREATE DATABASE my_shared_list CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 4. Executando o Projeto

1. Aplique as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

2. Colete os arquivos estáticos:

   ```bash
   python manage.py collectstatic --noinput
   ```

3. Execute o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

   Ou, para suportar WebSockets, use Daphne:

   ```bash
   pip install daphne
   daphne -b 0.0.0.0 -p 8000 shopping_list_project.asgi:application
   ```

4. Acesse o aplicativo em `http://localhost:8000`.

## Funcionalidades

- Lista de compras compartilhada
- Atualizações em tempo real via WebSockets
- API REST com Django REST Framework

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.
