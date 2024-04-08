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

Endereço de exposição do container: http://localhost:3002

Documentação das APIs: [SWAGGER](http://localhost:3002/api-docs/)


# 🌐- Frontend ![Badge](https://img.shields.io/static/v1?label=Bootstrap&message=v3.0&color=orange) ![Badge](https://img.shields.io/static/v1?label=jQuery&message=v3.7.1&color=orange)

Exibição de 3 páginas:

- Gráficos de Cotações de Moedas e Cripto-moedas

- Listagem de Notícias

- Administração de APIs

  
## ⚙️ Instalação e Execução (LINUX / WINDOWS + WSL):  

### Premissas para execução do Projeto:

> 💥 Ter instalado o WSL no Windows ou mesmo poderá executar no Linux
>
> 💥 Ter instalado o Docker no WSL ou no Linux

#### Para instalar o Docker no Ubuntu (WSL) / Linux:
    
1. Primeiro, atualize sua lista existente de pacotes:
   
```
$ sudo apt update
```

2. Instale alguns pacotes pré-requisito que deixam o apt usar pacotes pelo HTTPS:

```
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

3. Adicione a chave GPG para o repositório oficial do Docker no seu sistema:

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

4. Adicione o repositório do Docker às fontes do APT:

```
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

5. Atualize o banco de dados do pacote com os pacotes do Docker do recém adicionado repositório:

```
$ sudo apt update
```

6. Certifique-se de que você está prestes a instalar do repositório do Docker ao invés do repositório padrão do Ubuntu:

```
$ apt-cache policy docker-ce
```

7. Você verá um resultado assim, embora o número da versão para o Docker possa ser diferente:

```
docker-ce:
  Installed: (none)
  Candidate: 5:19.03.9~3-0~ubuntu-focal
  Version table:
     5:19.03.9~3-0~ubuntu-focal 500
        500 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages
```

8. Finalmente, instale o Docker:

```
$ sudo apt install docker-ce
```

9. Verifique se ele está funcionando:

```
$ sudo systemctl status docker
```

O resultado deve ser similar ao mostrado a seguir, mostrando que o serviço está ativo e funcionando:

```
Output
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2020-05-19 17:00:41 UTC; 17s ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 24321 (dockerd)
      Tasks: 8
     Memory: 46.4M
     CGroup: /system.slice/docker.service
             └─24321 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
```

10. Se você quiser evitar digitar sudo sempre que você executar o comando docker, adicione seu nome de usuário no grupo docker:

```
$ sudo usermod -aG docker ${USER}
```

11. Para inscrever o novo membro ao grupo, saia do servidor e logue novamente, ou digite o seguinte:

```
$ su - ${USER}
```

Você será solicitado a digitar a senha do seu usuário para continuar.

12. Confirme que seu usuário agora está adicionado ao grupo docker digitando:

```
$ id -nG
```

A saída do comando será algo parecido:

```
sammy sudo docker
```

### Executar os comandos descritos aqui para instalar a aplicação.

```
$ git clone git@github.com:pieroribeiro/pucrio_mvp2_full.git
$ cd pucrio_mvp2_full/
$ docker-compose up -d
```

### Para cancelar a execução dos containers Docker, executar o seguinte comando:

```
$ docker-compose down -v
```

> **PS**: Pelo fato de haver dependências entre os serviços e a criação de uma rede própria para estes, é altamente recomendável a execução através do docker-compose.yml e não separadamente.
