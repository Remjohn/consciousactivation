# Local GPU Proof

Classification: `non_production_readiness_proof`  
Assessment date: 2026-07-15  
Verdict: **FAIL — Docker GPU runtime not executable**

The fresh probe observed an NVIDIA GeForce GTX 960M, driver `576.02`, 2048 MiB total VRAM and 2002 MiB free. Docker client `28.3.3` and context `desktop-linux` are installed. Docker Desktop was started for the bounded retry. The sandbox probe could not access the named pipe; the escalated daemon probe reached Docker Desktop but received HTTP 500 for `/v1.51/info`.

Consequently no GPU container could start. There is no verified container digest, ComfyUI version, custom-node lockfile, model/VAE/LoRA hashes, compiled workflow hash, API request/response, execution-event stream, GPU-produced candidate, deterministic production receipt, GPU latency or execution cost. Actual execution cost was `$0.00` because no workload ran.

The controlled SVG candidates in the Format 02 fixture proof are not ComfyUI or GPU output and do not close this gate.
