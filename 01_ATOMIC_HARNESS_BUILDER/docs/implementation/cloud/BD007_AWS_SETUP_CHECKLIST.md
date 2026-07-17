# BD-007 AWS Setup Checklist

Status: `NOT_CONFIGURED_NOT_AUTHENTICATED`  
Purpose: later ST-06.03 development-only BD-007 execution

No AWS authentication or resource operation is authorized by this checklist.

## Account and region

- [ ] Install or upgrade an operator-approved AWS CLI.
- [ ] Configure a named, operator-controlled profile without committing credentials.
- [ ] Record `sts get-caller-identity` account and principal evidence.
- [ ] Select one region and bind it to the execution approval.
- [ ] Confirm SageMaker, S3, ECR, KMS, VPC, CloudWatch, Service Quotas, and budget
      services are available to that account and region.

## Least-privileged identities

- [ ] Create or identify a deployment identity limited to required model, endpoint,
      registry, storage, quota-read, metric, and teardown actions.
- [ ] Create a SageMaker execution role that can read only the exact versioned model
      prefix and exact ECR image digest, write only required health/metrics, and use
      the selected KMS keys.
- [ ] Prohibit administrator policies, arbitrary S3 access, arbitrary ECR access,
      pass-role outside the exact execution role, and unrelated workspace access.

## Immutable artifacts

- [ ] Create an encrypted, versioned S3 location for the revision-pinned model bytes.
- [ ] Mirror and verify all model objects against the final model-file manifest.
- [ ] Create an encrypted ECR repository and push the container by digest.
- [ ] Record base-image, dependency lock, final image, model manifest, and S3 version
      identities before endpoint creation.

## Compute and quota

- [ ] Query current regional SageMaker GPU endpoint quotas.
- [ ] Inventory only FP8-capable configurations with at least the governed aggregate
      VRAM starting floor.
- [ ] Confirm quota for exactly one endpoint and its tensor-parallel GPU count.
- [ ] Run model-load, health, maximum-request, and concurrency qualification before
      semantic trials; theoretical capacity is insufficient.

## Network and encryption

- [ ] Use private subnets and security groups with no public unauthenticated endpoint.
- [ ] Create narrowly scoped VPC endpoints for required AWS control, S3, ECR, logs,
      and metrics traffic.
- [ ] Block arbitrary internet egress during semantic trials.
- [ ] Require TLS in transit and KMS encryption for model, evidence, logs, and endpoint
      volumes.
- [ ] Ensure prompts, corpus excerpts, and outputs are absent from default access logs.

## Budget and execution gate

- [ ] Retrieve current authenticated regional pricing for storage, transfer, ECR,
      build, endpoint startup, GPU runtime, logs, and KMS.
- [ ] Bind the dated estimate to the USD 40 soft stop, USD 50 hard cap, one endpoint,
      and 180-minute maximum lifetime.
- [ ] Create a bounded budget/alarm and a pre-call committed-cost check.
- [ ] Obtain explicit execution authorization after every prerequisite validates.

## Teardown

- [ ] Delete the endpoint immediately after the experiment or on any stop condition.
- [ ] Delete endpoint configurations and temporary build resources.
- [ ] Retain only approved versioned model/container artifacts and encrypted evidence.
- [ ] Record every remaining resource, endpoint uptime, and actual cost.

Current blockers: no visible AWS profile, credentials, selected region, authenticated
identity, quota evidence, pricing evidence, IAM role, storage, registry, or endpoint.
