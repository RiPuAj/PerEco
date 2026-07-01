FROM python:3.13-slim

RUN addgroup --system --gid 1000 app && \
    adduser --system --uid 1000 --gid 1000 app && \
    pip install --no-cache-dir django gunicorn whitenoise

WORKDIR /app

COPY --chown=app:app . .

RUN mkdir -p /app/data /app/staticfiles && \
    chown -R app:app /app && \
    chmod +x entrypoint.sh && \
    python -m compileall -q . && \
    rm -rf __pycache__ */__pycache__

ENV HOME=/app

USER app

EXPOSE 8888

ENTRYPOINT ["/app/entrypoint.sh"]
