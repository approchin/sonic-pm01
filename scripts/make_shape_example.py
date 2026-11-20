"""Create synthetic arrays for the documented neural-network shape check.

These inputs are not a physical reference motion or a standing command.
No dataset, simulator, GPU, or robot connection is used.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    np.save(args.output / "actor_obs.npy", np.zeros((1, 789), dtype=np.float32))
    tokenizer = np.zeros((1, 541), dtype=np.float32)
    tokenizer[:, 0] = 1.0  # Canonical single robot-reference route selector.
    np.save(args.output / "tokenizer.npy", tokenizer)
    print("Synthetic shape-check inputs created; they are not robot commands.")


if __name__ == "__main__":
    main()
