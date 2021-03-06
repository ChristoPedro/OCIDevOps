# OCIDevOps

Exemplo de Arquitetura Orientada a Eventos utilizando o Stack Cloud Native do OCI.

## Resumo

Arquitetura Cloud Native orientada a eventos utilizando API Gateway + Functions + Streaming + Connetor Hub. É possível através desses componentes criar um fluxo de processamento de dados utilizando funções serveless e filas.

## Arquitetura

![Arquitetura](images/arquitetura.png)

### Fluxo de dados

1. O fluxo se inicia com uma chamada API, onde é utilizado o API Gateway para expor uma função do Functions
2. A função é um producer Kafka que recebe os dados da chamada API e joga as informações para cada uma das filas correspondentes do Streaming.
3. São utilizadas duas filas, NoSQL e File.
4. Connector Hub service trabalha monitorando as filas do Streaming como um Kafka consumer, e quando identifica um novo registro na fila chama a função correspondente de cada uma.
5. Na fila NoSQL é acionada a função no Functions que salva os dados que estão na fila dentro do Autonomous Json
6. Na fila File é iniciada uma função no Functions que cria um arquivo com os dados e salva esse arquivo em um Object Storage

## Deployment

### Criação da Infra

Serão criados os seguintes serviços no OCI:

- [Compartment](#Compartment)
- [Networking](#Networking)
- [Object Storage](#Object-Storage)
- [Autonomous Json](#Autonomous-Json)
- [Streaming](#Streaming)
- [Registry](#Registry)
- [Functions](#Functions)
- [API Gateway](#API-Gateway)
- [Policies](#Policies)

### Deployment do Código

- [Configuração e Deploy do Functions](#Configuração-e-Deploy-do-Functions)
- Configuração do Connetion Hub
- Configuração do API Gateway
- Teste

# Criação da Infra

## Compartment

Navegando no menu do OCI vá em **Identity & Security > Compartimentos**


![compartmentsmenu](images/compartmentsmenu.png)

Agora crie um **Compartment** para o deploy da arquitetura com o nome de usa preferencia:

![compartment](images/compartment.png)

## Networking

Vamos criar um **VCN** (Virtual Cloud Networking), onde sera feito o deploy do Functions, API Gateway e do endpoint privado do Stream.

Navegue no menu do OCI, vá em **Networking > Virtual Cloud Networking**

![menuvcn](images/menuvcn.png)

Vamos criar a rede através do **Wizard** sem a necessidade de colocar alguma informação específica, além do nome.

> :warning: **Crie a VCN dentro do Compartimento criado anteriormente**

![vcn](images/vcn.png)

Com a rede criada vamos adicionar 2 regras a **Security List Default** da rede:

1. Habilitando a comunicação dentro da VCN para qualquer máquina e qualquer porta.

![regra1](images/regra1.png)

2. Habilitando a comunicação com a internet na porta 443 para o Api Gateway 

![regra2](images/regra2.png)

## Object Storage

O **Object Storage** será o destino final dos dados de uma das filas.

Navegue no menu do OCI vá em **Storage > Buckets**

![bucketmenu](images/bucketmenu.png)

> :warning: **Crie o Bucket dentro do Compartimento criado anteriormente**

Crie um Object Storage **Standard** com o nome um nome de sua preferência


![bucketmenu](images/bucket.png)

## Autonomous Json

Para criação do **Autonomous Json** que será o banco NoSQL da arquitetura, navegue no menu do OCI Oracle **Database > Autonomous Json Database**

![autonmousmenu](images/autonomousmenu.png)

Crie um banco Autonomous do tipo **JSON**:

> :warning: **Crie o Banco dentro do Compartimento criado anteriormente**

![autonmous](images/autonomous.png)

Após a criação do banco, vamos pegar o URL do **ORDS** que será usado posteriormente no código.

Na pagina de informações do Autonomous Json vá em **Service Console**:

![serviceconsole](images/serviceconsole.png)

Navegamos para **Deployment** e copiamos o link no quadrado de **RESTful Services and SODA**

![ords](images/ords.png)

> :warning: **Para facilitar futuras configurações salve esse URL em um bloco de notas**

## Streaming

Vamos criar agora um **Stream Pool** para e as duas filas, necessárias.

### Crando o Stream Pool

No menu do OCI vamos em **Analytics & AI > Streaming**

![streamingmenu](images/streamingmenu.png)

No menu lateral vamos selecionar a opção **Stream Pools**

![streampoolmenu](images/streampoolmenu.png)

E criar um novo Stream Pool, onde serão criadas as filas. Nesse caso vamos criar o Pool com **Endpoint Privado** e selecionar a VCN e a Subnet Pública criada anteriormente.

> :warning: **Crie o Stream Pool no Compartimento criado anteriormente**

![streampool](images/streampool.png)

### Criando as Filas

De volta ao menu principal do **Streaming**, vamos dessa vez em **Streams** no menu lateral

![streammenu](images/streammenu.png)

Serão criados dois Streams, no Stream Pool que criamos no passo anterior:

> :warning: **Crie os Streams no Compartimento criado anteriormente**

1. Chamado **Object Storage**

![streamOS](images/streamOS.png)

2. Chamado **NoSQL**

![streamNoSQL](images/streamNoSQL.png)

## Registry

Vamos criar um **OCI Registry** onde as Docker Images do Functions serão armazenadas no OCI.

Navegando no menu do OCI vamos em **Developer Service > Container Registry**

![menuocir](images/menuocir.png)

Crie um novo repositório, lembrando que no nome deve conter apenas letras minusculas e sem caractéres especiais.

> :warning: **Crie o Registry no Compartimento criado anteriormente**

![ocir](images/ocir.png)

## Functions

Vamos criar agora uma nova aplicação no **Oracle Functions**, essa aplicação será o agrupamento lógico das funções que serão utilizadas para inserir e tratar os dados de cada fila.

Navegando no menu do OCI vamos em **Developer Services > Applications**

![FunctionsMenu](images/FunctionsMenu.png)

Criar a nova aplicação na VCN e Subnet Pública Criada anteriormente.

> :warning: **Crie a Aplicação no Compartimento criado anteriormente**

![Functions](images/Functions.png)

## API Gateway

API Gateway vai ser o elemento que nos permitirá realizar chamadas Functions de forma mais simples, nesse caso sem autenticação. Ele vai ser o ponto de entrada de dados no fluxo que estamos criando.

Navegue no menu do OCI vá em **Developer Services > API Managemnt**

![apigatewaymenu](images/apigatewaymenu.png)

Agora vamos criar o Gateway na Subnet Pública da VNC criada anteriormente.

![apigateway](images/apigateway.png)

## Policies

Vamos criar as **Policies** necessárias para a execução desse fluxo.

### Permitir que o Functions possa utilizar os recursos de OCI

```
Allow service FaaS to manage all-resources in compartment [Seu Compartimento]
```

### Permitir que o API Gateway liste e utilize o Functions

```
ALLOW any-user to use functions-family in compartment[Seu Compartimento] where ALL {request.principal.type = 'ApiGateway', request.resource.compartment.id = '[OCID do seu compartimento]'}
```

# Deployment do Código

## Configuração e Deploy do Functions

Para facilitar o deployment do código, vamos utilizar o **Cloud Shell** para fazer o deployment das funções na Aplicação do functions.

### Acessando Cloud Shell

No canto superior direito da Console do OCI, encontramos o botão do **Cloud Shell** entre a Region e o ícone de alerta do OCI.

![cloudshellmenu](images/cloudshellmenu.png)

Um terminal abrirá na parte inferior do navegador

![cloudshell](images/cloudshell.png)

### Clonando o Projeto

Já temos o **GIT** instalado no Cloud Shell, vamos utilizar o seguinte comando para clonar os códigos para o cloud shell

```
git clone https://github.com/ChristoPedro/OCIDevOps.git
```

### Configurando o fn Client

Vamos configurar o client do fn no cloud shell.

#### Gerando Auth Token

Primeiro vamos gerar um **Auth Token** para seu usuário conseguir logar no OCI Registry.

1. Na console do OCI click no icone de usuário no canto superior direito, e depois no seu nome de usuário.

![menuuser](images/menuuser.png)

2. Na página do seu usuário procure no menu lateral **Auth Token**. Depois Click em gerar um novo Token. Só é necessário dar um nome qualquer ao token.


![token](images/token.png)

> :warning: **Copie o token assim que for gerado e salve em algum lugar onde possa recupera-lo. Ele só fica disponível no memoento que é gerado!**

![tokencopy](images/tokencopy.png)

#### Gerando Configurações do fn Client

Com o token salvo podemos voltar na página da aplicação do **Functions** que foi criado anteriormente. Lá teremos um passo a passo de configuração do ambiente para o **Cloud Shell**.

1. No menu do OCI vá em **Developer Services > Applications**

![fnmenu](images/FunctionsMenu.png)

2. Selecione a aplicação criada anteriormente e no menu lateral vá em **Getting Started**

![fngettingstarted](images/fngettingstarted.png)

3. Siga as instruções copiando e colando cada passo no **Cloud Shell** até o passo:

```
fn list apps
```

---
**OBS**

No momento que for executar o passo de fazer login no Docker. Utilize o Auth Token como senha.

---

### Fazendo o Deployment das Funções

