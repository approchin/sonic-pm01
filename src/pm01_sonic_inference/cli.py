# SPDX-License-Identifier: Apache-2.0
"""Command line interface for raw 23-dimensional CPU Actor inference."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .runtime import ActorCPU


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="Local actor_mean23.onnx file")
    parser.add_argument("--actor-obs", type=Path, required=True, help="Float32 NPY, shape (N,789), with native packed history/feedback")
    reference = parser.add_mutually_exclusive_group(required=True)
    reference.add_argument("--reference", type=Path, help="Float32 NPY, shape (N,540): q240 | qd240 | orientation60")
    reference.add_argument("--tokenizer", type=Path, help="Float32 NPY, shape (N,541): selector1 followed by reference540")
    parser.add_argument("--output", type=Path, required=True, help="New NPY file for raw float32 (N,23) means; no actuation")
    args = parser.parse_args()
    if args.output.suffix != ".npy":
        parser.error("--output must end with .npy")
    actor_obs = np.load(args.actor_obs, allow_pickle=False)
    actor = ActorCPU(args.model)
    if args.reference is not None:
        means = actor.predict(actor_obs, np.load(args.reference, allow_pickle=False))
    else:
        means = actor.predict_packed(actor_obs, np.load(args.tokenizer, allow_pickle=False))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as handle:
        np.save(handle, means, allow_pickle=False)
    print(json.dumps({"provider": "CPUExecutionProvider", "rows": len(means), "output_features": 23,
                      "output": str(args.output), "robot_connection": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
