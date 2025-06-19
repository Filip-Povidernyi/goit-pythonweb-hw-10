FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false && poetry install --without dev

RUN poetry show

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]