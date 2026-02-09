<div align="center">

# Awesome-Video-Hallucination [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

### Distorted or Fabricated? A Survey on Hallucination in Video LLMs

*Yiyang Huang<sup>1</sup>, Yitian Zhang<sup>1</sup>, Yizhou Wang<sup>1</sup>, Mingyuan Zhang<sup>1</sup>, Liang Shi<sup>1</sup>, Huimin Zeng<sup>1</sup>, Yun Fu<sup>1,2</sup>*

<sup>1</sup>Department of Electrical and Computer Engineering, Northeastern University
<br>
<sup>2</sup>Khoury College of Computer Science, Northeastern University

<br>

[![TechRxiv](https://img.shields.io/badge/TechRxiv-Paper-blue?style=for-the-badge&logo=arxiv)](# )
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Papers](https://img.shields.io/badge/Papers-42-red?style=for-the-badge)](#evaluation-benchmarks)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](https://github.com)

<br>

<img src="imgs/teaser.png" width="96%" />

<br>

A curated and structured collection of papers on **hallucination in Video Large Language Models (Vid-LLMs)**,<br>covering **19 evaluation benchmarks** and **23 mitigation methods**.<br>
All papers are organized according to our mechanism-driven taxonomy,<br>which classifies video hallucinations into *Dynamic Distortion* and *Content Fabrication*.

</div>

---

<details open>
<summary><b>📖 Table of Contents</b></summary>

&emsp;📋 [Taxonomy of Video Hallucinations](#taxonomy-of-video-hallucinations)
<br>&emsp;📊 [Evaluation Benchmarks](#evaluation-benchmarks) — 19 benchmarks
<br>&emsp;&emsp;&emsp;🔵 [Spatiotemporal Dynamics](#-spatiotemporal-dynamics-benchmarks-dynamic-distortion) · 🟢 [Referential Inconsistency](#-referential-inconsistency-benchmarks-dynamic-distortion) · 🟠 [Context-Driven Fabrication](#-context-driven-fabrication-benchmarks-content-fabrication) · 🟣 [Audio-Visual Conflict](#-audio-visual-conflict-benchmarks-content-fabrication)
<br>&emsp;🛠️ [Mitigation Strategies](#mitigation-strategies) — 23 methods
<br>&emsp;&emsp;&emsp;🔵 [Spatiotemporal Dynamics](#-spatiotemporal-dynamics-mitigation-dynamic-distortion) · 🟢 [Referential Inconsistency](#-referential-inconsistency-mitigation-dynamic-distortion) · 🟠 [Context-Driven Fabrication](#-context-driven-fabrication-mitigation-content-fabrication) · 🟣 [Audio-Visual Conflict](#-audio-visual-conflict-mitigation-content-fabrication)
<br>&emsp;🤝 [Contributing](#contributing)

</details>

---

## Overview at a Glance

<table>
<tr>
<td align="center"><small><b>📊 19</b><br><sub>Evaluation<br>Benchmarks</sub></small></td>
<td align="center"><small><b>🛠️ 23</b><br><sub>Mitigation<br>Methods</sub></small></td>
<td align="center"><small><b>🔷 2</b><br><sub>Primary Hallucination<br>Types</sub></small></td>
<td align="center"><small><b>📂 4</b><br><sub>Sub-<br>Categories</sub></small></td>
<td align="center"><small><b>🏛️ 15+</b><br><sub>Top-tier<br>Venues</sub></small></td>
<td align="center"><small><b>📅 2023–2026</b><br><sub>Coverage<br>Period</sub></small></td>
</tr>
</table>

---

## Taxonomy of Video Hallucinations

We propose a **mechanism-driven taxonomy** that classifies hallucinations in Video Large Language Models (Vid-LLMs) into two primary types:

<table>
<tr>
<td width="50%" valign="top">

🔷 **Dynamic Distortion**

The model correctly detects entities but misrepresents their temporal progression or referential consistency.

- 🔵 *Spatiotemporal Dynamics* — Errors in event ordering, duration estimation, or frequency counting.
- 🟢 *Referential Inconsistency* — Characters or scenes are conflated across temporal boundaries.

</td>
<td width="50%" valign="top">

🔶 **Content Fabrication**

The model produces outputs that lack grounding in visual evidence and are instead influenced by learned priors.

- 🟠 *Context-Driven Fabrication* — Common object-action or scene-event associations lead to unsupported predictions.
- 🟣 *Audio-Visual Conflict* — Dominant auditory cues override visual input.

</td>
</tr>
</table>

<p align="center">
    <img src="imgs/taxonomy.png" width="96%" />
    <br>
    <em>Mechanism-driven taxonomy of Vid-LLM hallucinations. Solid fill = benchmarks; striped fill = mitigation methods.</em>
</p>

---

## Evaluation Benchmarks

> [!NOTE]
> Benchmarks are organized by our mechanism-driven taxonomy. Each entry includes venue, date, and links to code/project pages where available.
>
> **Legend:** <a href="#"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> = Project Page &ensp; <a href="#"><img src="https://img.shields.io/github/stars/octocat/Hello-World?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a> = GitHub Repository &ensp; `-` = Not Available

### 🔵 Spatiotemporal Dynamics Benchmarks (Dynamic Distortion)

<details open>
<summary><b>Event Misordering</b> (4 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2412.03735"><b>VidHalluc: Evaluating Temporal Hallucinations in Multimodal Large Language Models for Video Understanding</b></a></small></td>
      <td align="center"><small>VidHalluc</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>12/2024</small></td>
      <td align="center"><small><a href="https://people-robots.github.io/vidhalluc"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/CyL97/VidHalluc"><img src="https://img.shields.io/github/stars/CyL97/VidHalluc?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2503.19622"><b>Exploring Hallucination of Large Multimodal Models in Video Understanding: Benchmark, Analysis and Mitigation</b></a></small></td>
      <td align="center"><small>HAVEN</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>03/2025</small></td>
      <td align="center"><small><a href="https://github.com/Hongcheng-Gao/HAVEN"><img src="https://img.shields.io/github/stars/Hongcheng-Gao/HAVEN?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://ojs.aaai.org/index.php/AAAI/article/view/32463"><b>MHBench: Demystifying Motion Hallucination in VideoLLMs</b></a></small></td>
      <td align="center"><small>MHBench</small></td>
      <td align="center"><small>AAAI 2025</small></td>
      <td align="center"><small>01/2025</small></td>
      <td align="center"><small><a href="https://github.com/xzhouzeng/MHBench"><img src="https://img.shields.io/github/stars/xzhouzeng/MHBench?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2506.07371"><b>ARGUS: Hallucination and Omission Evaluation in Video-LLMs</b></a></small></td>
      <td align="center"><small>ARGUS</small></td>
      <td align="center"><small>ICCV 2025</small></td>
      <td align="center"><small>06/2025</small></td>
      <td align="center"><small><a href="https://github.com/JARVVVIS/argus"><img src="https://img.shields.io/github/stars/JARVVVIS/argus?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Duration Distortion</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2406.16338"><b>VideoHallucer: Evaluating Intrinsic and Extrinsic Hallucinations in Large Video-Language Models</b></a></small></td>
      <td align="center"><small>VideoHallucer</small></td>
      <td align="center"><small>arXiv 2024</small></td>
      <td align="center"><small>06/2024</small></td>
      <td align="center"><small><a href="https://github.com/patrick-tssn/VideoHallucer"><img src="https://img.shields.io/github/stars/patrick-tssn/VideoHallucer?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2501.00584"><b>Online Video Understanding: OVBench and VideoChat-Online</b></a></small></td>
      <td align="center"><small>OVBench</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>01/2025</small></td>
      <td align="center"><small><a href="https://videochat-online.github.io/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/mcg-nju/videochat-online"><img src="https://img.shields.io/github/stars/mcg-nju/videochat-online?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Frequency Confusion</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2411.16771"><b>VidHal: Benchmarking Temporal Hallucinations in Vision LLMs</b></a></small></td>
      <td align="center"><small>VidHal</small></td>
      <td align="center"><small>arXiv 2024</small></td>
      <td align="center"><small>11/2024</small></td>
      <td align="center"><small><a href="https://github.com/Lookuz/VidHal"><img src="https://img.shields.io/github/stars/Lookuz/VidHal?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2406.06040"><b>Vript: A Video Is Worth Thousands of Words</b></a></small></td>
      <td align="center"><small>Vript</small></td>
      <td align="center"><small>NeurIPS 2024</small></td>
      <td align="center"><small>06/2024</small></td>
      <td align="center"><small><a href="https://github.com/mutonix/Vript"><img src="https://img.shields.io/github/stars/mutonix/Vript?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟢 Referential Inconsistency Benchmarks (Dynamic Distortion)

<details open>
<summary><b>Character Conflation</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://aclanthology.org/2025.emnlp-main.1446/"><b>EGOILLUSION: Benchmarking Hallucinations in Egocentric Video Understanding</b></a></small></td>
      <td align="center"><small>EGOILLUSION</small></td>
      <td align="center"><small>EMNLP 2025</small></td>
      <td align="center"><small>11/2025</small></td>
      <td align="center"><small><a href="https://sites.google.com/view/egoillusion-demo/home"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2509.08538"><b>MESH: Measuring Hallucinations in Large Video Models</b></a></small></td>
      <td align="center"><small>MESH</small></td>
      <td align="center"><small>ACM MM 2025</small></td>
      <td align="center"><small>09/2025</small></td>
      <td align="center"><small><a href="https://github.com/HCYANG2000/MESH-Benchmark"><img src="https://img.shields.io/github/stars/HCYANG2000/MESH-Benchmark?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Scene Conflation</b> (1 paper)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2508.21496"><b>ELV-Halluc: Benchmarking Semantic Aggregation Hallucinations in Long Video Understanding</b></a></small></td>
      <td align="center"><small>ELV-Halluc</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>08/2025</small></td>
      <td align="center"><small><a href="https://github.com/hlsv02/ELV-Halluc"><img src="https://img.shields.io/github/stars/hlsv02/ELV-Halluc?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟠 Context-Driven Fabrication Benchmarks (Content Fabrication)

<details open>
<summary><b>Object-Action Hallucination</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.01481"><b>VideoHallu: Evaluating and Mitigating Multi-modal Hallucinations on Synthetic Video Understanding</b></a></small></td>
      <td align="center"><small>VideoHallu</small></td>
      <td align="center"><small>NeurIPS 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small><a href="https://github.com/zli12321/VideoHallu"><img src="https://img.shields.io/github/stars/zli12321/VideoHallu?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2303.02961"><b>Models See Hallucinations: Evaluating the Factuality in Video Captioning</b></a></small></td>
      <td align="center"><small>FactVC</small></td>
      <td align="center"><small>EMNLP 2023</small></td>
      <td align="center"><small>03/2023</small></td>
      <td align="center"><small><a href="https://github.com/PKULiuHui/FactVC"><img src="https://img.shields.io/github/stars/PKULiuHui/FactVC?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Scene-Event Hallucination</b> (3 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2409.16597"><b>EventHallusion: Diagnosing Event Hallucinations in Video LLMs</b></a></small></td>
      <td align="center"><small>EventHallusion</small></td>
      <td align="center"><small>arXiv 2024</small></td>
      <td align="center"><small>09/2024</small></td>
      <td align="center"><small><a href="https://github.com/Stevetich/EventHallusion"><img src="https://img.shields.io/github/stars/Stevetich/EventHallusion?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2511.06475"><b>NOAH: Benchmarking Narrative Prior driven Hallucination and Omission in Video Large Language Models</b></a></small></td>
      <td align="center"><small>NOAH</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>11/2025</small></td>
      <td align="center"><small><a href="https://anonymous550520.github.io/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/anonymous550520/NOAH"><img src="https://img.shields.io/github/stars/anonymous550520/NOAH?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://openaccess.thecvf.com/content/CVPR2025/papers/Parikh_RoadSocial_A_Diverse_VideoQA_Dataset_and_Benchmark_for_Road_Event_CVPR_2025_paper.pdf"><b>RoadSocial: A Diverse VideoQA Dataset and Benchmark for Road Event Understanding from Social Video Narratives</b></a></small></td>
      <td align="center"><small>RoadSocial</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>02/2025</small></td>
      <td align="center"><small><a href="https://roadsocial.github.io/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/roadsocial/roadsocial"><img src="https://img.shields.io/github/stars/roadsocial/roadsocial?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟣 Audio-Visual Conflict Benchmarks (Content Fabrication)

<details open>
<summary><b>Action Attribution</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2410.18325"><b>AVHBench: A Cross-Modal Hallucination Benchmark for Audio-Visual Large Language Models</b></a></small></td>
      <td align="center"><small>AVHBench</small></td>
      <td align="center"><small>ICLR 2025</small></td>
      <td align="center"><small>10/2024</small></td>
      <td align="center"><small><a href="https://github.com/kaist-ami/AVHBench"><img src="https://img.shields.io/github/stars/kaist-ami/AVHBench?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2410.12787"><b>The Curse of Multi-Modalities: Evaluating Hallucinations of Large Multimodal Models across Language, Visual, and Audio</b></a></small></td>
      <td align="center"><small>CMM</small></td>
      <td align="center"><small>arXiv 2024</small></td>
      <td align="center"><small>10/2024</small></td>
      <td align="center"><small><a href="https://cmm-damovl.site/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/DAMO-NLP-SG/CMM"><img src="https://img.shields.io/github/stars/DAMO-NLP-SG/CMM?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Emotion Inference</b> (1 paper)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="54%" align="left"><small>Title</small></th>
      <th width="12%" align="center"><small>Benchmark</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.11405"><b>EmotionHallucer: Evaluating Emotion Hallucinations in Multimodal Large Language Models</b></a></small></td>
      <td align="center"><small>EmotionHallucer</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small><a href="https://github.com/xxtars/EmotionHallucer"><img src="https://img.shields.io/github/stars/xxtars/EmotionHallucer?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

---

## Mitigation Strategies

> [!NOTE]
> Methods are classified by the type of hallucination they target. The **Training-Free** column indicates whether the method requires additional training (✘) or not (✔).

### 🔵 Spatiotemporal Dynamics Mitigation (Dynamic Distortion)

<details open>
<summary><b>Event Misordering</b> (3 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2512.04643"><b>SEASON: Mitigating Temporal Hallucination in Video LLMs via Self-Diagnostic Contrastive Decoding</b></a></small></td>
      <td align="center"><small>SEASON</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>12/2025</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small>-</small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2503.19622"><b>Exploring Hallucination of Large Multimodal Models in Video Understanding: Benchmark, Analysis and Mitigation</b></a></small></td>
      <td align="center"><small>Video-thinking (TDPO)</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>03/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/Hongcheng-Gao/HAVEN"><img src="https://img.shields.io/github/stars/Hongcheng-Gao/HAVEN?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2512.18671"><b>SmartSight: Mitigating Hallucination in Video-LLMs via Temporal Attention Collapse</b></a></small></td>
      <td align="center"><small>SmartSight</small></td>
      <td align="center"><small>AAAI 2026</small></td>
      <td align="center"><small>12/2025</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small>-</small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Duration Distortion</b> (3 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2401.09861"><b>Temporal Insight Enhancement: Mitigating Temporal Hallucination in Video Understanding by MLLMs</b></a></small></td>
      <td align="center"><small>Temporal Insight</small></td>
      <td align="center"><small>ICPR 2024</small></td>
      <td align="center"><small>01/2024</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small>-</small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2412.03735"><b>VidHalluc: Evaluating Temporal Hallucinations in Multimodal Large Language Models for Video Understanding</b></a></small></td>
      <td align="center"><small>DINO-HEAL</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>12/2024</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small><a href="https://people-robots.github.io/vidhalluc"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/CyL97/VidHalluc"><img src="https://img.shields.io/github/stars/CyL97/VidHalluc?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.12826"><b>Mitigating Hallucination in VideoLLMs via Temporal-Aware Activation Engineering</b></a></small></td>
      <td align="center"><small>TAAE</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small>-</small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Frequency Confusion</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2405.13382"><b>VTG-LLM: Integrating Timestamp Knowledge into Video LLMs for Enhanced Video Temporal Grounding</b></a></small></td>
      <td align="center"><small>VTG-LLM</small></td>
      <td align="center"><small>AAAI 2025</small></td>
      <td align="center"><small>05/2024</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/gyxxyg/VTG-LLM"><img src="https://img.shields.io/github/stars/gyxxyg/VTG-LLM?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2406.06040"><b>Vript: A Video Is Worth Thousands of Words</b></a></small></td>
      <td align="center"><small>Vriptor</small></td>
      <td align="center"><small>NeurIPS 2024</small></td>
      <td align="center"><small>06/2024</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/mutonix/Vript"><img src="https://img.shields.io/github/stars/mutonix/Vript?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟢 Referential Inconsistency Mitigation (Dynamic Distortion)

<details open>
<summary><b>Character Conflation</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2312.08870"><b>Vista-LLaMA: Reducing Hallucination in Video Language Models via Equal Distance to Visual Tokens</b></a></small></td>
      <td align="center"><small>Vista-LLaMA</small></td>
      <td align="center"><small>CVPR 2024</small></td>
      <td align="center"><small>12/2023</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://jinxxian.github.io/Vista-LLaMA/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/Flowerfan/VistaLLaMA"><img src="https://img.shields.io/github/stars/Flowerfan/VistaLLaMA?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2511.18463"><b>Alternating Perception-Reasoning for Hallucination-Resistant Video Understanding</b></a></small></td>
      <td align="center"><small>VideoPLR</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>11/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/BoweiPu/VideoPLR"><img src="https://img.shields.io/github/stars/BoweiPu/VideoPLR?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Scene Conflation</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2508.21496"><b>ELV-Halluc: Benchmarking Semantic Aggregation Hallucinations in Long Video Understanding</b></a></small></td>
      <td align="center"><small>ELV-Halluc-DPO</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>08/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/hlsv02/ELV-Halluc"><img src="https://img.shields.io/github/stars/hlsv02/ELV-Halluc?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2501.00584"><b>Online Video Understanding: OVBench and VideoChat-Online</b></a></small></td>
      <td align="center"><small>VideoChat-Online</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>01/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://videochat-online.github.io/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a> <a href="https://github.com/mcg-nju/videochat-online"><img src="https://img.shields.io/github/stars/mcg-nju/videochat-online?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟠 Context-Driven Fabrication Mitigation (Content Fabrication)

<details open>
<summary><b>Object-Action Hallucination</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2512.04356"><b>Mitigating Object and Action Hallucinations in Multimodal LLMs via Self-Augmented Contrastive Alignment</b></a></small></td>
      <td align="center"><small>SANTA</small></td>
      <td align="center"><small>WACV 2026</small></td>
      <td align="center"><small>12/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://kpc0810.github.io/santa/"><img src="https://img.shields.io/badge/Page%20%F0%9F%94%97-Link-228B22?style=flat-square&logo=readthedocs&logoColor=white" alt="page"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2409.16597"><b>EventHallusion: Diagnosing Event Hallucinations in Video LLMs</b></a></small></td>
      <td align="center"><small>TCD</small></td>
      <td align="center"><small>arXiv 2024</small></td>
      <td align="center"><small>09/2024</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small><a href="https://github.com/Stevetich/EventHallusion"><img src="https://img.shields.io/github/stars/Stevetich/EventHallusion?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Scene-Event Hallucination</b> (3 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2503.15871"><b>MASH-VLM: Mitigating Action-Scene Hallucination in Video-LLMs through Disentangled Spatial-Temporal Representations</b></a></small></td>
      <td align="center"><small>MASH-VLM</small></td>
      <td align="center"><small>CVPR 2025</small></td>
      <td align="center"><small>03/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small>-</small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2504.05810"><b>PaMi-VDPO: Mitigating Video Hallucinations by Prompt-Aware Multi-Instance Video Preference Learning</b></a></small></td>
      <td align="center"><small>PaMi-VDPO</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>04/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small>-</small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://www.ijcai.org/proceedings/2025/1019"><b>Hallucination Reduction in Video-Language Models via Hierarchical Multimodal Consistency</b></a></small></td>
      <td align="center"><small>MMA</small></td>
      <td align="center"><small>IJCAI 2025</small></td>
      <td align="center"><small>08/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small>-</small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Both Object-Action & Scene-Event</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2504.13122"><b>VistaDPO: Video Hierarchical Spatial-Temporal Direct Preference Optimization for Large Video Models</b></a></small></td>
      <td align="center"><small>VistaDPO</small></td>
      <td align="center"><small>ICML 2025</small></td>
      <td align="center"><small>04/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/HaroldChen19/VistaDPO"><img src="https://img.shields.io/github/stars/HaroldChen19/VistaDPO?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.01481"><b>VideoHallu: Evaluating and Mitigating Multi-modal Hallucinations on Synthetic Video Understanding</b></a></small></td>
      <td align="center"><small>VideoHallu-GRPO</small></td>
      <td align="center"><small>NeurIPS 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/zli12321/VideoHallu"><img src="https://img.shields.io/github/stars/zli12321/VideoHallu?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

### 🟣 Audio-Visual Conflict Mitigation (Content Fabrication)

<details open>
<summary><b>Action Attribution</b> (2 papers)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2410.18325"><b>AVHBench: A Cross-Modal Hallucination Benchmark for Audio-Visual Large Language Models</b></a></small></td>
      <td align="center"><small>AVHModel-Align-FT</small></td>
      <td align="center"><small>ICLR 2025</small></td>
      <td align="center"><small>10/2024</small></td>
      <td align="center"><small>✘</small></td>
      <td align="center"><small><a href="https://github.com/kaist-ami/AVHBench"><img src="https://img.shields.io/github/stars/kaist-ami/AVHBench?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.20862"><b>AVCD: Mitigating Hallucinations in Audio-Visual Large Language Models through Contrastive Decoding</b></a></small></td>
      <td align="center"><small>AVCD</small></td>
      <td align="center"><small>NeurIPS 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small><a href="https://github.com/kaistmm/AVCD"><img src="https://img.shields.io/github/stars/kaistmm/AVCD?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

<details open>
<summary><b>Emotion Inference</b> (1 paper)</summary>

<table width="100%">
  <thead>
    <tr>
      <th width="45%" align="left"><small>Title</small></th>
      <th width="13%" align="center"><small>Method</small></th>
      <th width="10%" align="center"><small>Venue</small></th>
      <th width="7%" align="center"><small>Date</small></th>
      <th width="8%" align="center"><small>Training-Free</small></th>
      <th width="17%" align="center"><small>Code</small></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><small><a href="https://arxiv.org/abs/2505.11405"><b>EmotionHallucer: Evaluating Emotion Hallucinations in Multimodal Large Language Models</b></a></small></td>
      <td align="center"><small>PEP-MEK</small></td>
      <td align="center"><small>arXiv 2025</small></td>
      <td align="center"><small>05/2025</small></td>
      <td align="center"><small>✔</small></td>
      <td align="center"><small><a href="https://github.com/xxtars/EmotionHallucer"><img src="https://img.shields.io/github/stars/xxtars/EmotionHallucer?style=flat-square&logo=github&label=Code%20%E2%AD%90" alt="code"></a></small></td>
    </tr>
  </tbody>
</table>

</details>

---

## Contributing

> [!TIP]
> We welcome contributions from the community! Here's how you can help:
>
> **🔀 Pull Request** — Add new papers, update code links, or correct errors
> <br>**🐛 Open an Issue** — Report mistakes, suggest missing papers, or request features

<details>
<summary><b>📝 PR Format Guide</b></summary>

<br>

Please follow this table structure when adding new entries:

```
| [**Paper Title**](paper_link) | Method/Benchmark Name | Venue | MM/YYYY | [code](code_link) |
```

</details>

---

<div align="center">

**If you find this repository helpful, please consider giving it a** ⭐

*Maintained by the [SmileLab](https://web.northeastern.edu/smilelab/) team at Northeastern University.*

</div>
