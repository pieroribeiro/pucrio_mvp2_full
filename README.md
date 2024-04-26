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

Endereço de exposição do container: [URL](http://localhost:3002/)

Documentação das APIs: [SWAGGER](http://localhost:3002/api-docs/)


# 🌐- Frontend ![Badge](https://img.shields.io/static/v1?label=Bootstrap&message=v3.0&color=orange) ![Badge](https://img.shields.io/static/v1?label=jQuery&message=v3.7.1&color=orange)

URL: (http://localhost:3003/)

Exibição de 3 páginas:

- Gráficos de Cotações de Moedas e Cripto-moedas

- Listagem de Notícias

- Administração de APIs

  
## ⚙️ Instalação e Execução (LINUX / WINDOWS + WSL):  

### Premissas para execução do Projeto:

> 💥 Ter instalado o WSL no Windows ou mesmo poderá executar no Linux
>
> 💥 Ter instalado o Docker no WSL ou no Linux
>
> 💥 Ter instalado o Docker-Compose no WSL ou no Linux

#### Para instalar o Docker no Ubuntu (WSL) / Linux:



> 🔆 Adicionar as chaves GPG Oficiais do Docker:
```
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

> 🔆 Adicionar o repositório ao APT Sources:
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

> 🔆 Instalar os pacotes do Docker:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin
```

> 🔆 Verificar se o Docker foi instalado corretamente:
```
sudo service docker status
```
A saída do comando deverá ser algo parecido com isso:
```
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2024-04-26 09:50:23 -03; 46min ago
TriggeredBy: ● docker.socket
       Docs: https://docs.docker.com
   Main PID: 5887 (dockerd)
      Tasks: 10
     Memory: 42.2M
     CGroup: /system.slice/docker.service
```

> 🔆 Executar uma imagem de teste:
```
sudo docker run hello-world
```

> 🔆 Se você quiser evitar digitar sudo sempre que você executar o comando docker, adicione seu nome de usuário no grupo docker:
```
sudo usermod -aG docker ${USER}
```

> 🔆 Para inscrever o novo membro ao grupo, saia do servidor e logue novamente, ou digite o seguinte:
```
su - ${USER}
```

> 🔆 Instalar o Docker-Compose:
```
sudo curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod 775 /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

> 🔆 Verificar se o Docker-Compose foi isntalado corretamente:
```
docker-compose version
```

### Executar os comandos descritos aqui para instalar a aplicação.

```
git clone git@github.com:pieroribeiro/pucrio_mvp2_full.git
cd pucrio_mvp2_full/
docker-compose up -d
```

### Para cancelar a execução dos containers Docker, executar o seguinte comando:

```
docker-compose down -v
```

> **PS**: Pelo fato de haver dependências entre os serviços e a criação de uma rede própria para estes, é altamente recomendável a execução através do docker-compose.yml e não separadamente.
