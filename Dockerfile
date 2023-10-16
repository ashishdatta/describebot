FROM python:3.10
RUN pip install poetry
WORKDIR /code
COPY poetry.lock pyproject.toml describebot/bot.py /code/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . /code
CMD python bot.py
