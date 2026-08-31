FROM jenkins/jenkins:lts-jdk21

USER root

ARG DOCKER_GID=986

RUN apt-get update \
    && apt-get install -y \
        ca-certificates \
        curl \
        git \
        openssh-client \
        docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN if getent group docker; then \
        groupmod -g ${DOCKER_GID} docker; \
    else \
        groupadd -g ${DOCKER_GID} docker; \
    fi \
    && usermod -aG docker jenkins

USER jenkins