# PUCRIO - MVP Fullstack - BACKEND
Repositório referente ao MVP da disciplina Desenvolvimento Fullstack Básico - Backend

## Swagger (API Documentation):
http://127.0.0.1:5000/openapi/swagger

## 🌐 Finalidade

Este MVP tem a finalidade de um sistema para cadastro de produtos, com as seguintes ações:
  - Listar produtos cadastrados (GET - ALL)
  - Cadastrar Produto (POST)
  - Atualizar produto cadastrado (GET by ID e PUT)
  - Excluir produto cadastrado

## Database concepts:

```
Table Products {
  id integer [pk, unique, not null, increment]
  name varchar
  value float
  created_at timestamp [default: `now()`]
}
``` 

## 🔨 BACKLOG

### 📦 Criação de rotas

🗃️ Adicionar rota para listagem de vendas

🗃️ Adicionar rota para listagem de venda pelo ID da venda

🗃️ Adicionar rota para adicionar novas vendas

🗃️ Adicionar rota para excluir novas vendas (acesso administrativo, ainda no Backlog)

🗃️ Adicionar rota para listar produtos de uma venda

🗃️ Adiocnar rota para adicionar produtos em uma venda

🗃️ Adiocnar rota para excluir produtos em uma venda

### 📦 Criação de Sistema de login:

- Adicionar rota para login
- Adicionar rota para recuperação de senha
- Adicionar rota para cadastro (acesso admin)

### 🛢️ Estrutura de dados a ser composta (adicionada) no Backlog

```
Table Products {
  id integer [pk, unique, not null, increment]
  name varchar
  value float
  created_at timestamp [default: `now()`]
}

Table Sales {
  id integer [pk, unique, not null, increment]
  created_at timestamp [default: `now()`]
}

Table Sales_Products {
  id integer [pk, unique, not null, increment]
  sale_id integer [unique, not null]
  product_id integer
}

Ref: Products.id - Sales_Products.product_id [delete: cascade, update: cascade]
Ref: Sales.id - Sales_Products.sale_id [delete: cascade, update: cascade]
```


## Sistema de Produtos aplicável à qualquer área que demande produtos e vendas:

> Este MVP tem a aplicação para comerciantes de feira.
  
## ⚙️ Instalação e Execução (LINUX):  

> 💢 Este projeto foi construído sobre o Python na versão 3.10.12.
> 
> 💢 Necessário a instalação de todas as bibliotecas contidas em `requirements.txt`.
> 
> 💢 É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
> Executar os comandos descritos aqui para instalar a aplicação:

```
(env)$ git clone git@github.com:pieroribeiro/pucrio_mvp1_backend.git do repositório
(env)$ cd pucrio_mvp1_backend/
(env)$ pip install -r requirements.txt
(env)$ ./run.sh

```
  
> Executar os comandos descritos aqui para executar a aplicação:
> 
> Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.


## 🕸️ Endpoints
| ROUTE | MÉTHOD  | REQUEST | RESPONSE CODE | RESPONSE |
|--|--|--|--|--|
| /product/<int:id> | GET | null | 201 | id: int <br> name: string <br> value: float <br>  created_at: str <br> updated_at: str
| /products/ | GET | null | 201 | List[ {id: int <br> name: string <br> value: float <br>  created_at: str <br> updated_at: str} ]
| /product/ | POST | name: string <br> value: float | 201 | id: int <br> name: string <br> value: float <br>  created_at: str <br> updated_at: str
| /products/<int:id> | PUT | name: string <br> value: float | 201 | message: string
| /product/<int:id> | DELETE | null | 201 | message: string




