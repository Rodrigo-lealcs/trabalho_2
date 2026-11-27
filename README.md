# Inventário de ativos e vulnerabilidades (Trabalho 02)

Aplicação em Python, orientada a objetos, que cadastra equipamentos (ativos de TI) e as
vulnerabilidades associadas a eles. Os dados ficam em um arquivo JSON e a aplicação
executa como um serviço HTTP dentro de um container Docker.

Trabalho da disciplina de Cibersegurança (UFU), 2ª atividade avaliativa, Sprints 3 a 5.

## Estado atual

Funciona:

- Classe base `Equipamentos` e classes derivadas `Roteador` e `Servidor` (herança),
  com o campo `tipo` e o método `para_dicionario()`.
- Persistência em JSON: `salvar_equipamentos` grava uma lista de objetos JSON e
  `carregar_equipamentos` recria o objeto da classe certa a partir do campo `tipo`.
- Serviço HTTP (`servidor.py`) em container, com as rotas `/saude` e `/equipamentos`.

Ainda não implementado:

- Modelo de risco com álgebra linear (matrizes M, v e A, risco próprio e efetivo) e as
  dependências entre equipamentos.
- CRUD completo, menu, enumeração de tipos de ativo e cadastro completo de vulnerabilidades
  (descrição, categoria, severidade e status).

## Estrutura do repositório

```
docker-compose.yml        sobe o serviço com "docker compose up -d"
att3/
├── Dockerfile            receita da imagem
├── requirements.txt      dependências declaradas
├── servidor.py           ponto de entrada: serviço HTTP que fica em execução
├── modelos.py            classes dos equipamentos
├── persistencia.py       leitura e gravação do JSON
├── main.py               teste manual de gravação e leitura
├── inventario.py         (vazio por enquanto)
├── risco.py              (vazio por enquanto)
└── data/inventario.json  dados iniciais
```

## Como construir e executar

Requisito: Docker com Docker Compose.

```
git clone https://github.com/Rodrigo-lealcs/trabalho_2.git
cd trabalho_2
docker compose up -d --build
```

Conferir:

- `http://localhost:8000/saude` devolve `{"status": "ok"}`.
- `http://localhost:8000/equipamentos` lista os equipamentos cadastrados.

Ver os logs: `docker compose logs`. Parar: `docker compose down`.

O container usa `restart: unless-stopped`, e os dados ficam em um volume (`inventario_dados`),
então sobrevivem a reinicializações.

Sem Docker (para desenvolvimento):

```
cd att3
pip install -r requirements.txt
python servidor.py
```

## Formato dos dados

O arquivo `data/inventario.json` é uma lista de objetos JSON, um por equipamento. O campo
`tipo` indica a classe a ser criada na leitura.

```json
{
    "id_ativo": 1,
    "nome": "roteador central",
    "ip": "123.245.0.1",
    "vulnerabilidades": [],
    "tipo": "ROTEADOR",
    "quantidade_portas": 4
}
```
