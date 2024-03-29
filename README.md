# Wishlist-API

## Começando
🚀 Uma API construída com FastAPI e MongoDB.
Este projeto trata de APIs RESTful, operações CRUD e integração com banco de dados não-relacional usando Python para criação de uma lista de favoritos.

## Requisitos
Certifique-se de ter o Python 3.10 ou superior instalado. Você pode instalar as dependências do projeto utilizando o arquivo requirements.txt.

* [python >= 3.10](https://www.python.org/)
* [pyenv](https://github.com/pyenv/pyenv)
* [pip](https://pypi.org/project/pip/)
* [git](https://git-scm.com/)
* [docker](https://www.docker.com/)



Certifique-se de ter o Docker e o Docker Compose instalados em seu sistema. Para instalar o Docker Compose, siga as instruções na documentação oficial do Docker.

## Configuração do ambiente local

#### Passo 1: Instalar o virtualenv (caso não tenha instalado)

Se você ainda não tem o virtualenv instalado, pode instalá-lo usando o pip, o gerenciador de pacotes do Python. Abra o terminal e execute o seguinte comando:

```pip install virtualenv```

#### Passo 2: Criar uma Virtual Environment
1- Abra o terminal e navegue até o diretório raiz do seu projeto.
2- Para criar uma nova virtual environment, execute o seguinte comando:

```virtualenv venv```

Isso criará uma pasta chamada venv no diretório do seu projeto, contendo todos os pacotes Python necessários para o seu ambiente virtual.

#### Passo 3: Ativar a Virtual Environment

Para ativar a virtual environment, execute o seguinte comando no terminal:

* No Windows:

```venv\Scripts\activate```

* No macOS/Linux:

```source venv/bin/activate```

Você saberá que a virtual environment está ativada quando o nome dela aparecer no seu prompt de comando.

#### Passo 4: Instalar Pacotes Requirements usando pip

Com a virtual environment ativada, você pode usar o pip para instalar pacotes Requirements, execute o seguinte comando:

```pip install -r requirements.txt```

## Como usar
Para construir e iniciar os contêineres do Docker, execute o seguinte comando na raiz do projeto, onde se encontra o arquivo docker-compose.yml:


```docker-compose up -d```

Isso iniciará o contêiner FastAPI e o contêiner MongoDB. O FastAPI estará disponível em:
http://localhost:8081.

Você pode acessar a documentação interativa da API em:
http://localhost:8081/docs 

e a interface alternativa em:
http://localhost:8081/redoc


### Iniciar o servidor FastAPI

Para iniciar o servidor FastAPI, você pode usar o comando abaixo:

```make run```

### Testes

Para executar os testes de unidade, execute:

```pytest```

Para executar um teste específico ou uma coleção de testes com nome comum, execute:

```pytest -x <path da pasta> -k <nome do teste>```

Exemplo:
```pytest -x tests/test_route_customer.py -k test_create_customer```

## Endpoints

#### Customer
* GET /customers: Consultar todos os clientes.
* POST /customers: Cadastrar um clientes.
* GET /customers/{email}: Consultar clientes por email.
* PUT /customers/{email}/update: Atualizar clientes.
* DELETE /customers/{email}: Remover clientes.

#### Wishlist
* PUT /customers/{customer_email}/add_favorites/{id_product}: Adicionar item na lista de favoritos.
* DELETE /customer/{customer_email}/favorites: Deletar todos os itens da lista de favoritos.
* DELETE /customers/{customer_email}/remove_favorites/{id_product}: Deletar um itens da lista de favoritos.

#### Product
* POST /products: Cadastrar produtos.
* GET /products: Consultar todos os produtos.
* GET /products/{id}: Consultar produtos pelo id.
* DELETE /products/{id}: Deletar produtos.

#### Product API
* GET /product_api/{page}: Consultar todos os produtos por página.
* GET /product_api/{id}: Consultar todos os produtos por id.

#### Wishlist API
* PUT /product_api/{customer_email}/{product_id}: Adiciona item na lista de favoritos.
* DELETE /product_api/{customer_email}/remove_favorites: Deletar todos os itens da lista de favoritos.
* DELETE /{customer_email}/remove_favorite/{product_id}: Deletar um itens da lista de favoritos.

#### Authentication
* POST /auth: Criar usuário.
