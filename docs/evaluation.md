# Evaluation

This document describes saved PM01 simulation results. The fixed test populations and termination rules are local, paper-inspired protocols; they are **not** the undisclosed official Any2Any benchmark. The saved aggregate values are in [aggregate_results.json](../evidence/aggregate_results.json).

## Main results

Completion means that a rollout reached the end of its complete reference without an applicable threshold crossing or an engineering error. It is not a percentage of tracking accuracy. Errors in the table are clip-macro means: each clip has equal weight, and a failed clip contributes only its genuinely executed prefix through the first primary violation.

| Test population | Global PPO step | Arm | Primary completion | 24-joint RMSE | MPJPE-L | Root position L2 |
|---|---:|---|---:|---:|---:|---:|
| Mixed 500 | 4,000 | A | 485/500 (97.0%) | 9.725° | 30.94 mm | 25.59 cm |
| Mixed 500 | 4,000 | B | 483/500 (96.6%) | 9.589° | 34.46 mm | 27.54 cm |
| Mixed 500 | 28,000 | A | 485/500 (97.0%) | 8.657° | 27.36 mm | 18.17 cm |
| Mixed 500 | 28,000 | B | 485/500 (97.0%) | 8.292° | 26.43 mm | 20.26 cm |
| BONES 500 | 4,000 | A | 498/500 (99.6%) | 7.579° | 25.98 mm | 19.67 cm |
| BONES 500 | 4,000 | B | 498/500 (99.6%) | 8.505° | 27.26 mm | 20.35 cm |
| BONES 500 | 10,000 | A | 498/500 (99.6%) | 6.427° | 23.52 mm | 13.31 cm |
| BONES 500 | 10,000 | B | 498/500 (99.6%) | 5.932° | 23.12 mm | 13.49 cm |
| BONES 500 | 28,000 | A | 498/500 (99.6%) | 6.011° | 22.68 mm | 10.72 cm |
| BONES 500 | 28,000 | B | 498/500 (99.6%) | 5.033° | 20.94 mm | 11.16 cm |
| OMOMO quality 500 | 28,000 | A | 498/500 (99.6%) | 8.494° | 26.15 mm | 16.10 cm |
| OMOMO quality 500 | 28,000 | B | 499/500 (99.8%) | 8.204° | 24.56 mm | 17.39 cm |

The BONES joint errors were recomputed from saved actual and reference joint trajectories; the original online scorer recorded the position metrics. MPJPE-L removes each pose's own root translation and retains yaw; MPJPE-G and world-root errors are also in the aggregate file. Joint RMSE covers 23 policy-controlled body joints and the reference-PD-controlled head joint.

The mixed 500 contains 106 LAFAN1 and 394 OMOMO references. At 4,000 steps, A completed 93/106 LAFAN1 and 392/394 OMOMO; B completed 91/106 and 392/394. Its source-derived difficulty groups were basic 150, moderate 150 and hard 200. At 4,000 steps A completed 186/200 hard references and B 184/200; the run/jump/land label contains only 12 references, of which each completed 9. These are engineering labels, not certified physical difficulty or proof of flight.

The same mixed 500 was evaluated at 4,000 and 28,000 steps. For A, 482 clips passed at both stages, 3 changed from failure to success, 3 from success to failure and 12 failed at both. For B, the corresponding counts were 481, 4, 2 and 13. On this selected population, later checkpoints reduced average joint and global position errors even where overall completion changed little. These figures do not establish statistical or universal superiority.

## Conditions and interpretation

- Simulation used the PM01 model in Isaac Sim/Isaac Lab with PhysX, 200 Hz physics and 50 Hz control. Evaluations used a fixed first reference frame, seed 42 and one rollout per clip per model. Policy parameters and execution were FP32 with TF32 enabled for supported operations; threshold arithmetic was FP64.
- The primary failure rule is a root height error strictly greater than 0.25 m, any of 13 tracked-link height errors greater than 0.30 m, or a full root SO(3) angle θ greater than 0.8 rad. The secondary interpretation replaces the last condition with θ² greater than 0.8 rad². The actual physical envelope uses the secondary orientation condition; the primary result marks the first observed primary crossing and stops its metric window there. Both interpretations are reported separately in the aggregate file.
- The fixed populations were selected before these rollouts and include previous exposure to the test sets. The BONES recording-level split excludes the PM01 adaptation recordings, but 431/500 test clips share an action-family label with training. The 106 LAFAN1 clips come from 26 synchronous groups and should not be treated as 106 independent recordings. The original SONIC pretraining source overlap is unknown.
- BONES 500 and OMOMO quality 500 were reference-qualified; the mixed 500 is also a selected cohort. The 272 mixed-cohort sources that appeared in the earlier OMOMO quality 500 are not independent observations across the two sets. No object dynamics were simulated for the OMOMO body-tracking evaluations.

The new 4,000-step trajectories and their reported aggregates received a separately initiated CPU integrity review. Its verdict was **WARN**, with same-family review independence and provisional acceptance. Scope limits include the selected populations, prior exposure, one fixed start and one seed. See [limitations](limitations.md) before using these numbers.

Motion Data by [Bones Studio](https://bones.studio/). BONES-derived results here are associated with eligible academic/non-commercial research use; see [limitations](limitations.md) for the separate source and model rights.
