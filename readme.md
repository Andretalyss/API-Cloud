

![python3](https://img.shields.io/badge/python-3-1)

# API base para implementação de frontEnd

Breve explicação de como colocar a API para rodar.


## Pré-requisitos para funcionamento

Instale o pacote do python para funcionamento da API.

```bash
  apt-get install python3.9
```

Caso decida usar o docker, instale a ferramenta:
https://docs.docker.com/engine/install/ubuntu/
## Formas de ativar  a API

Há duas formas de execução da API localmente:
- Executando diretamente pelo python na raíz do projeto:

```bash
  python3 main.py
```

- Utilizando uma imagem docker localmente:
    - Crie a imagem docker:
        ```bash
        docker build -t api .
        ```
    - Execute a imagem, passando o parâmetro -d caso não queira visualizar os logs:
        ```bash
        docker run -d -p 5000:5000 api 
        ```

    Após isso a API estará up e pronta para ser acessada.


## API Reference

#### Get EC2 items (Retorna as instâncias por conta, região e state)

```http
  GET /api/ec2/instances
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `account` | `string` | **Required**. (*'328178012196'* or *'574574247426'*) |
| `state`   | `string` | **Optional**. (*'running'* or *'stopped'*)           |


#### Get EBS Items (Retorna os volumes por conta, região e state)

```http
  GET /api/ec2/volumes
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `account` | `string` | **Required**. (*'328178012196'* or *'574574247426'*) |
| `state`   | `string` | **Optional**. (*'available'* or *'in-use'*)           |

#### Get EKS Items (Retorna os clusters por conta, região e versão)

```http
  GET /api/eks/clusters
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `account` | `string` | **Required**. (*'328178012196'* or *'574574247426'*) |
| `version`   | `string` | **Optional**. ex: (*'1.29'*)           |


## Testando funcionamento

Execute no seu terminal linux:

```bash
  curl -X GET http://localhost:5000/api/ec2/instances -H "Content-Type: application/json" -d '{"account": "328178012196"}'
```

- Retorno esperado parecido com:
```bash
[
  {
    "Account": "328178012196",
    "InstanceId": "id-liImNzKcXw",
    "InstanceType": "m6a.large",
    "Name": "ec2-Wd7cY",
    "PrivateIpAddress": "193.161.182.145",
    "Region": "us-east-1",
    "State": "running"
  },
  {
    "Account": "328178012196",
    "InstanceId": "id-FQd73SUCFs",
    "InstanceType": "m6a.large",
    "Name": "ec2-NmuYK",
    "PrivateIpAddress": "57.132.58.31",
    "Region": "us-east-1",
    "State": "stopped"
  }
]
```

