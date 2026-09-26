#!/usr/bin/env python3
"""Envia evento de deployment concluído para o endpoint SDLC da Dynatrace."""

import json
import os
import sys
import urllib.error
import urllib.request


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Variável obrigatória ausente: {name}")
    return value


environment_url = required("DT_ENVIRONMENT_URL").rstrip("/")
api_token = required("DT_API_TOKEN")
payload = {
    "event.type": "deployment",
    "event.status": "finished",
    "event.category": "task",
    "event.version": "0.1.0",
    "cicd.deployment.id": required("DT_DEPLOYMENT_ID"),
    "cicd.deployment.name": required("DT_DEPLOYMENT_NAME"),
    "cicd.deployment.release_stage": required("DT_RELEASE_STAGE"),
    "cicd.deployment.status": required("DT_DEPLOYMENT_STATUS"),
}

optional_fields = {
    "cicd.deployment.service.id": "DT_SERVICE_ID",
    "vcs.ref.base.revision": "DT_COMMIT_SHA",
    "vcs.repository.url.full": "DT_REPOSITORY_URL",
}
for field, variable in optional_fields.items():
    value = os.environ.get(variable, "").strip()
    if value:
        payload[field] = value

request = urllib.request.Request(
    f"{environment_url}/platform/ingest/v1/events.sdlc",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Api-Token {api_token}",
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 202:
            raise SystemExit(f"Dynatrace retornou HTTP {response.status}")
        print("Evento de deployment aceito pela Dynatrace (HTTP 202).")
except urllib.error.HTTPError as error:
    print(f"Falha ao enviar evento: HTTP {error.code}", file=sys.stderr)
    raise SystemExit(1) from error
except urllib.error.URLError as error:
    print(f"Falha de conexão com a Dynatrace: {error.reason}", file=sys.stderr)
    raise SystemExit(1) from error
