# ADR-0001: Compose local stack and Kubernetes manifests

## Status
Accepted

## Date
2026-09-24

## Context

The repository describes a platform with GitLab, Jenkins, SonarQube, PostgreSQL, Grafana, an OpenTelemetry Collector, a REST backend, and Angular/React frontends. It currently contains documentation only; the backend and frontends have no source code, build tool, startup command, health endpoint, or image to deploy. No registry, cluster, ingress controller, storage class, or production sizing has been selected.

## Decision

Provide a Docker Compose stack for local evaluation and Kubernetes base manifests for the six documented infrastructure services that have usable upstream container images. Keep backend and frontend deployment out until their source code and runtime contracts exist. Pin upstream image versions where available. Keep local secrets in an ignored `.env`; Kubernetes credentials are supplied separately, not committed as Secret manifests. Configure the Collector to receive OTLP and emit received telemetry through its debug exporter, because no telemetry storage backend is selected.

## Alternatives Considered

### Compose only

Simpler for a local reference environment, but it would not meet the requested Kubernetes deployment target.

### Kubernetes only

Would require a target cluster and would make local evaluation less accessible.

### Invent backend and frontend implementations

Would create runtime and health-check assumptions unsupported by the repository's documentation.

## Consequences

- Compose is intended for local evaluation, not production sizing or security hardening.
- GitLab and Jenkins require substantial persistent storage; Kubernetes PVC sizes and resource requests are starting points that must be adjusted for a real cluster.
- A cluster must provide a default StorageClass or users must set one explicitly.
- The Collector currently logs telemetry for inspection; Grafana has no metrics or trace backend configured.
- The backend and frontend README files must be supplemented with real code, build instructions, ports, probes, and image names before those workloads can be deployed.
- Image versions need deliberate updates after checking each upstream project's compatibility and upgrade guidance.
