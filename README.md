# SONIC-PM01

**An independent research adaptation of NVIDIA GEAR-SONIC for EngineAI PM01.**

[中文说明](README.zh-CN.md) · [Architecture](docs/architecture.md) · [Evaluation](docs/evaluation.md) · [Training recipe](docs/training_recipe.md) · [Scope and limitations](docs/limitations.md)

This repository contains the standalone PM01 Actor inference code, model input and output contracts, and simulation results. The [weights and usage instructions](docs/weights.md) cover both A/B variants at 4,000 and 28,000 PPO updates.

## What the adaptation does

The active SONIC motion encoder, fixed FSQ token representation, and control decoder are adapted to PM01's native interface by folding fixed coordinate maps into the boundary linear layers. Two dense update scopes are compared:

| Variant | Reference encoder | Control decoder | Training critic |
|---|---|---|---|
| A | Frozen | Updated | Updated |
| B | Updated | Updated | Updated |

Both actors were trained, with no LoRA layers in these A/B models. The inference export outputs 23 body-action means. A separate reference-PD path handles PM01's head. The critic and optimizer are training components and are not part of the exported actor.

See the [three architecture diagrams](docs/architecture.md) for training, actor and critic details. The packaged standalone inference code does not import the historical training checkout or its Any2Any fork.

## Checkpoints and evidence

The [model files](docs/weights.md) cover four checkpoints: `a_step_004000`, `b_step_004000`, `a_step_028000`, and `b_step_028000`. Each has `actor_mean23.onnx`, `actor_mean23.safetensors`, `config.json`, and `manifest.json`.

The 4k models are the budget milestones: approximately 6.514 / 6.712 RTX 4090 training-process GPU hours for A / B, including their parent stage but excluding source SONIC pretraining, evaluation, data preparation and idle time. The 28k models are later checkpoints with lower tracking errors on the same mixed test. These are per-variant training figures, not the combined project cost.

| Fixed simulation test | A 4k | B 4k | A 28k | B 28k |
|---|---:|---:|---:|---:|
| OMOMO394 + LAFAN106 | 485/500 (97.0%) | 483/500 (96.6%) | 485/500 (97.0%) | 485/500 (97.0%) |
| BONES500 | 498/500 (99.6%) | 498/500 (99.6%) | 498/500 (99.6%) | 498/500 (99.6%) |

Completion is reaching the end of a reference under the declared local height/orientation rules; it is not a tracking-accuracy percentage. Each fixed test uses seed 42 and a first-frame reset. Test recordings were excluded from PM01 adaptation, but some action families overlap, these populations were previously evaluated, and source SONIC pretraining overlap is unknown. These are PM01 PhysX results, not the official Any2Any benchmark or hardware trials. Full error metrics, denominators, scoring details and historical checkpoint comparisons are in [evaluation.md](docs/evaluation.md) and [aggregate_results.json](evidence/aggregate_results.json).

## CPU inference example

The public package supports **already packed observations**. Its fixed-batch interface is `actor_obs: float32[1,789]`, `tokenizer: float32[1,541]` → `mean23: float32[1,23]`. The output is a raw action mean, not a torque or absolute joint angle. Packing, joint order and postprocessing must follow the model contract.

```bash
python -m pip install -r requirements-inference.txt
python scripts/make_shape_example.py --output example_inputs
python scripts/infer_cpu.py \
  --model weights/a_step_028000/actor_mean23.onnx \
  --actor-obs example_inputs/actor_obs.npy \
  --tokenizer example_inputs/tokenizer.npy \
  --output example_inputs/mean23.npy
```

Extract or download the selected checkpoint as described in [Model weights](docs/weights.md), then pass its `actor_mean23.onnx` path. The generated inputs are synthetic shape checks only, not a standing or locomotion command. No robot connection is opened. Numerical export checks use a separate private cohort of 439 historical simulation-observation rows and 256 synthetic inputs.

The tensor-only PyTorch loader is in `src/pm01_sonic_inference/`. Actor exports intentionally omit full training state; they are not strict optimizer/sampler/RNG resume checkpoints.

## Data, licences and attribution

Built on [NVIDIA GEAR-SONIC](https://nvlabs.github.io/GEAR-SONIC/), with adaptation ideas informed by [Any2Any](https://any2any.top/), for [EngineAI PM01](https://github.com/engineai-robotics/engineai_robotics_native_sdk).

**Training data includes Motion Data by [Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the [BONES Motion Capture Dataset License Agreement](https://bones.studio/info/seed-license).** The project owner identifies this work as school/research-institution non-commercial research. Model files, code, robot assets and motion data have separate terms; see [licensing.md](docs/licensing.md) and the retained notices. No raw motion libraries or observation cohorts are included in this package.

See [limitations.md](docs/limitations.md) for the tested scope.

CMU training-data credit: [mocap.cs.cmu.edu](https://mocap.cs.cmu.edu/). The source database was created with funding from NSF EIA-0196217.
