# Dokploy Deployment Blueprint for Google Cloud or AWS

## Decision

Dokploy can manage the Conscious Activations deployment on Google Cloud, AWS, or a mixed
multi-server topology.

Dokploy owns deployment, domains, Docker services, logs, monitoring, backups, and
rollbacks. It does not own Atomic Harness campaigns or Workflow Node semantics.

## Recommended initial topology

```text
Dokploy manager
  small stable CPU VM
  Google Compute Engine or AWS EC2

Supabase
  managed Supabase project initially

Studio Web
  Next.js/React service

Studio API / Pipeline API
  Python service

Realtime and control records
  Supabase Postgres / Auth / Realtime / Storage / Queues

CPU workers
  Dokploy deployment servers

Remotion / HyperFrames / FFmpeg workers
  dedicated CPU/render servers

GPU workers
  GCP GPU VM, AWS GPU EC2, or other registered GPU provider
  connected through the Worker Registry and durable job queues

Artifact storage
  Supabase Storage initially or S3/GCS when volume and delivery require it

Container registry
  GHCR, Artifact Registry, ECR, or another explicit registry
```

## Dokploy use

- GitHub auto-deploy for applications and Docker Compose stacks.
- Remote deployment servers for workload isolation.
- Separate build servers when builds become resource-heavy.
- Docker registry for multi-server deployment.
- Scheduled backups to S3-compatible storage.
- Logs and monitoring per service.
- API, CLI, or MCP for deployment automation.

## Cloud choice

### Google Cloud

Good fit when:
- Vertex AI or GCP GPU workers will be used;
- GCS becomes the main artifact store;
- Cloud Run or Compute Engine workers are preferred.

### AWS

Good fit when:
- S3, ECR, EC2 GPU, ECS, or Lambda-adjacent services are preferred;
- the team wants broad instance and regional options.

### Mixed topology

Allowed:
- Dokploy manager on one provider;
- Supabase managed;
- CPU workers on the cheapest provider;
- GPU workers on whichever provider has capacity;
- artifacts in S3 or GCS.

All workers must register their exact capability and execution-stack identity with the
Studio control plane.

## Practical law

Use Dokploy to ship and operate containers.

Use Supabase to persist and synchronize Studio state.

Use the Atomic Harness Pipeline to run campaigns.
