# Wishlist-API

## Começando
🚀 Uma API construída com FastAPI e MongoDB.
Este projeto trata de APIs RESTful, operações CRUD e integração com banco de dados não-relacional usando Python para criação de uma lista de favoritos.

## Requisitos
Certifique-se de ter o Python 3.10 ou superior instalado. Você pode instalar as dependências do projeto utilizando o arquivo requirements.txt. Execute o seguinte comando:

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


### Configurar as credenciais e a URI de conexão

Você pode configurar as credenciais e a URI de conexão no arquivo de configuração .env.

Exemplo de .env:

```MONGODB_URI=mongodb://localhost:27017/```

```MONGODB_DB=meu_banco_de_dados```

Certifique-se de ter um servidor MongoDB em execução. O Docker Compose irá gerenciar isso para você, mas é importante que você saiba que o serviço MongoDB está configurado para usar a porta 27018.

## Como usar
Para construir e iniciar os contêineres do Docker, execute o seguinte comando na raiz do projeto, onde se encontra o arquivo docker-compose.yml:


```docker-compose up --build```

Isso iniciará o contêiner FastAPI e o contêiner MongoDB. O FastAPI estará disponível em:
http://localhost:8080.

Você pode acessar a documentação interativa da API em:
http://localhost:8080/docs 

e a interface alternativa em:
http://localhost:8080/redoc


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
* GET /customer: Consulta todos os clientes/customer.
* POST /customer: Cadastrar um cliente/customer.
* GET /customer/{email}: Consulta cliente por email.
* PUT /customer/{email}/update: Atualiza cliente por email.
* DELETE /customer/{email}/delete: Remove um cliente por email.

#### Wishlist
* PUT /customer/{customer_email}/add_favorite/{name_product}: Adiciona item na lista de favoritos.
* DELETE /customer/{customer_email}/favorites: Deletar todos os itens da lista de favoritos.
* DELETE /{customer_email}/remove_favorite/{name_product}: Deletar um itens da lista de favoritos.

#### Product
* POST /product/create: Cadastrar produto.
* GET /product: Consultar todos os produtos.
* DELETE /product/{name_product}: Deletar produto.

#### Product API
* GET /product_api/{page}: Consultar todos os produtos por página.
* GET /product_api/{id}: Consultar todos os produtos por id.

#### Wishlist API
* PUT /product_api/{customer_email}/{product_id}: Adiciona item na lista de favoritos.
* DELETE /product_api/{customer_email}/remove_favorites: Deletar todos os itens da lista de favoritos.
* DELETE /{customer_email}/remove_favorite/{product_id}: Deletar um itens da lista de favoritos.

#### Authentication
* POST /auth: Criar usuário.
