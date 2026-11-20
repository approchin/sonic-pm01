#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run the CPU inference CLI directly from a source checkout."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pm01_sonic_inference.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
