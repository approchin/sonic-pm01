# Model weights

Download a checkpoint ZIP from [SONIC-PM01 v0.1.0](https://github.com/approchin/sonic-pm01/releases/tag/v0.1.0). Extract it at the repository root so the `weights/` directory is available to the examples. Verify the archive against `SHA256SUMS.txt` from the release.

| Checkpoint | Actor adaptation | Intended use |
|---|---|---|
| `a_step_028000` | Decoder | Later checkpoint |
| `b_step_028000` | Encoder and decoder | Later checkpoint |
| `a_step_004000` | Decoder | Early compute milestone |
| `b_step_004000` | Encoder and decoder | Early compute milestone |

Each checkpoint contains `actor_mean23.onnx`, `actor_mean23.safetensors`, `config.json`, and `manifest.json`. The manifest records SHA-256 digests for the binary files. Keep the `weights/` layout so the shared input and control contracts remain next to the checkpoint folders.

The weights carry the NVIDIA Open Model License. The archives include the model licence and required attribution. See [licensing](licensing.md).

**Training data includes Motion Data by [Bones Studio](https://bones.studio/). Use of the underlying dataset is subject to the BONES Motion Capture Dataset License Agreement.**
