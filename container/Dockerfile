FROM nvcr.io/nvidia/pytorch:22.12-py3
ARG MODEL

ENV PYTHONPATH=/workspace

# Install some basic apt packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qy \
    sudo vim nano git curl wget mc less \
    openssh-server && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/*

RUN echo "%docker  ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/inside_sudoers

RUN pip install poetry

RUN mkdir /installation
COPY ./ /installation/

RUN echo /installation/${MODEL}

RUN cd /installation/$MODEL && \
    poetry install

RUN cd /installation/$MODEL && \
    poetry shell && \
    spacy project assets && \
    spacy project run all

WORKDIR /workspace

COPY container/entry.sh /entry.sh
RUN chmod +x /entry.sh
ENTRYPOINT ["/entry.sh"]