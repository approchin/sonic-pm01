# Target adaptation recipe

The experiments start from a SONIC default G1 pretrained policy and adapt its active reference-encoder, FSQ and dynamics-decoder route to PM01. Fixed robot-coordinate and observation/action mappings are folded into the network boundaries before target adaptation. The target receives retargeted PM01 references. This is a native dense-parameter adaptation, **not LoRA**.

| Component | A: `decoder_only` | B: `full_actor` |
|---|---|---|
| Reference encoder | Frozen | Trainable |
| Dynamics decoder | Trainable | Trainable |
| Body action standard deviation | Trainable | Trainable |
| Critic | Fully trainable | Fully trainable |
| FSQ and coordinate bridge | Retained, fixed | Retained, fixed |

The actor generates 23 body-joint action targets. A separate reference-PD path controls the head; the critic is used during training and is not needed to generate a deployed action. No real-robot deployment or exported policy is established by this recipe.

## Data and training lineage

The original first stage trained each arm through global step 1,018 using 93 CMU reference motions. The migration to the expanded library preserved the learned model and training state while rebuilding the data sampler for the new library; the migration itself added no PPO updates. The expanded target-training library contains 3,950 motion references: 250 CMU and 3,700 BONES/SEED SOMA uniform references, about 8.0 hours of reference motion. A separate 25-clip CMU development set was repeatedly inspected during training. Reference duration is a data quantity, not GPU training time.

Step 4,000 therefore contains 1,018 earlier updates and 2,982 updates after the expanded-data migration. Step 28,000 contains 26,982 updates after that migration. A and B are separate training runs; they are not two GPUs cooperating on one policy.

## Saved configuration

The original target adaptation used one RTX 4090 per arm, 4,096 parallel environments per GPU, 24 steps per environment per PPO update, five PPO optimization epochs, four minibatches per epoch, seed 42 and FP32 with TF32 permitted. The configured initial decoder and action-standard-deviation learning rate was 1e-5; the actor rate could adapt based on KL. The critic used a separate 3e-4 rate. In B, the configured encoder initial rate was 1e-6. These are saved configuration values, not a claim that the actor learning rate remained constant.

The approximate target-adaptation process occupation through step 4,000 was **6.514 GPU hours for A** and **6.712 GPU hours for B**. This sums each arm's initial training jobs once and its subsequent training jobs, including process startup, model loading and saving. It excludes SONIC source pretraining, data preparation, evaluations, idle allocation and unrelated experiments. It is not a measurement of active CUDA kernel time or the total cost of developing both arms. The analogous saved estimates through step 28,000 are approximately 52.368 and 53.935 GPU hours respectively.

The saved evaluations use fixed reference-start inference and do not perform PPO updates or construct an optimizer. Evaluating a checkpoint changes neither its recorded training budget nor the definition of an earlier checkpoint's results. See [evaluation](evaluation.md) for the separate populations, metrics and limitations.

## Source and rights

Motion Data by [Bones Studio](https://bones.studio/). The project's BONES-derived research results are subject to the applicable non-commercial research licence and attribution requirements; raw motion data are not made available here. Any SONIC source weights, robot assets, other datasets and project code have separate rights and redistribution requirements. Their inclusion or permission must be established before publication.
