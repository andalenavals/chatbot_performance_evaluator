FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OLLAMA_HOST=127.0.0.1:11434 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY pyproject.toml README.md ./
COPY src ./src
COPY app ./app
COPY configs ./configs
COPY data ./data
COPY examples ./examples

RUN pip install --upgrade pip \
    && pip install -e .

COPY deploy/huggingface/start.sh /usr/local/bin/start-space
RUN chmod +x /usr/local/bin/start-space

EXPOSE 7860

CMD ["start-space"]
