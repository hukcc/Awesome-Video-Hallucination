# Method Scope Audit

Reviewed **2026-11-01**. All **53 method contributions** received official abstract, introduction, and relevant method/evaluation review. Sources are pinned arXiv versions or the official IJCAI PDF. This is a relevance, intervention, and evaluation-evidence audit, not experimental replication or a claim that every appendix was read.

Outcome: **39 recommended for retention** (including a method-name correction) and **14 proposed moves to related work, awaiting human approval**. No method has been removed. All existing training-free flags agree with the inspected sources. Paper URLs, resource badges, stable identifiers, and sibling benchmark decisions are preserved.

## Scope Rule

- A core method explicitly targets unsupported or contradicted claims about input video. Targeted post-hoc claim verification and audio-visual hallucination interventions qualify; general QA, grounding, efficiency, or reliability methods are not automatically dedicated mitigation methods.
- Research objective and strength of evaluation are separate. Vista-LLaMA, MMA, and Temporal Insight explicitly target hallucinations but have indirect or narrow evaluation evidence. They are retained with limitations, not presented as validated by dedicated hallucination rates.
- Dedicated hallucination tests in a broad method are real evidence, but do not by themselves make that method a core hallucination intervention. CoE, Video-ToC, and SToP are conservative boundary recommendations for manual review, not claims that their hallucination experiments are absent.
- Frozen backbones do not imply training-free operation when an auxiliary classifier, aligner, controller, or patcher is learned. Input-only gradient optimization with fixed parameters is distinguished from parameter learning; off-the-shelf pretrained components do not imply new task-specific training.
- Detection, answer selection, selective risk, grounding accuracy, omission rates, and generation hallucination rates are different outcomes. Multimodal aggregate gains are not video-only gains.

These are curator judgments about collection scope, not scientific-quality rankings. A method and benchmark from the same paper are reviewed independently. Pending recommendations below do not remove Vript-HAL, VHD, or any other sibling benchmark.

## Manual Decision Queue

| Method | Reason to Consider Related Work |
| --- | --- |
| [ClueNet](#method-mitigation--context-driven-fabrication--scene-event-hallucination--cluenet--2603-15008) | General clue-guided VideoQA is the core evaluated task. WUPS and answer accuracy do not establish a measured unsupported-claim reduction despite the paper's hallucination wording. |
| [CoE](#method-mitigation--spatiotemporal-dynamics--duration-distortion--coe--2601-07761) | A conservative strict-scope exclusion: the primary contribution co-optimizes general perceptual grounding and reasoning efficiency. Its explicit hallucination reward and tests remain relevant, so exclusion is not a claim that such evidence is absent. |
| [FrameRepeat](#method-mitigation--spatiotemporal-dynamics--duration-distortion--framerepeat--2603-16256) | Targets visual forgetting and reasoning performance; reported general QA gains do not establish dedicated hallucination mitigation. The learned scorer is not training-free. |
| [Reflect-R1](#method-mitigation--spatiotemporal-dynamics--duration-distortion--reflect-r1--2606-27922) | Targets general long-video answer correction; the inspected evidence uses correctness and rectification, not a dedicated unsupported-claim/hallucination protocol. The paper's hallucination-loop claim is not itself a measured hallucination rate. |
| [SToP](#method-mitigation--context-driven-fabrication--both-object-action-scene-event--stop--2604-20937) | Strict-scope boundary recommendation: core objective is efficient token pruning while preserving fine-grained understanding. Hallucination is a diagnostic and benefit, not the sole dedicated task; this is not an image-only method or a claim that no hallucination evaluation exists. |
| [STVG-R1](#method-mitigation--context-driven-fabrication--object-action-hallucination--stvg-r1--2602-11730) | Addresses coordinate/timestamp prediction errors in grounding, not unsupported video-language claims under the catalog's strict hallucination scope. IoU and mask accuracy are not hallucination rates. |
| [TRACE-RC](#method-mitigation--context-driven-fabrication--compositional-and-factuality-hallucination--trace-rc--2609-13288) | Recommend moving out of the core mitigation list into related reliability work. The method targets general answer-risk ranking under shift, not answer correction or video-specific claim verification. Retain the separate VHD benchmark; lower selective risk is not lower full-coverage hallucination incidence. |
| [Video-ToC](#method-mitigation--context-driven-fabrication--scene-event-hallucination--video-toc--2604-20473) | Strict-scope boundary recommendation: the central contribution is general perception-aware video reasoning, with hallucination evaluation as an additional benefit. This is not a claim that hallucination evidence is absent. |
| [Video-TwG](#method-mitigation--spatiotemporal-dynamics--duration-distortion--video-twg--2602-18702) | A general long-video reasoning and grounding method; hallucination language is not accompanied by a dedicated reduction test in the inspected protocol. |
| [VideoChat-Online](#method-mitigation--referential-inconsistency--scene-conflation--videochat-online--2501-00584) | Core contribution is general streaming perception, memory, and reasoning rather than a dedicated video-hallucination intervention. |
| [VideoTemp-o3](#method-mitigation--spatiotemporal-dynamics--event-misordering--videotemp-o3--2602-07801) | Hallucination motivates better visual evidence, but the core contribution and reported protocol target general grounding/QA rather than dedicated video-hallucination mitigation. |
| [VideoTIR](#method-mitigation--spatiotemporal-dynamics--duration-distortion--videotir--2603-25021) | Hallucination is a motivation, but the core method and evidence address efficient long-video QA and tool use. |
| [Vriptor](#method-mitigation--spatiotemporal-dynamics--frequency-confusion--vriptor--2406-06040) | Vriptor is a general detailed-captioning model rather than a dedicated hallucination intervention. The separately introduced Vript-HAL benchmark remains eligible and must not be removed with the model. |
| [VTG-LLM](#method-mitigation--spatiotemporal-dynamics--frequency-confusion--vtg-llm--2405-13382) | A temporal-grounding model, not a method whose central objective is video-hallucination mitigation. Timestamp localization accuracy alone is insufficient. |

## Corrections and Evidence Limits

- **MoPE:** name the mitigation entry **GRPO with MoPE**, as in Section 4.3. MoPE is the parsing/evaluation component; the listed intervention uses it as a training reward. The old name remains an alias.
- **PEP-MEK:** expand as **Predict-Explain-Predict with Modality and Emotion Knowledge**, not perception-enhanced prompting or a memory-based mechanism. Table 3 reports mixed-modality results, not isolated video gains.
- **ProCap:** automatic Temporal Inconsistency measures missing salient objects. Its separate human inconsistency ratings address unsupported content; a rating change is not an incidence rate.
- **GroundedVQA:** tags drafted claims without rewriting them. Its evidence is 40 claims from 12 questions on one animated video, not a broad benchmark.
- **Video-DPL / TRACE-RC:** evaluator accuracy and selective-risk ranking must not be reported as a reduction in hallucinations in all generated answers. TRACE-RC never changes base answers.
- **C-TCD:** assumes a scene-matched counterfactual counterpart at inference. **ELV-Halluc-DPO:** the best SAH-ratio result uses in-video pairs; the combined 8k setting is different.
- **mrDPO:** total error combines missing and hallucinated events. **VideoHallu-GRPO:** the source labels its training GRPO, but Equation 2 has a pairwise DPO form; the implementation has not been independently resolved or reproduced.

## Evidence Register

Each entry records the inspected sections, intervention, actual evaluation, training requirement, and recommendation. Source-file SHA-256 hashes in the machine-readable register identify the downloaded evidence used for this pass; they are not a guarantee that an HTML rendering will remain byte-identical.

### Pending Scope Decisions

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--cluenet--2603-15008"></a>

#### ClueNet

[Clue Matters: Leveraging Latent Visual Clues to Empower Video Reasoning](https://arxiv.org/abs/2603.15008) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--cluenet--2603-15008)). **Training-free: No.**

- **Intervention:** Trains clue extraction, differentiable clue gating, and clue-conditioned reasoning with supervised losses.
- **Evaluation:** NExT-QA, STAR, MVBench accuracy and NExT-OE WUPS semantic similarity.
- **Assessment:** General clue-guided VideoQA is the core evaluated task. WUPS and answer accuracy do not establish a measured unsupported-claim reduction despite the paper's hallucination wording.
- **Inspected:** [Abstract; Introduction; Sections 4.4, 5.1, and 5.2 open-ended generation](https://arxiv.org/html/2603.15008v1).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--coe--2601-07761"></a>

#### CoE

[Video Evidence to Reasoning Efficient Video Understanding via Explicit Evidence Grounding](https://arxiv.org/abs/2601.07761) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--coe--2601-07761)). **Training-free: No.**

- **Intervention:** Jointly trains evidence grounding and concise reasoning, with evidence-alignment and answer-accuracy rewards.
- **Evaluation:** Includes genuine VidHal and EventHallusion evaluation alongside Video-MME, MVBench, and VSI-Bench.
- **Assessment:** A conservative strict-scope exclusion: the primary contribution co-optimizes general perceptual grounding and reasoning efficiency. Its explicit hallucination reward and tests remain relevant, so exclusion is not a claim that such evidence is absent.
- **Inspected:** [Abstract; Introduction; Section II-C; Section IV-A; Section IV-D (Quantifying the CoE Advantage)](https://arxiv.org/html/2601.07761v2).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--framerepeat--2603-16256"></a>

#### FrameRepeat

[When Thinking Hurts: Mitigating Visual Forgetting in Video Reasoning via Frame Repetition](https://arxiv.org/abs/2603.16256) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--framerepeat--2603-16256)). **Training-free: No.**

- **Intervention:** Learns a frame-repeat scoring module from Add-One-In correct-answer log-probability gains, then repeats selected frames.
- **Evaluation:** VideoMME, MLVU, LongVideoBench, LVBench, and Video-Holmes reasoning/QA accuracy.
- **Assessment:** Targets visual forgetting and reasoning performance; reported general QA gains do not establish dedicated hallucination mitigation. The learned scorer is not training-free.
- **Inspected:** [Abstract; Introduction; Section 4.2; Section 5.1](https://arxiv.org/html/2603.16256v1).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--reflect-r1--2606-27922"></a>

#### Reflect-R1

[Reflect-R1: Evidence-Driven Reflection for Self-Correction in Long Video Understanding](https://arxiv.org/abs/2606.27922) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--reflect-r1--2606-27922)). **Training-free: No.**

- **Intervention:** SFT and stage-decoupled reinforcement learning train intuition, evidence retrieval, verification, and arbitration.
- **Evaluation:** VideoMME, LongVideoBench, MLVU answer accuracy and correction behavior, plus Haystack-LVBench retrieval metrics.
- **Assessment:** Targets general long-video answer correction; the inspected evidence uses correctness and rectification, not a dedicated unsupported-claim/hallucination protocol. The paper's hallucination-loop claim is not itself a measured hallucination rate.
- **Inspected:** [Abstract; Introduction; Section 2; Section 3.4 (Model training); Section 4.1](https://arxiv.org/html/2606.27922v3).

<a href="https://github.com/ShuimuChen-hyq/Reflect-R1"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a> <a href="https://huggingface.co/datasets/CSDDSFSFSAFSAF/Reflect-R1-data"><img src="https://img.shields.io/badge/Dataset-HuggingFace-yellow?logo=huggingface" alt="dataset" title="Dataset" /></a>

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--stop--2604-20937"></a>

#### SToP

[Sink-Token-Aware Pruning for Fine-Grained Video Understanding in Efficient Video LLMs](https://arxiv.org/abs/2604.20937) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--stop--2604-20937)). **Training-free: Yes.**

- **Intervention:** Adds sink-token penalties to existing spatial/temporal pruning rules to preserve visual information under small token budgets.
- **Evaluation:** Genuine EventHallusion binary/description evaluation alongside VideoComp, VCG-Bench, and generic VideoQA under 10-20% token retention.
- **Assessment:** Strict-scope boundary recommendation: core objective is efficient token pruning while preserving fine-grained understanding. Hallucination is a diagnostic and benefit, not the sole dedicated task; this is not an image-only method or a claim that no hallucination evaluation exists.
- **Inspected:** [Abstract; Introduction; Sections 4.2 and 5.1](https://arxiv.org/html/2604.20937v2).

<a id="method-mitigation--context-driven-fabrication--object-action-hallucination--stvg-r1--2602-11730"></a>

#### STVG-R1

[STVG-R1: Incentivizing Instance-Level Reasoning and Grounding in Videos via Reinforcement Learning](https://arxiv.org/abs/2602.11730) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--object-action-hallucination--stvg-r1--2602-11730)). **Training-free: No.**

- **Intervention:** Adds tracked object-ID visual prompts and learns grounding through temporal IoU, spatial consistency, and format rewards.
- **Evaluation:** HCSTVG, ST-Align, Charades-STA, TVGBench and MeViS localization/segmentation metrics.
- **Assessment:** Addresses coordinate/timestamp prediction errors in grounding, not unsupported video-language claims under the catalog's strict hallucination scope. IoU and mask accuracy are not hallucination rates.
- **Inspected:** [Abstract; Introduction; Sections 3.3 and 4.1](https://arxiv.org/html/2602.11730v1).

<a id="method-mitigation--context-driven-fabrication--compositional-and-factuality-hallucination--trace-rc--2609-13288"></a>

#### TRACE-RC

[Target-Checked Reliability Score Refinement for Video Question Answering](https://arxiv.org/abs/2609.13288) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--compositional-and-factuality-hallucination--trace-rc--2609-13288)). **Training-free: No.**

- **Intervention:** Trains HGB and target-pilot logistic reliability scorers over fixed model/view responses; does not change any generated answer.
- **Evaluation:** Held-out HERBench and Perception Test AURC, AUROC, calibration and selective risk; VHD is used for development and diagnosis.
- **Assessment:** Recommend moving out of the core mitigation list into related reliability work. The method targets general answer-risk ranking under shift, not answer correction or video-specific claim verification. Retain the separate VHD benchmark; lower selective risk is not lower full-coverage hallucination incidence.
- **Inspected:** [Abstract; Introduction; Sections 3.3, 4.1, and 4.5](https://arxiv.org/html/2609.13288v1).

<a href="https://github.com/sydney-machine-learning/video-hallucination-diagnosis"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a> <a href="https://www.kaggle.com/datasets/mlopssss/video-hallucination-diagnosis"><img src="https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle&amp;logoColor=white" alt="dataset" title="Dataset" /></a>

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--video-toc--2604-20473"></a>

#### Video-ToC

[Video-ToC: Video Tree-of-Cue Reasoning](https://arxiv.org/abs/2604.20473) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--video-toc--2604-20473)). **Training-free: No.**

- **Intervention:** SFT and GRPO teach tree-guided cue localization with rewards scaled by question reasoning demand.
- **Evaluation:** Six general reasoning/understanding benchmarks and genuine VideoHallucer evaluation; the latter improves average accuracy but not every category.
- **Assessment:** Strict-scope boundary recommendation: the central contribution is general perception-aware video reasoning, with hallucination evaluation as an additional benefit. This is not a claim that hallucination evidence is absent.
- **Inspected:** [Abstract; Introduction; Section III-C reasoning-demand reward; Section IV-B benchmarks and Table II](https://arxiv.org/html/2604.20473v1).

<a href="https://github.com/qizhongtan/Video-ToC"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a>

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--video-twg--2602-18702"></a>

#### Video-TwG

[Think with Grounding: Curriculum Reinforced Reasoning with Video Grounding for Long Video Understanding](https://arxiv.org/abs/2602.18702) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--video-twg--2602-18702)). **Training-free: No.**

- **Intervention:** Uses two-stage reinforcement learning for on-demand grounding and video QA, with grounding and pseudo-rewards.
- **Evaluation:** Multiple-choice Video-MME, LongVideoBench, and MLVU accuracy, with grounding quality/efficiency ablations.
- **Assessment:** A general long-video reasoning and grounding method; hallucination language is not accompanied by a dedicated reduction test in the inspected protocol.
- **Inspected:** [Abstract; Introduction; Section 3.4; Section 4.3](https://arxiv.org/html/2602.18702v1).

<a id="method-mitigation--referential-inconsistency--scene-conflation--videochat-online--2501-00584"></a>

#### VideoChat-Online

[Online Video Understanding: OVBench and VideoChat-Online](https://arxiv.org/abs/2501.00584) ([catalog entry](../README.md#paper-mitigation--referential-inconsistency--scene-conflation--videochat-online--2501-00584)). **Training-free: No.**

- **Intervention:** Trains offline-to-online video understanding with a pyramid memory bank and interleaved streaming instruction data.
- **Evaluation:** OVBench and generic offline VideoQA accuracy; OVBench includes temporal-hallucination subtasks within a broader streaming suite.
- **Assessment:** Core contribution is general streaming perception, memory, and reasoning rather than a dedicated video-hallucination intervention.
- **Inspected:** [Abstract; Introduction; Sections 4.2, 5.2, and 5.3](https://arxiv.org/html/2501.00584v2).

<a href="https://videochat-online.github.io/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?logo=readthedocs&amp;logoColor=white" alt="page" title="Project Page" /></a> <a href="https://github.com/mcg-nju/videochat-online"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a>

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--videotemp-o3--2602-07801"></a>

#### VideoTemp-o3

[VideoTemp-o3: Harmonizing Temporal Grounding and Video Understanding in Agentic Thinking-with-Videos](https://arxiv.org/abs/2602.07801) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--videotemp-o3--2602-07801)). **Training-free: No.**

- **Intervention:** SFT and reinforcement learning jointly optimize temporal grounding, answer accuracy, format, and iterative clip refinement.
- **Evaluation:** Long-video QA, temporal-grounding IoU, and grounded QA on VideoTemp-Bench, NextGQA, ReXTime, Charades-STA, and related general benchmarks.
- **Assessment:** Hallucination motivates better visual evidence, but the core contribution and reported protocol target general grounding/QA rather than dedicated video-hallucination mitigation.
- **Inspected:** [Abstract; Introduction; Section 4.2 (Reward Design); Section 5.1; Appendix B.2](https://arxiv.org/html/2602.07801v4).

<a href="https://liuwq-bit.github.io/VideoTemp-o3/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?logo=readthedocs&amp;logoColor=white" alt="page" title="Project Page" /></a> <a href="https://github.com/Kwai-Keye/VideoTemp-o3"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a>

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--videotir--2603-25021"></a>

#### VideoTIR

[VideoTIR: Accurate Understanding for Long Videos with Efficient Tool-Integrated Reasoning](https://arxiv.org/abs/2603.25021) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--videotir--2603-25021)). **Training-free: No.**

- **Intervention:** Trains a multi-tool video reasoning policy with TAGPO, with optional SFT cold start and multi-granularity retrieval.
- **Evaluation:** MVBench, Video-MME, and LongVideoBench QA plus tool-call efficiency, not a dedicated hallucination protocol.
- **Assessment:** Hallucination is a motivation, but the core method and evidence address efficient long-video QA and tool use.
- **Inspected:** [Abstract; Introduction; Section 3.1; Section 4.1](https://arxiv.org/html/2603.25021v3).

<a id="method-mitigation--spatiotemporal-dynamics--frequency-confusion--vriptor--2406-06040"></a>

#### Vriptor

[Vript: A Video Is Worth Thousands of Words](https://arxiv.org/abs/2406.06040) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--frequency-confusion--vriptor--2406-06040)). **Training-free: No.**

- **Intervention:** Trains dense video-script captioning with aligned multi-scene captions, voice-over transcripts, and timestamps.
- **Evaluation:** Genuine Vript-HAL object/action precision, recall, and F1, alongside captioning and long-video tasks.
- **Assessment:** Vriptor is a general detailed-captioning model rather than a dedicated hallucination intervention. The separately introduced Vript-HAL benchmark remains eligible and must not be removed with the model.
- **Inspected:** [Abstract; Introduction; Section 4.1; Section 5.1 (Hallucination Evaluation Metrics; Evaluation)](https://arxiv.org/html/2406.06040v2).

<a href="https://github.com/mutonix/Vript"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a>

<a id="method-mitigation--spatiotemporal-dynamics--frequency-confusion--vtg-llm--2405-13382"></a>

#### VTG-LLM

[VTG-LLM: Integrating Timestamp Knowledge into Video LLMs for Enhanced Video Temporal Grounding](https://arxiv.org/abs/2405.13382) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--frequency-confusion--vtg-llm--2405-13382)). **Training-free: No.**

- **Intervention:** Trains timestamp-aware embeddings, absolute-time tokens, and slot-based compression for temporal grounding.
- **Evaluation:** YouCook2 CIDEr/SODA/F1, Charades-STA temporal IoU recall, and QVHighlights mAP/HIT@1.
- **Assessment:** A temporal-grounding model, not a method whose central objective is video-hallucination mitigation. Timestamp localization accuracy alone is insufficient.
- **Inspected:** [Abstract; Introduction; Method: Overview of VTG-LLM; Experiments: Experiment Settings](https://arxiv.org/html/2405.13382v3).

<a href="https://github.com/gyxxyg/VTG-LLM"><img src="https://img.shields.io/badge/Code-Link-blue?logo=github" alt="code" title="Code" /></a>

### Retained With a Name Correction

<a id="method-mitigation--spatiotemporal-dynamics--frequency-confusion--mope--2602-17768"></a>

#### GRPO with MoPE

[KPM-Bench: A Kinematic Parsing Motion Benchmark for Fine-grained Motion-centric Video Understanding](https://arxiv.org/abs/2602.17768) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--frequency-confusion--mope--2602-17768)). **Training-free: No.**

- **Intervention:** Uses MoPE-extracted action, order, and direction matches as a composite GRPO reward following supervised fine-tuning.
- **Evaluation:** KPM-HA GPT-Hall and Mo-Hall, separated from generic caption metrics and QA accuracy.
- **Assessment:** Retain the targeted motion-hallucination post-training contribution, named GRPO with MoPE as in Section 4.3. MoPE alone is a parsing/evaluation algorithm, not the trained mitigation policy.
- **Inspected:** [Abstract; Introduction; Sections 4.3, 5.1, and 5.2](https://arxiv.org/html/2602.17768v1).

### Retained Methods

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--arp-cd--2610-19728"></a>

#### ARP-CD

[Mitigating Video Hallucinations via Attention-Guided Representation Perturbation](https://arxiv.org/abs/2610.19728) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--arp-cd--2610-19728)). **Training-free: Yes.**

- **Intervention:** Optimizes input visual hidden-state perturbations for a contrastive negative; model weights are not trained.
- **Evaluation:** VideoHallucer and EventHallusion, alongside separate general-understanding tests. Not every model/benchmark combination improves.
- **Assessment:** Video-grounded hallucination mitigation is the explicit design target and is directly evaluated.
- **Inspected:** [Abstract; Introduction; Sections 3.3, 4.1 (Benchmarks), and 4.2 (Hallucination mitigation)](https://arxiv.org/html/2610.19728v1).

<a id="method-mitigation--audio-visual-conflict--action-attribution--avcd--2505-20862"></a>

#### AVCD

[AVCD: Mitigating Hallucinations in Audio-Visual Large Language Models through Contrastive Decoding](https://arxiv.org/abs/2505.20862) ([catalog entry](../README.md#paper-mitigation--audio-visual-conflict--action-attribution--avcd--2505-20862)). **Training-free: Yes.**

- **Intervention:** Uses modality-dominance-aware attentive masking, trimodal contrastive logits, and entropy-gated extra decoding without parameter updates.
- **Evaluation:** AVHBench cross-modal hallucination evaluation; MUSIC-AVQA, MSVD-QA and ActivityNet-QA are separate general tasks.
- **Assessment:** Direct audio-visual hallucination intervention. Video-only QA gains alone are not proof of video-only hallucination reduction; the direct evidence comes from the audio-visual conditions.
- **Inspected:** [Abstract; Introduction; Sections 3.2, 4.1, and 4.2](https://arxiv.org/html/2505.20862v2).

<a id="method-mitigation--audio-visual-conflict--action-attribution--avhmodel-align-ft--2410-18325"></a>

#### AVHModel-Align-FT

[AVHBench: A Cross-Modal Hallucination Benchmark for Audio-Visual Large Language Models](https://arxiv.org/abs/2410.18325) ([catalog entry](../README.md#paper-mitigation--audio-visual-conflict--action-attribution--avhmodel-align-ft--2410-18325)). **Training-free: No.**

- **Intervention:** Trains audio alignment and LoRA adaptations on audio-visual hallucination-aware questions.
- **Evaluation:** AVHBench audio-driven video and video-driven audio hallucination tasks; captioning/matching and VAST/AVinstruct are distinct outcomes.
- **Assessment:** Explicit cross-modal hallucination mitigation with direct audio-induced false visual-claim evaluation; not audio-only research.
- **Inspected:** [Abstract; Introduction; Section 4.2 audio alignment and LoRA FT; Appendix F](https://arxiv.org/html/2410.18325v2).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--c-tcd--2604-20460"></a>

#### C-TCD

[CCTVBench: Contrastive Consistency Traffic VideoQA Benchmark for Multimodal LLMs](https://arxiv.org/abs/2604.20460) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--c-tcd--2604-20460)). **Training-free: Yes.**

- **Intervention:** Contrasts logits with a scene-matched, semantically exclusive counterfactual counterpart supplied by CCTVBench.
- **Evaluation:** CCTVBench instance classification and strict quadruple consistency, with negative hallucination diagnostics.
- **Assessment:** Targets unsupported traffic-event assertions, but depends on paired counterfactual videos at inference; do not imply an unrestricted single-video deployment method.
- **Inspected:** [Abstract; Introduction; Sections 4.3 and 4.4 contrastive-decoding results](https://arxiv.org/html/2604.20460v1).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--dino-heal--2412-03735"></a>

#### DINO-HEAL

[VidHalluc: Evaluating Temporal Hallucinations in Multimodal Large Language Models for Video Understanding](https://arxiv.org/abs/2412.03735) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--dino-heal--2412-03735)). **Training-free: Yes.**

- **Intervention:** Reweights video visual features with fixed DINOv2 spatial saliency maps during inference.
- **Evaluation:** VidHalluc action, temporal-sequence, and scene-transition tasks with baseline/intervention comparisons; some individual scores do not improve.
- **Assessment:** A dedicated inference-time hallucination intervention with direct video evaluation.
- **Inspected:** [Abstract; Introduction; Section 4.3; Section 5.2 (Table 4)](https://arxiv.org/html/2412.03735v2).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--dtr--2604-12582"></a>

#### DTR

[Relaxing Anchor-Frame Dominance for Mitigating Hallucinations in Video Large Language Models](https://arxiv.org/abs/2604.12582) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--dtr--2604-12582)). **Training-free: Yes.**

- **Intervention:** Rebalances decoder visual-attention logits toward under-attended frames in selected middle-to-late layers, without training or extra decoding branches.
- **Evaluation:** EventHallusion and VideoHallucer. LLaVA uses paired accuracy; Qwen uses hallucinated-question accuracy, so those protocol values are not interchangeable.
- **Assessment:** Anchor-frame-driven hallucination is the central target, tested with dedicated video-hallucination tasks.
- **Inspected:** [Abstract; Introduction; Section 3.2; Section 4.1.1](https://arxiv.org/html/2604.12582v1).

<a id="method-mitigation--referential-inconsistency--scene-conflation--elv-halluc-dpo--2508-21496"></a>

#### ELV-Halluc-DPO

[ELV-Halluc: Benchmarking Semantic Aggregation Hallucinations in Long Video Understanding](https://arxiv.org/abs/2508.21496) ([catalog entry](../README.md#paper-mitigation--referential-inconsistency--scene-conflation--elv-halluc-dpo--2508-21496)). **Training-free: No.**

- **Intervention:** DPO trains caption preferences using within-video or out-of-video hallucinated negatives.
- **Evaluation:** ELV-Halluc average accuracy and SAH ratio, with Video-MME as a separate general-capability check.
- **Assessment:** Direct long-video semantic-aggregation mitigation. The best SAH reduction uses 4k in-video pairs, not the combined 8k setting; SAH ratio and overall hallucination are distinct.
- **Inspected:** [Abstract; Introduction; Strategies for Mitigating SAH (position encoding and DPO)](https://arxiv.org/html/2508.21496v2).

<a id="method-mitigation--context-driven-fabrication--object-action-hallucination--gm-dpo--2609-36628"></a>

#### GM-DPO

[Beyond Binary Preferences: Graded Preference Optimization for Limb-Motion Captioning](https://arxiv.org/abs/2609.36628) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--object-action-hallucination--gm-dpo--2609-36628)). **Training-free: No.**

- **Intervention:** Scales DPO margins and loss weights with action-error severity to penalize incorrect or fabricated limb-motion claims.
- **Evaluation:** FlexBench GPA and Weighted Hallucination Rate, with caption length/shot structure and generic QA reported separately.
- **Assessment:** Direct motion-hallucination alignment; reported WHR reduction varies by backbone and is distinct from aggregate GPA gain.
- **Inspected:** [Abstract; Introduction; Sections 4.3, 5.1, and 5.4](https://arxiv.org/html/2609.36628v1).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--graphthinker--2602-17555"></a>

#### GraphThinker

[GraphThinker: Reinforcing Temporally Grounded Video Reasoning with Event Graph Thinking](https://arxiv.org/abs/2602.17555) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--graphthinker--2602-17555)). **Training-free: No.**

- **Intervention:** GRPO trains event-graph-guided reasoning with visual-attention, accuracy, and format rewards.
- **Evaluation:** Official VidHalluc ACH/TSH accuracy and STH score; RexTime grounding and QA are separate.
- **Assessment:** Directly targets weak visual grounding and temporal reasoning hallucinations, with dedicated video-hallucination evaluation.
- **Inspected:** [Abstract; Introduction; Sections 3.3 and 4.1](https://arxiv.org/html/2602.17555v3).

<a id="method-mitigation--context-driven-fabrication--compositional-and-factuality-hallucination--groundedvqa--2608-15574"></a>

#### GroundedVQA

[Catching Hallucinated Citations in Video-LLM Question Answering: A Self-Verification Pipeline and Verifier Ablation Study](https://arxiv.org/abs/2608.15574) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--compositional-and-factuality-hallucination--groundedvqa--2608-15574)). **Training-free: Yes.**

- **Intervention:** Blindly re-captions cited video frames and uses an off-the-shelf pretrained NLI classifier to tag drafted claims as Grounded or Unverified.
- **Evaluation:** Forty claims from 12 questions on one animated video, including adversarial false premises; no broad held-out benchmark or confidence intervals.
- **Assessment:** Direct post-hoc video-claim verification, not answer rewriting. Catch rate measures verification on a small controlled sample, not generation improvement or broad generalization. No task-specific NLI training is introduced.
- **Inspected:** [Abstract; Introduction; Sections 3.3, 5.3, 6, and 8](https://arxiv.org/html/2608.15574v1).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--macd--2602-01740"></a>

#### MACD

[MACD: Model-Aware Contrastive Decoding via Counterfactual Data](https://arxiv.org/abs/2602.01740) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--macd--2602-01740)). **Training-free: Yes.**

- **Intervention:** Optimizes input object/frame masks using query-side gradients, then applies contrastive decoding while model parameters stay fixed.
- **Evaluation:** EventHallusion and a video-adapted POPE absent-object test; general QA benchmarks are separate.
- **Assessment:** Dedicated hallucination intervention. Input-mask optimization does not constitute model training; the video-POPE test is a custom subset protocol.
- **Inspected:** [Abstract; Introduction; Section 4.2; Section 5.1 benchmarks; Section 5.4](https://arxiv.org/html/2602.01740v3).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--mash-vlm--2503-15871"></a>

#### MASH-VLM

[MASH-VLM: Mitigating Action-Scene Hallucination in Video-LLMs through Disentangled Spatial-Temporal Representations](https://arxiv.org/abs/2503.15871) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--mash-vlm--2503-15871)). **Training-free: No.**

- **Intervention:** Trains with disentangled spatial-temporal attention and Harmonic-RoPE to suppress spurious action-scene associations.
- **Evaluation:** UNSCENE dual-question correctness and open-ended action/scene scoring; generic VideoQA metrics are separate.
- **Assessment:** Action-scene hallucination is the explicit design target and receives dedicated evaluation.
- **Inspected:** [Abstract; Introduction; Section 3.3; Section 4.2; Section 5.1 instruction tuning](https://arxiv.org/html/2503.15871v1).

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--mixdpo--2601-04778"></a>

#### MixDPO

[CounterVid: Counterfactual Video Generation for Mitigating Action and Temporal Hallucinations in Video-Language Models](https://arxiv.org/abs/2601.04778) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--mixdpo--2601-04778)). **Training-free: No.**

- **Intervention:** Trains with textual and visual DPO preferences constructed from same-scene counterfactual action videos.
- **Evaluation:** VideoHallucer, EventHallusion, and VidHalluc's temporal-sequence subset, alongside CounterVid and broader tests. Synthetic-video generation is a training-data tool.
- **Assessment:** Directly targets unsupported action and order claims, rather than the quality of generated videos themselves.
- **Inspected:** [Abstract; Introduction; Sections 3.4 and 4.1; Appendix C.1](https://arxiv.org/html/2601.04778v2).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--mma--hallucination-reduction-in-video-language-models-via-hierarchical-multimodal-consistency"></a>

#### MMA

[Hallucination Reduction in Video-Language Models via Hierarchical Multimodal Consistency](https://www.ijcai.org/proceedings/2025/1019) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--mma--hallucination-reduction-in-video-language-models-via-hierarchical-multimodal-consistency)). **Training-free: No.**

- **Intervention:** Trains Q-Former and a text encoder with multilevel semantic-discriminative alignment and two-stage task learning; the vision encoder and LLM remain frozen.
- **Evaluation:** LVU content/metadata top-1 accuracy and MSVD VideoQA accuracy, plus qualitative examples; no dedicated hallucination-rate protocol in the inspected experiments.
- **Assessment:** Retain for its explicit central hallucination-mitigation objective, but mark indirect evaluation evidence. General classification/QA improvements do not quantify hallucination reduction.
- **Inspected:** [Official IJCAI PDF: Abstract, Introduction, Sections 3.1-3.4 and 4.1-4.3 (pp. 9167-9172)](https://www.ijcai.org/proceedings/2025/1019.pdf).

<a id="method-mitigation--audio-visual-conflict--action-attribution--mrdpo--2410-06682"></a>

#### mrDPO

[Enhancing Multimodal LLM for Detailed and Accurate Video Captioning using Multi-Round Preference Optimization](https://arxiv.org/abs/2410.06682) ([catalog entry](../README.md#paper-mitigation--audio-visual-conflict--action-attribution--mrdpo--2410-06682)). **Training-free: No.**

- **Intervention:** Multi-round DPO ranks captions by atomic-event hallucination/omission and repetition metrics, updating the reference and LoRA modules between rounds.
- **Evaluation:** Audio-visual caption missing and hallucinated event rates against annotated event lists, with total error and general QA reported separately.
- **Assessment:** Retain the targeted hallucination-aware preference objective, not an unrestricted endorsement of the whole captioning model. Total error combines omissions and hallucinations and must not be described as hallucination rate alone.
- **Inspected:** [Abstract; Introduction; Sections 3.3 and 5.2; Appendix E](https://arxiv.org/html/2410.06682v2).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--multitop--2606-11792"></a>

#### MultiToP

[MultiToP: Learning to Patch Visual Tokens to Mitigate Hallucinations in Video Large Multimodal Models](https://arxiv.org/abs/2606.11792) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--multitop--2606-11792)). **Training-free: No.**

- **Intervention:** Trains a visual token patcher using answer supervision, information-guided rank calibration, and sparsity regularization with a frozen backbone.
- **Evaluation:** VideoHallucer, Vript-HAL, and VidHalluc; Video-MMMU and ActivityNet-QA are general-capability checks.
- **Assessment:** Direct hallucination mitigation through learned token repair. Ground-truth answers are used during training, not inference.
- **Inspected:** [Abstract; Introduction; Section 3.3.4; Section 4.1 evaluation benchmarks](https://arxiv.org/html/2606.11792v2).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--pami-vdpo--2504-05810"></a>

#### PaMi-VDPO

[PaMi-VDPO: Mitigating Video Hallucinations by Prompt-Aware Multi-Instance Video Preference Learning](https://arxiv.org/abs/2504.05810) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--pami-vdpo--2504-05810)). **Training-free: No.**

- **Intervention:** Updates the model with prompt-aware multi-instance video preference optimization using augmented rejected clips.
- **Evaluation:** Official VideoHallucer and EventHallusion protocols, plus separate general video benchmarks.
- **Assessment:** Direct video-response hallucination mitigation. No additional parameters or preference annotation does not mean training-free.
- **Inspected:** [Abstract; Introduction; Section 5 prompt-aware MIL formulation; Section 6.1 implementation and benchmarks](https://arxiv.org/html/2504.05810v2).

<a id="method-mitigation--audio-visual-conflict--emotion-inference--pep-mek--2505-11405"></a>

#### PEP-MEK

[EmotionHallucer: Evaluating Emotion Hallucinations in Multimodal Large Language Models](https://arxiv.org/abs/2505.11405) ([catalog entry](../README.md#paper-mitigation--audio-visual-conflict--emotion-inference--pep-mek--2505-11405)). **Training-free: Yes.**

- **Intervention:** Prompts modality/emotion knowledge extraction, an initial prediction, explanation and verification, then a revised binary answer.
- **Evaluation:** EmotionHallucer-P mixed-modality paired QA, including video conditions; Table 3 reports pooled results rather than isolated video-only gains.
- **Assessment:** Dedicated multimodal emotion-hallucination intervention with a video application. Scope is limited to video/audio-visual inputs; the pooled 9.9-point improvement is not a video-only result.
- **Inspected:** [Abstract; Introduction; Sections 5.1-5.2 and Table 3; Appendix B.2](https://arxiv.org/html/2505.11405v1).

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--ppv--2606-23061"></a>

#### PPV

[MotionHalluc: Diagnosing Kinematic Hallucinations in Fine-Grained Motion Reasoning](https://arxiv.org/abs/2606.23061) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--ppv--2606-23061)). **Training-free: Yes.**

- **Intervention:** Reconstructs and aligns skeletons, parses candidate instructions into measurement queries, and injects quantitative kinematic evidence at inference.
- **Evaluation:** MotionHalluc directional, attributional, and temporal accuracy; reconstructed and ground-truth motion are compared separately, within Fit3D rather than unconstrained settings.
- **Assessment:** Explicitly reduces unsupported cross-video motion judgments; pretrained reconstruction components do not make the intervention newly trained.
- **Inspected:** [Abstract; Introduction; Section 4; Section 5.2; Appendix H.4](https://arxiv.org/html/2606.23061v2).

<a id="method-mitigation--context-driven-fabrication--object-action-hallucination--procap--2607-21022"></a>

#### ProCap

[ProCap: Prominence-guided Object Rectification for Faithful and Comprehensive Video Captioning](https://arxiv.org/abs/2607.21022) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--object-action-hallucination--procap--2607-21022)). **Training-free: Yes.**

- **Intervention:** Uses fixed detectors and captioners for object-grounded rectification and prominence-guided iterative caption refinement.
- **Evaluation:** MSVD/MSR-VTT object-coverage metrics and a human study rating unsupported/incorrect caption content.
- **Assessment:** Retain the explicit post-hoc visual-faithfulness intervention with a metric caveat: its automatic Temporal Inconsistency measures omitted salient objects, not fabricated objects. The reported human inconsistency improvement is a rating change, not a hallucination incidence rate.
- **Inspected:** [Abstract; Introduction; Sections III-C, IV-A, IV-C1/2, and IV-D2](https://arxiv.org/html/2607.21022v1).

<a id="method-mitigation--context-driven-fabrication--object-action-hallucination--santa--2512-04356"></a>

#### SANTA

[Mitigating Object and Action Hallucinations in Multimodal LLMs via Self-Augmented Contrastive Alignment](https://arxiv.org/abs/2512.04356) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--object-action-hallucination--santa--2512-04356)). **Training-free: No.**

- **Intervention:** Learns tracklet-phrase contrastive alignment using self-generated hallucinative negatives and an action-squeezer.
- **Evaluation:** FactVC and weighted-HalFscore on video captions plus VidHal QA; Dream1k description quality is separate.
- **Assessment:** Joint object/action hallucination mitigation is the central method objective, with explicit caption-level faithfulness evaluation.
- **Inspected:** [Abstract; Introduction; Section 3.4; Section 4.1 (benchmarks, metrics, implementation)](https://arxiv.org/html/2512.04356v1).

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--season--2512-04643"></a>

#### SEASON

[SEASON: Mitigating Temporal Hallucination in Video Large Language Models via Self-Diagnostic Contrastive Decoding](https://arxiv.org/abs/2512.04643) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--season--2512-04643)). **Training-free: Yes.**

- **Intervention:** Balances spatial and temporally homogenized contrastive negatives using token-level attention divergence, without parameter learning.
- **Evaluation:** VidHalluc, VideoHallucer, and deterministic EventHallusion subtasks; general video benchmarks are reported separately.
- **Assessment:** Explicitly targets spatial and temporal video hallucinations, with direct task-specific evidence.
- **Inspected:** [Abstract; Introduction; Sections 3.3, 4.1 (Benchmarks and Metrics), and 4.2 (Hallucination Benchmark Evaluation)](https://arxiv.org/html/2512.04643v1).

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--smartsight--2512-18671"></a>

#### SmartSight

[SmartSight: Mitigating Hallucination in Video-LLMs Without Compromising Video Understanding via Temporal Attention Collapse](https://arxiv.org/abs/2512.18671) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--smartsight--2512-18671)). **Training-free: Yes.**

- **Intervention:** Selects sampled responses using Temporal Attention Collapse scores and stops weaker candidates at Visual Attention Vanishing, without training.
- **Evaluation:** Vript-HAL captions and EventHallusion QA; Video-MME and Video-MMMU are separate capability-preservation tests.
- **Assessment:** Explicitly minimizes video-response hallucinations through generation-time response selection.
- **Inspected:** [Abstract; Introduction; Sections 3.3 and 4.1](https://arxiv.org/html/2512.18671v1).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--stear--2604-03045"></a>

#### STEAR

[STEAR: Layer-Aware Spatiotemporal Evidence Intervention for Hallucination Mitigation in Video Large Language Models](https://arxiv.org/abs/2604.03045) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--stear--2604-03045)). **Training-free: Yes.**

- **Intervention:** Selects uncertain tokens, reinjects frozen projected evidence in middle layers, and contrasts temporal counterfactuals in later decoding layers.
- **Evaluation:** EventHallusion and VidHalluc, with NExT-QA and MVBench general evaluation; complete cross-backbone runs are not reported for every benchmark.
- **Assessment:** Explicit spatiotemporal hallucination mitigation. The inspected version states reinjection tensors are constructed at inference without learned additions.
- **Inspected:** [Abstract; Introduction; Sections 3.3 and 4.1](https://arxiv.org/html/2604.03045v1).

<a id="method-mitigation--referential-inconsistency--character-conflation--strand-trajectory-reasoning--2609-29607"></a>

#### STRAND (Trajectory Reasoning)

[STRAND: Benchmarking and Improving Object-Centric Spatio-Temporal Monitoring in Video Large Language Models](https://arxiv.org/abs/2609.29607) ([catalog entry](../README.md#paper-mitigation--referential-inconsistency--character-conflation--strand-trajectory-reasoning--2609-29607)). **Training-free: Yes.**

- **Intervention:** Builds object trajectories through prompted state extraction and aggregation, then retrieves trajectories to answer each query without parameter updates.
- **Evaluation:** STRAND unconditional joint Faithful Accuracy and VideoHallucer, separated from general Video-MME and EgoSchema accuracy.
- **Assessment:** Directly targets hallucinated object states, relations, and temporal reasoning. Conditional consistency alone is not the primary faithfulness measure.
- **Inspected:** [Abstract; Introduction; Section 5 overview; Sections 6.1 and 6.2](https://arxiv.org/html/2609.29607v1).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--structured-rewards--2604-01460"></a>

#### Structured Rewards

[Reinforcing Consistency in Video MLLMs with Structured Rewards](https://arxiv.org/abs/2604.01460) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--structured-rewards--2604-01460)). **Training-free: No.**

- **Intervention:** Trains caption policies with structured factual scene-graph, temporal, and video-grounded VQA rewards using sequence-level REINFORCE.
- **Evaluation:** VideoHallucer and EventHallusion, with temporal/general QA metrics separately reported.
- **Assessment:** Reducing unsupported factual and temporal caption content is central, rather than an incidental consequence of generic QA optimization.
- **Inspected:** [Abstract; Introduction; Section 3.3; Sections 4.1 benchmarks and 4.2 hallucination evaluation](https://arxiv.org/html/2604.01460v2).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--taae--2505-12826"></a>

#### TAAE

[Mitigating Hallucination in VideoLLMs via Temporal-Aware Activation Engineering](https://arxiv.org/abs/2505.12826) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--taae--2505-12826)). **Training-free: No.**

- **Intervention:** Trains a temporal-variation classifier and computes activation offsets to select and intervene in hallucination-sensitive modules.
- **Evaluation:** VidHalluc action/order/scene scores and EventHallusion binary accuracy.
- **Assessment:** Direct video-hallucination mitigation. No LLM fine-tuning does not mean training-free: the auxiliary classifier is learned.
- **Inspected:** [Abstract; Introduction; Sections 4.1-4.2](https://arxiv.org/html/2505.12826v1).

<a id="method-mitigation--context-driven-fabrication--object-action-hallucination--tcd--2409-16597"></a>

#### TCD

[EventHallusion: Diagnosing Event Hallucinations in Video LLMs](https://arxiv.org/abs/2409.16597) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--object-action-hallucination--tcd--2409-16597)). **Training-free: Yes.**

- **Intervention:** Contrasts original-video logits with temporally downsampled-video logits during decoding.
- **Evaluation:** EventHallusion binary accuracy on three video-language backbones.
- **Assessment:** Explicit event-hallucination mitigation without training; improvements are benchmark-specific and not universal per-subset gains.
- **Inspected:** [Abstract; Introduction; Temporal Contrastive Decoding; TCD Evaluation (implementation and effectiveness)](https://arxiv.org/html/2409.16597v6).

<a id="method-mitigation--spatiotemporal-dynamics--duration-distortion--temporal-insight--2401-09861"></a>

#### Temporal Insight

[Temporal Insight Enhancement: Mitigating Temporal Hallucination in Multimodal Large Language Models](https://arxiv.org/abs/2401.09861) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--duration-distortion--temporal-insight--2401-09861)). **Training-free: Yes.**

- **Intervention:** Decomposes event queries, retrieves timestamp evidence with fixed CLIP/BLIP2, and prompts GPT-3.5 to correct video-model responses.
- **Evaluation:** Charades-STA-derived timestamp R@1/R@5 and event-order Yes/No accuracy. This operationalizes temporal errors, not free-form object hallucination rates.
- **Assessment:** Temporal-hallucination correction is the explicit central contribution; retain with the narrower event-time/order definition and metric caveat.
- **Inspected:** [Abstract; Introduction; Section 3.3; Sections 4.1-4.2](https://arxiv.org/html/2401.09861v1).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--tricd--2602-00559"></a>

#### TriCD

[Learning to Decode Against Compositional Hallucination in Video Multimodal Large Language Models](https://arxiv.org/abs/2602.00559) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--tricd--2602-00559)). **Training-free: No.**

- **Intervention:** Trains perturbation-selection and saliency-fusion controllers with REINFORCE, then combines original, negative, and positive decoding branches.
- **Evaluation:** OmniVCHall isolated and compositional yes/no and multiple-choice accuracy.
- **Assessment:** Dedicated compositional video-hallucination mitigation. Frozen VLLM weights do not make the learned controllers training-free.
- **Inspected:** [Abstract; Introduction; Sections 3.4 and 4.3](https://arxiv.org/html/2602.00559v1).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--vader--2608-08622"></a>

#### VADER

[VADER: Adaptive Debiasing for Hallucination Mitigation in Video Large Language Models](https://arxiv.org/abs/2608.08622) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--vader--2608-08622)). **Training-free: Yes.**

- **Intervention:** Combines input-conditioned attention reallocation and per-frame evidence erasure with contrastive decoding; all model parameters remain frozen.
- **Evaluation:** VidHalluc, VideoHallucer, EventHallusion, with general video benchmarks reported separately.
- **Assessment:** Direct video-hallucination mitigation. Training-free does not mean hyperparameter-free; the source reports source-setting calibration.
- **Inspected:** [Abstract; Introduction; Sections 3.4 and 4.1](https://arxiv.org/html/2608.08622v1).

<a id="method-mitigation--referential-inconsistency--character-conflation--videoplr--2511-18463"></a>

#### Video-DPL

[Decoupling Perception from Reasoning for Hallucination-Resistant Video Understanding](https://arxiv.org/abs/2511.18463) ([catalog entry](../README.md#paper-mitigation--referential-inconsistency--character-conflation--videoplr--2511-18463)). **Training-free: No.**

- **Intervention:** Learns a Factual-Aware Evaluator and uses segment-level anti-hallucination plus answer-evidence consistency rewards for video reasoning post-training.
- **Evaluation:** Section 5.2 evaluates the FAE detector on VideoHallucer, reformatted HAVEN, and VidHalluc MCQ; downstream policy evaluation and reward analysis are distinct.
- **Assessment:** Unsupported perceptual evidence is directly penalized in the central training design. Detector accuracy is not a downstream generation hallucination rate.
- **Inspected:** [Abstract; Introduction; Section 4.2; Sections 5.2 and 5.5](https://arxiv.org/html/2511.18463v3).

<a id="method-mitigation--spatiotemporal-dynamics--event-misordering--video-thinking-tdpo--2503-19622"></a>

#### Video-thinking (TDPO)

[Exploring Hallucination of Large Multimodal Models in Video Understanding: Benchmark, Analysis and Mitigation](https://arxiv.org/abs/2503.19622) ([catalog entry](../README.md#paper-mitigation--spatiotemporal-dynamics--event-misordering--video-thinking-tdpo--2503-19622)). **Training-free: No.**

- **Intervention:** LoRA supervised reasoning fine-tuning followed by thinking-based DPO that upweights human-corrected hallucinated reasoning segments.
- **Evaluation:** HAVEN hallucination accuracy and consistency/bias scores. Training includes replicated-image videos, but evaluation uses video questions.
- **Assessment:** A dedicated video-hallucination mitigation contribution; TDPO means thinking-based, not temporal, DPO.
- **Inspected:** [Abstract; Introduction; Sections 5.1-5.3 (Tables 5-6)](https://arxiv.org/html/2503.19622v1).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--videohallu-grpo--2505-01481"></a>

#### VideoHallu-GRPO

[VideoHallu: Evaluating and Mitigating Multi-modal Hallucinations on Synthetic Video Understanding](https://arxiv.org/abs/2505.01481) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--videohallu-grpo--2505-01481)). **Training-free: No.**

- **Intervention:** Reported GRPO post-training mixes counterintuitive synthetic-video QA and real-video QA, with a ROUGE-based answer reward.
- **Evaluation:** VideoHallu counterintuitive-video answer accuracy, with MMVU and MVBench checking general performance.
- **Assessment:** The method explicitly counters language/physics priors overriding visible video evidence. This is a video-understanding intervention, not video-generation quality control. Implementation was not replicated: the source's Equation 2 has a pairwise DPO form despite its GRPO label, whereas the training narrative names Open-R1 and a ROUGE reward.
- **Inspected:** [Abstract; Introduction; Section 3.2 Method Overview, experimental setup, and Tables 2-3](https://arxiv.org/html/2505.01481v4).

<a id="method-mitigation--context-driven-fabrication--scene-event-hallucination--stscd--2601-22574"></a>

#### ViSSRes

[Enhancing Video Representations with Spatiotemporal-Semantic Residual to Mitigate Hallucinations in Video Large Multimodal Models](https://arxiv.org/abs/2601.22574) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--scene-event-hallucination--stscd--2601-22574)). **Training-free: No.**

- **Intervention:** Trains a residual MLP aligner for spatiotemporal and semantic consistency with a frozen backbone.
- **Evaluation:** VideoHallucer, EventHallusion, and VideoHallu; ActivityNet-QA and MMVU assess general ability.
- **Assessment:** Explicit video-hallucination mitigation. Inference-time insertion and a frozen backbone do not make the learned aligner training-free.
- **Inspected:** [Abstract; Introduction; Section 4.3; Section 5.1 evaluations](https://arxiv.org/html/2601.22574v2).

<a id="method-mitigation--referential-inconsistency--character-conflation--vista-llama--2312-08870"></a>

#### Vista-LLaMA

[Vista-LLaMA: Reducing Hallucination in Video Language Models via Equal Distance to Visual Tokens](https://arxiv.org/abs/2312.08870) ([catalog entry](../README.md#paper-mitigation--referential-inconsistency--character-conflation--vista-llama--2312-08870)). **Training-free: No.**

- **Intervention:** Changes visual-text relative-position attention and trains a sequential visual projector while freezing vision/language backbones.
- **Evaluation:** General VideoQA accuracy and GPT-assisted generation quality/consistency, with qualitative hallucination cases; no dedicated hallucination-rate benchmark in the inspected evaluation.
- **Assessment:** The design explicitly targets hallucinated video descriptions, so retain as early direct-focus work with an evidence-strength caveat. Do not present general QA scores as a measured hallucination reduction.
- **Inspected:** [Abstract; Introduction; Sections 3.4 and 4.1; Section 8 Discussion](https://arxiv.org/html/2312.08870v2).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--vistadpo--2504-13122"></a>

#### VistaDPO

[VistaDPO: Video Hierarchical Spatial-Temporal Direct Preference Optimization for Large Video Models](https://arxiv.org/abs/2504.13122) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--vistadpo--2504-13122)). **Training-free: No.**

- **Intervention:** Trains instance-, temporal-, and perceptive-level DPO with spatially and temporally grounded preferences.
- **Evaluation:** VideoHallucer and EventHallusion; general QA and caption quality are separate.
- **Assessment:** Directly targets video-language misalignment and hallucinated responses with dedicated evaluation.
- **Inspected:** [Abstract; Introduction; Sections 5.2 and 6.1](https://arxiv.org/html/2504.13122v1).

<a id="method-mitigation--context-driven-fabrication--both-object-action-scene-event--vthm-moe--2604-17375"></a>

#### VTHM-MoE

[When Text Hijacks Vision: Benchmarking and Mitigating Text Overlay-Induced Hallucination in Vision Language Models](https://arxiv.org/abs/2604.17375) ([catalog entry](../README.md#paper-mitigation--context-driven-fabrication--both-object-action-scene-event--vthm-moe--2604-17375)). **Training-free: No.**

- **Intervention:** Trains patch scoring, query conditioning, and routed experts to disentangle misleading overlay text from native video evidence.
- **Evaluation:** VisualTextTrap resistance, vulnerability, answer-shift and conflict-intensity metrics under positive/negative/neutral overlays.
- **Assessment:** Directly targets text-overlay-induced hallucinated video claims; learned auxiliary modules mean training is required.
- **Inspected:** [Abstract; Introduction; Sections 5.5 and 6.3](https://arxiv.org/html/2604.17375v1).

## Maintenance

Evidence, recommendations, and original contribution snapshots are in [`data/method_review.json`](../data/method_review.json). Baseline: [`ccbf469`](https://github.com/hukcc/Awesome-Video-Hallucination/commit/ccbf4692d3dbce955b15feeda0c8776d10153018). Regenerate with `python3 scripts/generate_method_review.py`. Tests enforce complete method coverage, training flags, preserved identities/resources, and retention of pending candidates. Scope moves require explicit human approval and a synchronized README, browser, taxonomy, and audit update.
