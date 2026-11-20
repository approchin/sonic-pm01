# SPDX-License-Identifier: Apache-2.0
"""Packed-observation CPU inference; outputs raw body action means only.

No robot connection, action scaling, clipping, PD controller or sensor
preprocessing is implemented here. The caller supplies the documented native
observation layout, including its historical terms and current feedback.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import onnxruntime as ort


def _rows(value, width, name):
    array = np.asarray(value)
    if array.dtype != np.float32:
        raise ValueError(f"{name} must have dtype float32")
    if array.ndim == 1:
        array = array[None, :]
    if array.ndim != 2 or array.shape[1] != width or array.shape[0] < 1:
        raise ValueError(f"{name} must have shape (N, {width}) or ({width},)")
    if not np.isfinite(array).all():
        raise ValueError(f"{name} contains nonfinite values")
    return np.ascontiguousarray(array)


class ActorCPU:
    """Evaluate a fixed-batch-one ONNX graph sequentially on CPU.

    ``actor_obs`` has 789 values: omega30 | relative_q240 | relative_qd240 |
    raw_action_history240 | gravity30 | current_feedback9. Histories include
    all 24 native joints. ``reference`` has 540 values in stored order:
    all ten q frames240 | all ten qd frames240 | ten 6D orientations60.
    These are already packed model features, not raw sensor measurements.
    """

    def __init__(self, model_path):
        options = ort.SessionOptions()
        # Preserve the arithmetic path used for the released parity check.
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
        options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1
        self.session = ort.InferenceSession(
            str(Path(model_path)), sess_options=options, providers=["CPUExecutionProvider"]
        )
        self.session.disable_fallback()
        if self.session.get_providers() != ["CPUExecutionProvider"]:
            raise RuntimeError("The inference session did not select CPUExecutionProvider exclusively")
        actual = {item.name: (item.type, item.shape) for item in self.session.get_inputs()}
        expected = {"actor_obs": ("tensor(float)", [1, 789]), "tokenizer": ("tensor(float)", [1, 541])}
        if actual != expected:
            raise ValueError("ONNX inputs differ from the released native Actor contract")
        outputs = self.session.get_outputs()
        if len(outputs) != 1 or (outputs[0].name, outputs[0].type, outputs[0].shape) != (
            "mean23", "tensor(float)", [1, 23]
        ):
            raise ValueError("ONNX output must be float32 mean23 with shape (1, 23)")

    def predict(self, actor_obs, reference):
        reference = _rows(reference, 540, "reference")
        tokenizer = np.concatenate((np.ones((len(reference), 1), dtype=np.float32), reference), axis=1)
        return self.predict_packed(actor_obs, tokenizer)

    def predict_packed(self, actor_obs, tokenizer):
        actor_obs = _rows(actor_obs, 789, "actor_obs")
        tokenizer = _rows(tokenizer, 541, "tokenizer")
        if len(actor_obs) != len(tokenizer):
            raise ValueError("State and reference row counts differ")
        if not np.all(tokenizer[:, 0] == np.float32(1)):
            raise ValueError("The fixed G1 reference route requires selector1 in tokenizer[:, 0]")
        result = np.concatenate([
            self.session.run(["mean23"], {
                "actor_obs": actor_obs[index:index + 1], "tokenizer": tokenizer[index:index + 1]
            })[0] for index in range(len(actor_obs))
        ])
        if result.shape != (len(actor_obs), 23) or not np.isfinite(result).all():
            raise RuntimeError("The Actor returned invalid raw action means")
        return result
