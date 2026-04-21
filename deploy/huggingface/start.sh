#!/usr/bin/env bash
set -euo pipefail

export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
export OLLAMA_MODELS="${OLLAMA_MODELS:-/data/ollama/models}"
export SPACE_OLLAMA_MODELS="${SPACE_OLLAMA_MODELS:-deepseek-r1:latest qwen3:8b}"
export PYTHONPATH="/app:/app/src${PYTHONPATH:+:${PYTHONPATH}}"

mkdir -p "${OLLAMA_MODELS}"

ollama serve > /tmp/ollama.log 2>&1 &
OLLAMA_PID="$!"

cleanup() {
  kill "${OLLAMA_PID}" 2>/dev/null || true
}
trap cleanup EXIT

echo "Waiting for Ollama at ${OLLAMA_HOST}..."
for _ in $(seq 1 60); do
  if curl -fsS "http://${OLLAMA_HOST}/api/tags" >/dev/null; then
    break
  fi
  sleep 1
done

if ! curl -fsS "http://${OLLAMA_HOST}/api/tags" >/dev/null; then
  echo "Ollama did not become ready. Recent Ollama logs:"
  tail -100 /tmp/ollama.log || true
  exit 1
fi

for model in ${SPACE_OLLAMA_MODELS}; do
  echo "Ensuring Ollama model is available: ${model}"
  ollama pull "${model}"
done

exec streamlit run app/main.py \
  --server.address=0.0.0.0 \
  --server.port="${PORT:-7860}" \
  --server.headless=true
