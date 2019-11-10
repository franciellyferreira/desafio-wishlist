# Desafio Wishlist (Lista de Produtos Favoritos)
================================================

<p>
Foi criada uma API para atender a necessidade de 
gerenciar os produtos favoritos dos clientes.
</p>


## Como executar a API
----------------------

### Clonar repositório

Clonar o repositório no seu computador:
```bash
$ cd pasta-desejada
$ git clone https://github.com/franciellyferreira/desafio-wishlist.git
```

### Banco de dados
<p>
Criar um banco de dados MySQL em desenvolvimento ou produção e 
alterar o arquivo settings.py com os dados de conexão.
</p>
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome-do-banco',
        'USER': 'nome-do-usuario',
        'PASSWORD': 'senha-do-usuario',
        'HOST': 'ip-do-host',
        'PORT': 'porta-do-host',
    }
}
```

### Virtualenv

Instalar o Virtualenv:
```bash
$ pip3 install virtualenv
```

### Ambiente virtual

Criar o ambiente virtual com Virtualenv:
```bash
$ cd desafio-wishlist
$ virtualenv venv -p python3
```

Ativar o ambiente virtual:
```bash
$ source venv/bin/activate 
```

Instalar as dependências:
```bash
$ pip3 install -r requirements.txt
```

### Migrations

Criar as migrations
```bash
$ cd wishlist
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Criar super usuário para usar na autenticação
```bash
$ python3 manage.py createsuperuser
```

### Executar Testes

Executar os testes da aplicação
```bash
$ python3 manage.py test
```

### Executar Servidor

Executar o servidor da aplicação
```bash
$ python3 manage.py runserver
```

### Abrir projeto

[API - Wishlist](http://127.0.0.1:8000)

## Endpoints da API
-------------------

<p>
Para fornecer uma documentação rápida e acessível foi criada no Postman a seguinte 
[documentação da API](https://documenter.getpostman.com/view/2628786/SW18wvPe?version=latest)
</p>

### Gerar token para autenticação

<p>
Todos os endpoints precisam de autenticação por token
para serem executados, utilize o endpoint abaixo para gerar
o token que será usado para autenticação.
</p>

Tipo de requisição: POST <br />
Endpoints: http://127.0.0.1:8000/api/auth/ <br />
Entrada:
```bash
{
    "username": "username-do-super-usuario",
    "passwrod": "password-do-super-usuario"
}
```

### Cadastra um novo cliente

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: POST <br />
Endpoints: http://127.0.0.1:8000/api/clients/ <br />
Entrada:
```bash
{
    "name": "nome-do-cliente",
    "email": "email-do-cliente"
}
```

### Obtém todos os clientes

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: GET <br />
Endpoints: http://127.0.0.1:8000/api/clients/ <br />

### Obtém dados de um cliente específico

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: GET <br />
Endpoints: http://127.0.0.1:8000/api/clients/{id-do-cliente}/ <br />


### Atualiza o cadastro do cliente

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: PUT <br />
Endpoints: http://127.0.0.1:8000/api/clients/{id-do-cliente}/ <br />
Entrada:
```bash
{
    "name": "novo-nome-do-cliente",
    "email": "novo-email-do-cliente"
}
```

### Deleta o cadastro do cliente

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: DELETE <br />
Endpoints: http://127.0.0.1:8000/api/clients/{id-do-cliente}/ <br />

### Obtém os produtos favoritos do cliente

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: GET <br />
Endpoints: http://127.0.0.1:8000/api/clients/{id-do-cliente}/wishlist/ <br />

### Adiciona um produto na lista de favoritos

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: POST <br />
Endpoints: http://127.0.0.1:8000/api/wishlist/ <br />
Entrada:
```bash
{
    "client": "id-do-cliente",
    "product_id": "id-do-produto"
}
```

### Remove um produto da lista de favoritos

Adicionar no cabeçalho da requisição: Authorization "Token {token-gerado}"<br />
Tipo de requisição: DELETE <br />
Endpoints: http://127.0.0.1:8000/api/wishlist/{id-do-produto}/{id-do-cliente}/ <br />

## Obrigada por visualizar este desafio!