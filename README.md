# PUCRIO - MVP2 - BACKEND ADVANCED
Repositório referente ao MVP da disciplina Desenvolvimento Fullstack Avançado

## Sobre o projeto

Este MVP foi concebido para demonstrar a arquitetura de comunicação entre micro-serviços isolados.

O objetivo deste modelo é capturar dados de fontes externas e exibí-los de forma agradável e condizente ao mercado financeiro.

Segue abaixo o desenho esquemático da arquitetura:

![Image](/git-assets/img/infraestrutura-v1.0.1.png)

# COMPONENTES DA ARQUITETURA:

# 🌐- Database Container ![Badge](https://img.shields.io/static/v1?label=MySQL&message=v8.0&color=orange)

Container onde está instalado o Banco de Dados MySQL.

Usuário root, Usuário e Senha da aplicação definidos no arquivo Dockerfile

Endereço para conexão ao MySQL: database_host

Porta de exposição do serviço MySQL: 3306

# 🌐- Interceptor Container ![Badge](https://img.shields.io/static/v1?label=Python&message=v3.8&color=orange)

Endereço de exposição do container: http://localhost:3001

Documentação das APIs: [SWAGGER](http://localhost:3001/apidocs/)

# 🌐- Loader Container ![Badge](https://img.shields.io/static/v1?label=NodeJS&message=v18.0&color=orange) 

Este container é o responsável pelo carregamento de todos os dados de APIs externas, modelando os dados de acordo com os contratos previamente estabelecidos.

Este serviço é executado através de CronJobs, com tempos estipulados diretamente de variáveis de ambiente, no arquivo Dockerfile

# 🌐- External APIs ![Badge](https://img.shields.io/static/v1?label=JSON&message={}&color=green)

APIs externas conectadas ao projeto:

[NewsAPIs.org](https://newsapi.org/v2/top-headlines) - Carregamento de Notícias

[AwesomeAPIs](https://economia.awesomeapi.com.br/json/last) - Carregamento de Dados de Moedas e Criptos-Moedas


# 🌐- API Container ![Badge](https://img.shields.io/static/v1?label=NodeJS&message=v18.0&color=orange) 

API que servirá dados para o nosso frontend, contendo os seguintes endpoints:

URL: http://localhost:3002


🚧 ENDPOINTS:


```
Descrição: Endpoint para verificação de status do serviço.
Método HTTP: GET
Exemplo de Requisição:
💥 GET /health
```

```
Descrição: Endpoint para retornar dados de cotações das moedas e cripto-moedas
Método HTTP: GET
Exemplo de Requisição:
💥 GET /finance/:coin
```

```
Descrição: Endpoint para retornar dados de notícias
Método HTTP: GET
Exemplo de Requisição:
💥 GET /news
```

```
Descrição: Endpoint para retornar as apis cadastradas
Método HTTP: GET
Exemplo de Requisição:
💥 GET /api
```

```
Descrição: Endpoint para retornar uma api cadastrada pelo ID
Método HTTP: GET
Exemplo de Requisição:
💥 GET /api/:id
```

```
Descrição: Endpoint para atualizar uma api cadastrada
Método HTTP: GET
Exemplo de Requisição:
💥 PUT /api/:id
```

```
Descrição: Endpoint para excluir uma api cadastrada
Método HTTP: DELETE
Exemplo de Requisição:
💥 DELETE /api/:id
```

# 🌐- Frontend ![Badge](https://img.shields.io/static/v1?label=Bootstrap&message=v3.0&color=orange) ![Badge](https://img.shields.io/static/v1?label=jQuery&message=v3.7.1&color=orange)

Exibição de 3 páginas:

- Gráficos de Cotações de Moedas e Cripto-moedas

- Listagem de Notícias

- Administração de APIs

  
## ⚙️ Instalação e Execução (LINUX / WINDOWS + WSL):  

Premissas para execução do Projeto:

> 💥 Ter instalado o WSL no Windows ou mesmo poderá executar no Linux
>
> 💥 Ter instalado o Docker no WSL ou no Linux

Executar os comandos descritos aqui para instalar a aplicação.

```
$ git clone git@github.com:pieroribeiro/pucrio_mvp2_full.git
$ cd pucrio_mvp2_full/
$ docker-compose up -d
```

Para cancelar a execução dos containers Docker, executar o seguinte comando:

```
$ docker-compose down -v
```

> **PS**: Pelo fato de haver dependências entre os serviços e a criação de uma rede própria para estes, é altamente recomendável a execução através do docker compose e não separadamente.
