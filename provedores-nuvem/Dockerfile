FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/root/.local/bin:/opt/sdkman/candidates/springboot/current/bin:/usr/local/bin:${PATH}" \
    CLOUDSDK_CORE_DISABLE_PROMPTS=1 \
    CLOUDSDK_PYTHON=python3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl gnupg unzip tar git python3 python3-venv \
       zip less groff openjdk-21-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/install-cli.sh /usr/local/bin/install-cloud-cli
RUN chmod 0755 /usr/local/bin/install-cloud-cli \
    && for provider in aws azure gcp heroku oci openshift spring-cloud; do \
         install-cloud-cli "$provider"; \
       done \
    && useradd --create-home --uid 10001 --shell /bin/bash toolbox

ENV HOME=/home/toolbox \
    PATH="/home/toolbox/.local/bin:/opt/sdkman/candidates/springboot/current/bin:/usr/local/bin:${PATH}"
USER 10001:10001
WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
