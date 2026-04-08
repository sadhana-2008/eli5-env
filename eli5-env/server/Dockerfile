FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn huggingface_hub httpx tqdm filelock fsspec packaging pyyaml typer

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]