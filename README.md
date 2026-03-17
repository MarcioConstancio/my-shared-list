# My Shared List

Este é um projeto Django para uma lista de compras compartilhada, utilizando WebSockets para atualizações em tempo real.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- MySQL Server
- Redis Server
- Git

### Instalando MySQL e Redis (Linux Ubuntu/Debian)

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

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/my-shared-list.git
   cd my-shared-list
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

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

3. Crie o banco de dados no MySQL:

   ```sql
   CREATE DATABASE my_shared_list CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

## Executando o Projeto

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
