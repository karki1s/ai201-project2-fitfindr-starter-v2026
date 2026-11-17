# FitFindr in a container.
#
#   docker build -t fitfindr .
#   docker run --rm --env-file .env fitfindr python app.py ask 'vintage graphic tee under $30'
#   docker run --rm --env-file .env -p 5000:5000 fitfindr        # HTTP server (serve.py)
#
# 3.13 matches the local venv; requirements.txt says 3.11–3.13, not 3.14.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install deps first so code changes don't invalidate this layer.
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Don't run as root.
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

# Default: the HTTP server, the way a host would run it. Sync worker and one
# worker on purpose — see the note above _one_at_a_time in serve.py.
# Override the command to use the CLI instead (see top of file).
CMD ["sh", "-c", "gunicorn --workers 1 --bind 0.0.0.0:${PORT:-5000} serve:app"]
