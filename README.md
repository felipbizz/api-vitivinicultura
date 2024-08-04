# fiap-mle-tech-challenge
poetry run fastapi run app.py --host 127.0.0.1

# Para inserir a env do poetry no jupyter use
poetry config virtualenvs.in-project true

## Se o virtualenv do poetry já estiver criado, delete ele e crie novamente
poetry env list  # shows the name of the current environment
poetry env remove <current environment>
poetry install  # will create a new environment using your updated configuration

## Para obter o path da venv do poetry encontre em
poetry config virtualenvs.path