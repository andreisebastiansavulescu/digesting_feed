FROM python:3.11-slim

WORKDIR /app

COPY . .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv pip install . --system

# Generate a lockfile for reproducible installs
RUN uv pip lock > requirements.lock

CMD ["python", "-m", "digesting_feed.main"]
