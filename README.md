# Inventário de equipamentos e vulnerabilidades

Trabalho de Cibersegurança (UFU), feito em Python.

O programa guarda uma lista de equipamentos de rede (roteador, servidor, notebook, banco de dados e outros)
e as vulnerabilidades de cada um. Ele também calcula uma nota de risco para cada equipamento.

## Como rodar

Com Docker (como será entregue no servidor):

    docker compose up -d --build
    curl localhost:8000/saude

Sem Docker, dentro da pasta `app`:

    python main.py        (abre o menu)
    python servidor.py    (liga o serviço na porta 8000)
    python -m pytest      (roda os testes)

> Observação: os testes e o menu foram executados no meu computador.
> O Docker ainda precisa ser conferido no servidor.

## O que tem em cada arquivo

- `modelos.py`: as classes. `Equipamentos` é a classe mãe; `Roteador`, `Servidor`, `Notebook`, `BancoDeDados` e `Outro` (câmera, switch, impressora...) herdam dela.
- `persistencia.py`: salva e lê os dados nos arquivos JSON.
- `inventario.py`: cadastrar, listar, buscar, atualizar e remover.
- `risco.py`: o cálculo do risco.
- `main.py`: o menu.
- `servidor.py`: o serviço que fica ligado no container.

## Como o risco é calculado

1. Cada vulnerabilidade tem uma nota (baixa 2, média 5, alta 7,5, crítica 9,5).
2. O **risco próprio** de um equipamento é a soma das notas das suas vulnerabilidades, multiplicada por um peso do tipo dele (servidor pesa mais que notebook).
3. Alguns equipamentos dependem de outros. Quem depende recebe uma parte do risco do outro.
4. Isso vira a equação **(I − A) x = b**, em que b é o risco próprio, A são as dependências e x é o risco final.
5. Antes de resolver, o programa confere se a equação tem uma única solução (matriz invertível).

Exemplo feito à mão (está nos testes): b = 9, 18,75 e 5. Resultado final: 9, 20,55 e 15,275.
