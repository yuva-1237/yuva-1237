<div align="center">

# Dr. Yuvathilagan (YUVA THILAGAN) — Researcher & Engineer

**AI Systems · Software Engineering · Design Engineering**

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=2400&pause=700&color=00D8FF&center=true&vCenter=true&width=920&lines=Research-Driven+AI+%7C+Reproducible+Systems+%7C+Responsible+Design" alt="typing" />
</p>

<p align="center">
  [![Profile Views](https://komarev.com/ghpvc/?username=yuva-1237&label=Profile%20Views&color=00d8ff&style=flat-square)](https://github.com/yuva-1237)
  &nbsp;&nbsp;
  ![Followers](https://img.shields.io/github/followers/yuva-1237?label=Followers&style=flat-square&color=00d8ff)
  ![Stars](https://img.shields.io/github/stars/yuva-1237?label=Stars&style=flat-square&color=7c3aed)
  ![Top Language](https://img.shields.io/github/languages/top/yuva-1237/yuva-1237?style=flat-square&color=0d1117)
</p>

</div>

---

Table of contents
- [Abstract](#abstract)
- [Snapshot](#snapshot)
- [Selected Projects](#selected-projects)
  - [BotZone (case study)](#botzone-case-study)
  - [Project Hail Mary](#project-hail-mary)
  - [IA Zone](#ia-zone)
- [Research Interests & Methods](#research-interests--methods)
- [Technical Competence](#technical-competence)
- [Reproducibility & Quick Start](#reproducibility--quick-start)
- [UI / UX Improvements (recommendations & quick fixes)](#ui--ux-improvements-recommendations--quick-fixes)
- [Publications & Citations](#publications--citations)
- [Contact](#contact)

---

Abstract
--------

> I design, implement, and evaluate interpretable AI systems with an emphasis on reproducibility, privacy, and product-quality user experiences. This repository is a living dossier of my research and engineering work.


## Snapshot

- Student: Computer Science Engineering — Prathyusha Engineering College
- Roles: Researcher · AI Engineer · Software Engineer · Design Engineer
- Focus: Agentic AI, RAG, local LLM stacks, reproducible pipelines, UX-driven interfaces
- Contact: [yuvathilagan@gmail.com](mailto:yuvathilagan@gmail.com) · [Portfolio](https://yuvathilagan-portfolio.vercel.app/)

---

Selected Projects (short)
- BotZone — Local & Private Multimodal RAG Platform · Repo: https://github.com/yuva-1237/BotZone
- Project Hail Mary — Autonomous Multi-Agent Decision Intelligence · Repo: https://github.com/yuva-1237/Project_hail_mary
- IA Zone — AI Gateway & Assistant Hub (live demo) · https://ia-zone.vercel.app/ · Repo: https://github.com/yuva-1237/ia-zone
- ARS — Intelligent Resume Screener · Repo: https://github.com/yuva-1237/ARS
- Exam Forge — Online Examination Platform

---

BotZone (case study)
---------------------

<details>
<summary>Click to expand the full BotZone case study (background, methods, results, lessons)</summary>

### Background

Enterprises and privacy-conscious users require document intelligence without sending sensitive data to remote APIs. BotZone is a local-first, multimodal RAG workspace that supports OCR and audio transcription for private document querying.

### Objectives

- Private, offline-capable RAG with deterministic pipelines
- Multimodal support (text, scanned docs, audio)
- Reproducible evaluation and deterministic runs

### Architecture (high-level)

1. Ingestion: PDF/text ingestion, layout-aware OCR (EasyOCR/Tesseract), Whisper for audio.
2. Embeddings & storage: local embeddings (Ollama/HF), Chroma/FAISS vector store.
3. Retrieval & reranking: vector similarity + lexical reranker.
4. Generation: local LLM inference (Ollama/LLaMA family) with agentic tool calls sandboxed.
5. Evaluation: seeded benchmarks, human-in-the-loop QA.

### Representative results (example — run benchmarks to replace)
- Ingestion throughput: ~50 pages/min on 4-core laptop.
- Retrieval latency (10k docs): median 45 ms (Chroma+FAISS).
- End-to-end median query latency: ~1.2s (small/medium local LLM).
- Example QA exact-match: 81% on an internal 200-question set.

### Lessons learned
- OCR quality dominates downstream QA; invest in layout-aware models and post-correction.
- Lexical reranking often improves accuracy more cost-effectively than larger LLMs.
- Expose provenance to users — it increases trust and debugability.

### Artifacts
- Repo: https://github.com/yuva-1237/BotZone
- Local demo / quickstart: see next section

</details>

---

Project Hail Mary — short

- Multi-agent orchestration for time-critical decision-making under delayed communications. Uses a simulated digital twin and Monte Carlo policy evaluation to maintain safety constraints. Repo: https://github.com/yuva-1237/Project_hail_mary

---

IA Zone — short

- Multilingual assistant gateway with real-time context adaptation and a 3D agentic companion. Live demo: https://ia-zone.vercel.app/ · Repo: https://github.com/yuva-1237/ia-zone

---

Research Interests & Methods
----------------------------

- Foundations of LMs: robustness, alignment, evaluation
- RAG: retrieval fidelity, latency vs accuracy tradeoffs
- Agentic architectures: planners, tool integration, safety
- Private inference: on-premise LLM deployments, multimodal privacy

Methodological commitments: reproducibility (seed control, containers), interpretability (provenance, structured logs), and safety (minimize external APIs for sensitive data).

---

Technical Competence
--------------------

- Languages: Python, TypeScript, Java, C/C++
- ML & tools: PyTorch, TensorFlow, Hugging Face, LangChain, LlamaIndex, Ollama
- Data infra: Postgres, MongoDB, Redis, Pinecone, Chroma, FAISS
- Deployment: FastAPI, Docker, GitHub Actions, Vercel, Kubernetes (optional)

---

Reproducibility & Quick Start (BotZone example)

Recommended quickstart (local developer environment):

```bash
# clone
git clone https://github.com/yuva-1237/BotZone.git
cd BotZone

# optional: create venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# start local demo (Docker Compose if present)
docker-compose up --build
# or run backend locally
uvicorn app.main:app --reload
```

For reproducible evaluation:
- Ensure experiment-config.yaml exists and contains a random seed
- Use the provided `eval/run_benchmarks.py --config experiment-config.yaml` script (if present)

---

Visuals & Assets (improve README UX)

- Place project GIFs/screenshots in `.github/assets/` and reference them as raw URLs.
- Use centered images and short captions. Example:

<p align="center">
  <img alt="BotZone demo" src="https://raw.githubusercontent.com/yuva-1237/yuva-1237/main/.github/assets/botzone-demo.gif" width="720" />
  <br/>
  <em>BotZone — local multimodal RAG (replace with production GIF)</em>
</p>

---

UI / UX Improvements — recommendations & quick fixes
----------------------------------------------------

I reviewed the projects and README design and recommend the following prioritized improvements you can apply quickly. I include exact, copy-paste snippets or design guidance where helpful.

1) README / Project-level UX (low effort, high impact)
- Add a clear hero with a one-line value proposition (done).  
- Add a Table of Contents and expandable sections for long content (done).  
- Add centered GIFs/screenshots for visual proof (place assets in `.github/assets/`) — examples above.
- Add badges for quick signals: build status, license, top language, followers (placeholders added).

2) Web UI / Frontend UX improvements (BotZone, IA Zone, Exam Forge)
- Onboarding flow: display a "How it works" 3-step overlay for first-time users.  
- Provenance panel: always show source snippets + page link for every generated answer.  
- Error states: show graceful fallbacks and provide actionable next steps (retry, fallback to keyword search).  
- Accessibility: ensure color contrast, keyboard navigation, and ARIA attributes for interactive components.

Quick snippet — Provenance panel component (React + Tailwind)

```jsx
// ProvenancePanel.jsx (simplified)
export function ProvenancePanel({sources}){
  return (
    <aside className="p-4 bg-neutral-900 rounded-md text-sm">
      <h4 className="font-semibold">Sources</h4>
      <ul className="mt-2 space-y-2">
        {sources.map(s => (
          <li key={s.id} className="flex items-start">
            <a href={s.url} className="text-blue-300 underline mr-2">{s.title}</a>
            <p className="text-gray-300 text-xs">"{s.snippet}"</p>
          </li>
        ))}
      </ul>
    </aside>
  )
}
```

3) Design system & consistency (medium effort)
- Create a small design token file (colors, spacing, type scale) and a central CSS/Tailwind config.  
- Apply consistent card components for results, provenance, and error states.

Design token example (tailwind.config.js snippet)

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#00D8FF',
        accent: '#7C3AED',
        bg: '#0D1117'
      }
    }
  }
}
```

4) UX metrics & instrumentation (important for product decisions)
- Add lightweight analytics: event counts for searches, average query latency, user clicks on sources.  
- Track qualitative feedback: thumbs up/down per answer + optional comment box.

5) Rapid A/B idea (fast experiment)
- Test two response layouts: (A) single answer + provenance list vs (B) short answer + expandable deep-dive. Measure time-to-click and satisfaction.

---

Publications & Citations (BibTeX + human)

```bibtex
@techreport{botzone2026,
  title = {BotZone: A Private, Local-First Multimodal Retrieval-Augmented Workspace},
  author = {Yuvathilagan, Y.},
  institution = {yuva-1237 / Personal Research},
  year = {2026},
  url = {https://github.com/yuva-1237/BotZone}
}

@techreport{hailmary2026,
  title = {Project Hail Mary: Multi-Agent Decision Intelligence under Communication Latency},
  author = {Yuvathilagan, Y.},
  institution = {yuva-1237 / Personal Research},
  year = {2026},
  url = {https://github.com/yuva-1237/Project_hail_mary}
}
```

Human-readable

- Y. Yuvathilagan. BotZone: A Private, Local-First Multimodal Retrieval-Augmented Workspace. 2026. https://github.com/yuva-1237/BotZone
- Y. Yuvathilagan. Project Hail Mary: Multi-Agent Decision Intelligence under Communication Latency. 2026. https://github.com/yuva-1237/Project_hail_mary

---

Contact
-------

<p align="center">
  <a href="mailto:yuvathilagan@gmail.com" style="margin-right:12px">📧 Email</a>
  <a href="https://www.linkedin.com/in/yuvathilagan-%E2%80%8C-806681308/" style="margin-right:12px">🔗 LinkedIn</a>
  <a href="https://yuvathilagan-portfolio.vercel.app/">🌐 Portfolio</a>
</p>

---

Acknowledgements
----------------

Prepared with scholarly rigor and an engineer's pragmatism — Yuvathilagan.

