FROM python:3.9 AS base

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

FROM base AS final

COPY --from=base /app /app

EXPOSE 4012

CMD ["sh", "-c", "flask db upgrade && python run.py"]
