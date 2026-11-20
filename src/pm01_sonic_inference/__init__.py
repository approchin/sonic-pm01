# SPDX-License-Identifier: Apache-2.0
"""CPU-only inference for packed SONIC-PM01 observations."""

__version__ = "0.1.0"


def load_cpu_actor(model_path):
    """Load an ONNX Actor with CPUExecutionProvider explicitly selected."""
    from .runtime import ActorCPU
    return ActorCPU(model_path)
