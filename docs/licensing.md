# Licences and attribution

Source code and model weights carry separate licences and attribution.

## Model exports

The candidates derive from the released NVIDIA GEAR-SONIC G1 model. The upstream model terms are the **NVIDIA Open Model License**, retained with the model package. Preserve its agreement and required attribution when distributing derivatives:

> Licensed by NVIDIA Corporation under the NVIDIA Open Model License.

Source: [pinned SONIC licence](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/087f9ac01d46f6d8e4d0b73c01ae64799f292a38/LICENSE). The root model-package `LICENSE` contains the model agreement. Intended use for these research candidates is non-commercial scientific research and evaluation. This note does not establish unrestricted commercial-use permission from every source.

## Inference code

The standalone actor reconstruction is packaged separately from the historical training environment. Preserve the module-level provenance and notices under `src/pm01_sonic_inference/notices/`. SONIC source components use Apache-2.0; the active FSQ implementation also retains the vector-quantize-pytorch/MIT attribution. The standalone inference packaging is released under Apache-2.0. The model weights retain the NVIDIA Open Model License.

The original training checkout contained concrete changes from the public Any2Any SONIC-to-Oli example. The public deterministic inference package does not require that checkout. Acknowledging an adaptation idea is distinct from recording the origin of copied implementation files. This release does not redistribute an unreviewed copy of the whole historical training repository.

## Robot assets

EngineAI's robot-model and SDK source repositories have their own notices. The visualization model comes from the native SDK; its original 2025 Shenzhen Zhongqing Robot Technology Co., Ltd. (EngineAI) notice is in `licenses/ENGINEAI-NATIVE-SDK-BSD-3-CLAUSE.txt`. The distinct RL Lab 2026 engineai-robotics notice is retained separately in `licenses/ENGINEAI-RL-LAB-BSD-3-CLAUSE.txt`. The raw robot asset tree is not mirrored here. Videos use the PM01 model for visualization; preserve the manufacturer attribution and notices alongside distributed media.

Sources: [EngineAI RL Lab](https://github.com/engineai-robotics/engineai_rl_lab), [EngineAI native SDK](https://github.com/engineai-robotics/engineai_robotics_native_sdk).

## Motion data and media

The project owner confirmed use for school/research-institution non-commercial research. Under the [BONES-SEED Dataset License Agreement](https://bones.studio/info/seed-license), results include models, rendered animations and statistical findings; eligible users' result display and ownership remain subject to the agreement, raw-data restrictions and attribution requirements. We do not distribute the raw BONES dataset, its retargeted motion libraries, or the private numerical-validation observation cohort.

**Training data includes Motion Data by [Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.**

Other source datasets retain separate terms. In particular, the [LAFAN1 repository](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) identifies CC BY-NC-ND 4.0. The release reports aggregate LAFAN1 body-tracking results.

## CMU source-data credit

CMU motion capture data: [mocap.cs.cmu.edu](https://mocap.cs.cmu.edu/). The source database was created with funding from NSF EIA-0196217. This acknowledges the data source and does not state that the present project received that grant.

## Evaluation-source credit

OMOMO evaluation data originate from [Li, Wu and Liu's official OMOMO project](https://lijiaman.github.io/projects/omomo/) and [omomo_release](https://github.com/lijiaman/omomo_release). Only body-tracking statistics are reported here; no object dynamics, raw motion files or OMOMO-derived demo videos are distributed. LAFAN1 evaluation data originate from [Ubisoft La Forge](https://github.com/ubisoft/ubisoft-laforge-animation-dataset), with its separate source terms and citation retained.
