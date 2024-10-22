FROM python:3.12-slim

RUN pip install uv
RUN --mount=source=dist,target=/dist uv pip install --no-cache --system /dist/*.whl 

COPY src/spam_detector/app.py /app/entrypoint.py
COPY src/spam_detector/models /app/models
WORKDIR /app

CMD ["sh", "-c", "fastapi run entrypoint.py --port $PORT"]
