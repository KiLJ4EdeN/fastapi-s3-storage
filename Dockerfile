# Dockerfile
FROM python:3.9-slim-bullseye

ENV APP_WORKERS 4

# Keep the apt cache
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' | tee /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/list/apt,sharing=locked \
    apt update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gcc

# We copy our Python requirements here to cache them
COPY . /code
WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/pip,sharing=locked \
    pip install -r requirements.txt


# FastAPI App Port
EXPOSE 8000


ENTRYPOINT [ "/bin/bash", "/code/entrypoint.sh"]
