FROM python:3.10-slim

RUN python3 --version

# necessary for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

RUN pip install poetry
WORKDIR /app
ENV PYTHONPATH=/app

COPY . .

RUN poetry install --no-root

RUN ls
EXPOSE 8000

CMD ["poetry", "run", "python", "backend/app/main.py"]