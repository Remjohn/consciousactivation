# BD-007 Google Cloud Setup Checklist

Status: `NOT_CONFIGURED_NOT_AUTHENTICATED`  
Purpose: later ST-06.03 development-only BD-007 execution

No Google Cloud authentication or resource operation is authorized by this checklist.

## Project and region

- [ ] Install an operator-approved Google Cloud CLI.
- [ ] Authenticate through an operator-controlled identity without committing
      credentials.
- [ ] Select and record the exact project, billing account, region, and identity.
- [ ] Confirm Vertex AI, Cloud Storage, Artifact Registry, Cloud Build, Compute Engine,
      Cloud KMS, Logging, Monitoring, Quotas, and Budgets are enabled and available.

## Least-privileged identities

- [ ] Create or identify a deployment identity limited to required build, registry,
      storage, model, endpoint, quota-read, metric, and teardown actions.
- [ ] Create a Vertex serving service account that can read only the exact versioned
      model prefix and exact Artifact Registry image digest.
- [ ] Create a Builder invocation identity limited to the selected endpoint and exact
      encrypted evidence prefix.
- [ ] Prohibit Owner/Editor grants, arbitrary bucket access, arbitrary registry access,
      and unrelated repository access.

## Immutable artifacts

- [ ] Create an encrypted, versioned Cloud Storage location for the pinned model bytes.
- [ ] Mirror and verify every object against the final model-file manifest.
- [ ] Create an Artifact Registry repository and store the container by digest.
- [ ] Record base-image, dependency lock, final image, model manifest, and object
      generation identities before model upload or endpoint deployment.

## Compute and quota

- [ ] Query current Vertex/Compute GPU accelerator availability and project quotas in
      the selected region.
- [ ] Inventory only FP8-capable configurations with at least the governed aggregate
      VRAM starting floor.
- [ ] Confirm quota for exactly one endpoint and its tensor-parallel GPU count.
- [ ] Run model-load, startup probe, health, maximum-request, and concurrency
      qualification before semantic trials.

## Network and encryption

- [ ] Use a private endpoint or approved private network path; prohibit unauthenticated
      public invocation.
- [ ] Restrict egress to required Google APIs and internal control traffic, then remove
      bootstrap model-download access before semantic trials.
- [ ] Require TLS in transit and customer-approved encryption for model, evidence,
      registry, logs, and endpoint storage.
- [ ] Ensure prompts, corpus excerpts, and outputs are absent from default access logs.

## Budget and execution gate

- [ ] Retrieve current authenticated regional pricing for storage, transfer, Artifact
      Registry, Cloud Build, endpoint startup, GPU runtime, logs, and KMS.
- [ ] Bind the dated estimate to the USD 40 soft stop, USD 50 hard cap, one endpoint,
      and 180-minute maximum lifetime.
- [ ] Create a bounded budget/alert and a pre-call committed-cost check.
- [ ] Obtain explicit execution authorization after every prerequisite validates.

## Teardown

- [ ] Undeploy and delete the endpoint immediately after the experiment or stop.
- [ ] Delete unused deployed-model resources and temporary build resources.
- [ ] Retain only approved versioned model/container artifacts and encrypted evidence.
- [ ] Record every remaining resource, endpoint uptime, and actual cost.

Current blockers: `gcloud` is unavailable and there is no authenticated account,
project, region, quota evidence, service account, pricing evidence, storage, registry,
build, model, or endpoint.
