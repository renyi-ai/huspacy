FROM nvidia/cuda:11.2.2-devel-ubuntu20.04
ARG MODEL

ENV PYTHONPATH=/workspace

# Install some basic apt packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qy \
    sudo vim nano git curl wget mc less \
    python3-pip openssh-server && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

RUN echo "%docker  ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/inside_sudoers

# Ensure that pip, setuptools, and wheel are up to date
RUN python3 -m pip install --upgrade pip setuptools wheel

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN mkdir /install
WORKDIR /install

COPY ./$MODEL/pyproject.toml ./$MODEL/poetry.lock ./

RUN touch README.md

RUN poetry install --no-root

RUN poetry run python -m pip install torch==1.10.2+cu111 -f https://download.pytorch.org/whl/torch_stable.html
RUN poetry run pip install -U pip setuptools wheel

# Inserting the script into the Dockerfile
RUN echo '#!/bin/bash' > /run_spacy_commands.sh \
    && echo "cd /workspace/$MODEL" >> /run_spacy_commands.sh \
    && echo "source /install/.venv/bin/activate" >> /run_spacy_commands.sh \
    && echo 'spacy project assets' >> /run_spacy_commands.sh \
    && echo 'spacy project run all' >> /run_spacy_commands.sh \
    && chmod +x /run_spacy_commands.sh \

RUN echo "source /install/.venv/bin/activate" >> /activate.sh \
    && chmod +x /activate.sh

WORKDIR /workspace/$MODEL

COPY container/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT ["/entry.sh"]