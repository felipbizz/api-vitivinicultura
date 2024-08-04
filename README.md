# API EMBRAPA - Vitivinicultura

Esse projeto contém uma API que entrega os dados fornecidos em http://vitibrasil.cnpuv.embrapa.br/

## Recursos
- **FastAPI**: Framework de alta performance utilizado para construção da API.
- **Testes**: Conjunto de testes unitários utilizando `pytest`.
- **Formatação**: Aplicação e formatação de estilo de código com `ruff`.

## Primeiros passos
Para começar nesse projeto, siga as instruções abaixo:

### Pré-requisitos
A versão python utilizada nesse projeto foi a 3.12. Para verificar a sua versão você pode checar através de:
```bash
python --version
```

## Instalação
Clone o repositório com:
```bash
git clone https://github.com/felibbizz/api-vitivinicultura.git
cd api-vitivinicultura
```

### Instale as dependências:
Se você não tem o poetry instalado, instale com:
```bash
pipx install poetry
```

Então, instale as dependências do projeto que estão em `pyproject.toml` através do comando:
```bash
poetry install
```

## Desenvolvimento
Esse projeto utiliza o ambiente de desenvolvimento do poetry. 
Para entrar no ambiente, rode o comando:
```bash
poetry shell
```

### Gerenciamento de tarefas:
Esse projeto utiliza o [Taskipy](https://github.com/taskipy/taskipy) para gerenciar as tarefas. 
Aqui estão alguns comandos úteis:

#### Rodar os testes: 
Para rodar os testes unitários com o [PyTest](https://docs.pytest.org/en/stable/) utilize:
```bash
task test
```

#### Formatar o código: 
Para formatar o código com [Ruff](https://docs.astral.sh/ruff/), utilize:
```bash
task format
```

#### Iniciar a aplicação: 
Para iniciar o server em modo de desenvolvimento, utilize:
```bash
task run
```

## Documentação:
- Swagger: https://localhost:8000/docs
- Documentação no padrão [Redoc](https://github.com/Redocly/redoc): https://localhost:8000/redoc

## License
