# Limitations and responsible use

These materials describe selected PM01 simulation experiments, not a general-purpose robot-control product. No real-robot execution, disturbance recovery, safety-certified operation, object manipulation, or production readiness is established. Fixed-start tracking does not establish safe entry, continuous switching, standing recovery, fault handling or emergency stop.

## What the numbers do and do not show

- Completion means that the complete reference was observed without crossing the stated threshold. It is not pose accuracy. Joint, local/global body, root position and orientation errors need to accompany completion.
- The 4,000-step results use a single seed, one rollout per clip and reference-frame initialization. Failures remain in each denominator. For failed clips, error summaries contain the actual executed prefix only; the unexecuted suffix is not simulated or fabricated.
- The mixed 500 and BONES 500 use recorded sources held out from PM01 target-adaptation training. They are not newly blinded tests: these populations had been evaluated previously. SONIC pretraining exposure to the underlying sources is unknown.
- The mixed cohort is a selected, reference-qualified 106 LAFAN1 plus 394 OMOMO clips. Its LAFAN1 windows share 26 synchronous recording groups. The BONES test contains 500 held-out recordings selected from 1,209 candidates, but 431/500 clips share an action-family label with the adaptation set. The quality-conditioned OMOMO 500 is not a random sample of all OMOMO; 272 of its source sequences also occur in the mixed cohort.
- Source-derived action and difficulty labels are engineering annotations. A source label such as jump does not establish that the simulated PM01 became airborne. Saved trajectories lack measured contact forces; a foot-geometry diagnostic alone is not a force measurement.
- OMOMO is used for body tracking without the object dynamics or object load. A successful rollout is not a successful manipulation task.
- The local 0.8-rad primary and 0.8-rad² secondary orientation interpretations are reported separately. The selected datasets, morphology, simulator and tracked points differ from the authors' undisclosed Any2Any evaluation. No cross-paper efficiency or equal-performance claim follows from GPU-hour ratios.
- A separately initiated review of the new 4,000-step trajectories returned WARN for scope and uses same-family, provisional review. It supports the reported bounded measurements, not unqualified generalization.

## Motion-data and model rights

Motion Data by [Bones Studio](https://bones.studio/). The project owner has identified the intended use as qualifying academic/non-commercial research. Under the applicable BONES/SEED terms, that confirmed use can include public display of results, subject to the licence and attribution conditions; raw motion data must not be made accessible. This project-specific eligibility does not grant downstream users blanket commercial or redistribution permission.

LAFAN1 and OMOMO contribute separate aggregate evaluation results. Their motion data are governed by their source terms. See [Licences and attribution](licensing.md).

The release contains inference-only Actor exports. The code consumes packed observations and returns raw action means. Robot integration requires a separately validated interface and safety process.
