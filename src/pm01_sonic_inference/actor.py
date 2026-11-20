# SPDX-License-Identifier: Apache-2.0
# NativeFSQ adapts vector-quantize-pytorch by Phil Wang (lucidrains), MIT.
# See notices/ and MODULE_PROVENANCE.json for upstream attribution.
"""Deterministic SONIC-PM01 Actor reconstruction; no simulation or robot I/O.

This optional PyTorch module loads tensor-only safetensors weights on CPU.
The ONNX CPU inference CLI does not import PyTorch or this module.
"""
from __future__ import annotations

from pathlib import Path

import torch
from torch import nn


def _mlp(widths):
    layers = []
    for index, (left, right) in enumerate(zip(widths[:-1], widths[1:])):
        layers.append(nn.Linear(left, right))
        if index < len(widths) - 2:
            layers.append(nn.SiLU())
    return nn.Sequential(*layers)


class NativeFSQ(nn.Module):
    """Active FSQ 1.31.6 path, including FP32 arithmetic and round_ste order.

    Packed indices are unused by the native actor. They are intentionally absent.
    Keep Add/Sub around Round: replacing round_ste with round can change floats.
    """
    def __init__(self):
        super().__init__()
        self.register_buffer("_levels", torch.full((32,), 32, dtype=torch.int32), persistent=False)

    def forward(self, latent):
        original_dtype = latent.dtype
        float_latent = latent.float()
        half_l = (self._levels - 1) * (1 + 1e-3) / 2
        offset = torch.where(self._levels % 2 == 0, 0.5, 0.0)
        shift = torch.atanh(offset / half_l)
        bounded = torch.tanh(float_latent + shift) * half_l - offset
        rounded = bounded + (torch.round(bounded) - bounded).detach()
        return (rounded / (self._levels // 2)).to(original_dtype)


class StandaloneActor(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = _mlp([540, 2048, 1024, 512, 512, 64])
        self.fsq = NativeFSQ()
        self.decoder = _mlp([853, 2048, 2048, 1024, 1024, 512, 512, 23])

    @staticmethod
    def encoder_input(tokenizer):
        command = tokenizer[:, 1:481].reshape(-1, 10, 48)
        orientation = tokenizer[:, 481:541].reshape(-1, 10, 6)
        return torch.cat((command, orientation), dim=-1).flatten(1)

    def forward_debug(self, actor_obs, tokenizer):
        encoder_input = self.encoder_input(tokenizer)
        pre_fsq = self.encoder(encoder_input).reshape(-1, 2, 32)
        codes = self.fsq(pre_fsq).flatten(1)
        mean23 = self.decoder(torch.cat((codes, actor_obs), dim=-1))
        return encoder_input, pre_fsq.flatten(1), codes, mean23

    def forward(self, actor_obs, tokenizer):
        return self.forward_debug(actor_obs, tokenizer)[-1]

    @classmethod
    def from_safetensors(cls, path):
        from safetensors.torch import load_file
        model = cls()
        state = load_file(str(Path(path)), device="cpu")
        if any(value.dtype != torch.float32 for value in state.values()):
            raise ValueError("Actor weights must remain float32")
        model.load_state_dict(state, strict=True)
        return model.eval().requires_grad_(False)
