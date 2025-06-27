# if-comp-grafica
Algoritmos desenvolvidos na disciplina de computação gráfica utilizando python 3.12

## Setup

- Utilize python 3.12
- Crie um ambiente virtual, por exemplo `python3 -m venv .venv`
- Ative o ambiente no terminal, por exemplo `source .venv/bin/activate` (se estiver no linux) ou `.venv\Scripts\Activate.ps1` (se estiver no windows)
- instale as dependências com pip usando `pip install -r requirements`

> O necessário é o `numpy` e `matplotlib`, mas o `pytest` e `pytest-cov` são interessantes pra fazer testes rápidos

## Utilização

- Você pode executar os scripts com: `python -m src.scenes.teste_3d`, por exemplo;
- Você pode executar os testes com: `pytest -v --cov=src --cov-report xml:coverage.xml` (ou simplesmente `pytest`, vale conferir a documentação para ver quais parâmetros se pode usar)
