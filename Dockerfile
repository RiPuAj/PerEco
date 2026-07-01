# Stage 1: build dependencies
FROM python:3.13-slim AS builder

COPY requirements.txt .
RUN pip install --no-cache-dir --user --no-warn-script-location \
    -r requirements.txt

# Stage 2: runtime
FROM python:3.13-slim

RUN addgroup --system --gid 1000 app && \
    adduser --system --uid 1000 --gid 1000 app

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY --chown=app:app . .

RUN chmod +x entrypoint.sh && \
    python -m compileall -q . && \
    rm -rf __pycache__ */__pycache__

USER app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
