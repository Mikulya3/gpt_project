FROM python:3.12-slim AS builder
ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
WORKDIR /app


RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential curl git \
&& rm -rf /var/lib/apt/lists/*
RUN python -m pip install --upgrade pip wheel setuptools \
&& pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes -vvv
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ---- runtime ----
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PORT=8000
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
&& rm -rf /wheels


COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
