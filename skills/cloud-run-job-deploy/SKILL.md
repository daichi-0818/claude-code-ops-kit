---
name: cloud-run-job-deploy
description: Deploy procedure for Cloud Run Jobs (batch / scheduled workloads) — fires on "deploy the job", "jobs update", "ship the batch job". Assumes the generic pre-deploy gate already passed; adds the job-specific steps that prevent silent batch failures.
---
# Cloud Run Job Deploy

Run the generic `pre-deploy` gates first. Then:

## Principles
- **One job per deploy.**
- **Build from merged main**, not from a feature branch.
- **Image-only updates**: pass `--image` and nothing else, so existing env
  vars and secrets survive.

## Steps

### 1. Record the rollback target (first, always)
```sh
gcloud run jobs describe <JOB> --region=<REGION> --project=<PROJECT> \
  --format="value(spec.template.spec.template.spec.containers[0].image)"
```
Write the old image sha down before touching anything.

### 2. Build
Build from the merge commit. Confirm the build reports SUCCESS and the image
tag is the sha you intended.

### 3. Update (image only)
```sh
gcloud run jobs update <JOB> --region=<REGION> --project=<PROJECT> \
  --image=<AR_PATH>/<IMAGE>:<SHA>
```
Immediately `describe` again: new sha in place, env-var count unchanged.

### 4. Verify by execution — and read the logs
```sh
gcloud run jobs execute <JOB> --region=<REGION> --project=<PROJECT> --wait
```
`succeededCount=1` is not enough: **exit 0 with an empty run is a real
failure mode.** Read the execution logs and find positive evidence the work
actually happened ("export finished", row counts written, …).

### 5. Register in monitoring
Scheduler registration is not monitoring. If the job is not added to
whatever watches your jobs, it can fail silently for weeks. Add it now, in
the same change — not "later".

### 6. Timeout vs. trigger interval
Check: expected runtime < `timeoutSeconds` < trigger interval (with margin).
When runtime exceeds the interval, executions overlap and failures hide
behind the "latest execution".

## Rollback
```sh
gcloud run jobs update <JOB> --region=<REGION> --project=<PROJECT> \
  --image=<the image recorded in step 1>
```

## Afterwards
Log the deploy (job, old/new sha, verification evidence). For
incident-driven changes, watch the next scheduled execution complete once.
