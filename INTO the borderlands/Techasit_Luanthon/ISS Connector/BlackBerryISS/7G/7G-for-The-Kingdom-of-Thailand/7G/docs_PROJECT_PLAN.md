# 12–24 Month Project Plan — Techasit 7G Research Platform (Thailand)

Purpose
Build a private experimental 7G research network in Thailand that demonstrates:
- THz links (short-range, high-capacity)
- Reconfigurable Intelligent Surfaces (RIS)
- Holographic / extremely-large MIMO arrays
- O‑RAN aligned disaggregated RAN with near-RT RIC xApps for AI-native control
- Integrated sensing & communications (ISAC)
- Quantum-resistant control plane security (PQC)

High-level timeline
Phase 0 — Setup & approvals (Months 0–3)
- Appoint project lead, regulatory lead, and systems architect.
- Define 2–3 priority demos (e.g., THz XR streaming, RIS coverage boost, ISAC localization).
- Apply for experimental/test license with NBTC (start immediately).
- Reserve lab/anechoic chamber or campus test area (university partner suggested).
- Order long-lead items (SDRs, THz frontends).

Phase 1 — Core testbed (Months 4–9)
- Install SDRs, frontends, edge servers, measurement gear.
- Deploy O‑RAN experimental stack (community O‑RAN SC / srsRAN / OAI) + private core (Open5GS).
- Implement data collection and ML pipelines.
- Demonstrate baseline THz link and capture channel soundings.

Phase 2 — Advanced features & AI control (Months 10–15)
- Integrate RIS and holographic-MIMO prototypes; provide control via near-RT RIC xApps.
- Develop semantic encoder/decoder for a target vertical (XR/robotics).
- Demonstrate ISAC (detection/localization) using communications waveforms.
- Integrate PQC into control plane prototypes.

Phase 3 — Field pilot & standards contributions (Months 16–24)
- Field demo at a controlled outdoor/indoor site (campus or industrial park).
- Publish datasets, whitepapers; contribute findings to O‑RAN, ITU study groups, and 3GPP study items where possible.
- Run partner demos and begin IP capture & funding outreach.

Regulatory steps (Thailand)
- Contact NBTC (National Broadcasting and Telecommunications Commission) for experimental/test license procedures.
- Prepare technical annex with frequency bands requested, ERP, test location, safety measures, interference mitigation, and test dates.
- Provide institutional sponsor letter (Techasit + host university or campus).
- Keep NBTC informed and request site inspections if asked.

Suggested Thai partners & funding sources (examples)
- Universities: Chulalongkorn University, King Mongkut’s University of Technology Thonburi (KMUTT), Mahidol University — for lab space and research collaboration.
- Government/Research: NSTDA (National Science and Technology Development Agency) for funding/collab.
- Industry partners: local carriers (AIS/True/DTAC) for future partnerships; international vendors for equipment.
- International collaborators: research labs in EU/Japan/US for THz hardware and expertise.

Team (initial hires)
- Project Lead (1)
- RF / PHY researchers (2–4)
- Systems / RAN engineers (2–3)
- ML / AI engineers (2)
- Security engineer (PQC) (1)
- Test & instrumentation engineer (1)
- DevOps / Cloud engineer (1)
- Program manager / partnerships (1)

Key deliverables (by month 24)
- Working private network demo(s) showing THz + RIS + AI RIC control.
- Published dataset (channel soundings, RIS configs).
- 3+ technical contributions/whitepapers for standards fora.
- Partner demo events and initial funding proposals.

KPIs
- THz lab link: demonstrated Gbps-level PHY throughput in short-range LOS (report throughput/BER).
- RIS: measurable coverage / SNR improvement vs baseline.
- Semantic demo: % bitrate reduction for target QoE.
- ISAC: localization accuracy (cm-level target in constrained setting).
- PQC integration: successful authenticated control messages using PQC algorithms.

Budget guide (very rough)
- Minimal academic testbed: ~$500k–1.5M USD
- Industry-grade lab: $1.5M–6M USD (recommended)
- Pilot expansion & device work: $6M–25M+

Risks & mitigations
- THz hardware availability: partner with THz vendors and university labs; start with mmWave fallback.
- Regulatory delays: apply early and maintain dialogue with NBTC.
- Integration complexity: use modular architecture and incremental tests.

Immediate next steps (choose one)
- I can prepare a draft NBTC experimental license application (I included a template).
- I can produce an itemized procurement spreadsheet with vendor links and lead times.
- I can produce a week-by-week 12-month Gantt schedule based on an exact budget.

Provide: preferred budget band and whether you already have lab space or a local university partner.