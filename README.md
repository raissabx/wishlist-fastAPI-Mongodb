# Wishlist-API

## Começando
🚀 Uma API construída com FastAPI e MongoDB.
Este projeto trata de APIs RESTful, operações CRUD e integração com banco de dados relacional usando Python para criação de uma lista de favoritos.

## Requisitos
Certifique-se de ter o Python 3.10 ou superior instalado. Você pode instalar as dependências do projeto utilizando o arquivo requirements.txt. Execute o seguinte comando:
* python >= 3.10
* pyenv
* pip/poetry
* git
* docker

```pip install -r requirements.txt```

Certifique-se de ter o Docker e o Docker Compose instalados em seu sistema. Para instalar o Docker Compose, siga as instruções na documentação oficial do Docker.

## Configuração do ambiente local
Certifique-se de ter um servidor MongoDB em execução. Você pode configurar as credenciais e a URI de conexão no arquivo de configuração .env.

Exemplo de .env:

```MONGODB_URI=mongodb://localhost:27017/```

```MONGODB_DB=meu_banco_de_dados```

Certifique-se de ter um servidor MongoDB em execução. O Docker Compose irá gerenciar isso para você, mas é importante que você saiba que o serviço MongoDB está configurado para usar a porta 27018.

## Como usar
Para iniciar o servidor FastAPI, você pode usar o comando abaixo:

```make run```

Para construir e iniciar os contêineres do Docker, execute o seguinte comando na raiz do projeto, onde se encontra o arquivo docker-compose.yml:


```docker-compose up --build```

Isso iniciará o contêiner FastAPI e o contêiner MongoDB. O FastAPI estará disponível em http://localhost:8080.

Você pode acessar a documentação interativa da API em http://localhost:8080/docs e a interface alternativa em http://localhost:8080/redoc.

## Endpoints

* GET /favorites: Retorna a lista de todos os favoritos.
* GET /favorites/{favorito_id}: Retorna os detalhes de um favorito específico.
* POST /favorites: Adiciona um novo favorito.
* PUT /favorites/{favorito_id}: Atualiza os detalhes de um favorito existente.
* DELETE /favorites/{favorito_id}: Remove um favorito existente.

