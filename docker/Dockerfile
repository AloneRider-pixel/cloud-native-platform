# syntax=docker/dockerfile:1
FROM python:3.14-slim

# Security: run as a dedicated non-root user.
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /usr/sbin/nologin appuser

WORKDIR /app
COPY app/main.py ./main.py

RUN chown -R appuser:appuser /app
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=3).read()" || exit 1

EXPOSE 8000
CMD ["python", "main.py"]
