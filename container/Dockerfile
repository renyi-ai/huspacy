FROM nvidia/cuda:11.1.1-devel-ubuntu20.04
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

RUN mkdir /installation
COPY ./ /installation/

RUN cd /installation/$MODEL && poetry install

RUN cd /installation/$MODEL && poetry run python -m pip install torch==1.10.2+cu111 -f https://download.pytorch.org/whl/torch_stable.html
RUN cd /installation/$MODEL && poetry run pip install -U pip setuptools wheel

RUN chmod -R 777 /installation

# Inserting the script into the Dockerfile
RUN echo '#!/bin/bash' > /run_spacy_commands.sh \
    && echo 'cd /installation/${MODEL}' >> /run_spacy_commands.sh \
    && echo 'poetry run spacy project assets' >> /run_spacy_commands.sh \
    && echo 'poetry run spacy project run all' >> /run_spacy_commands.sh \
    && chmod +x /run_spacy_commands.sh \
    && chmod -R 777 /installation

WORKDIR /workspace

COPY container/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT ["/entry.sh"]