# BIS SmartHub

**BIS SmartHub** is the unified next-generation BIS intelligence and compliance platform combining the strongest capabilities of BIS SmartGuide and BIS Sahayak into one user-first experience.

## Vision

**SmartGuide intelligence + Sahayak workflows + SmartHub ecosystem.**

SmartHub helps consumers, MSMEs, manufacturers, importers, procurement teams, laboratories and compliance professionals move from a product question to an evidence-grounded action plan.

## Core experience

- 🤖 **BIS Copilot** — one conversational entry point for BIS tasks
- 👤 **Role-based modes** — Consumer, Manufacturer/MSME, Importer, Procurement, Laboratory, Compliance
- 📷 **Scan Anything** — QR, barcode, ISI/CM-L, HUID, CRS, labels and documents
- 🏭 **Product Intelligence** — product → standards → requirements
- 📋 **Compliance Workspace** — requirements, tests, documents, labs and readiness
- 📐 **CAD Compliance** — geometry analysis connected to standards and testing workflows
- 🧪 **Smart Lab Match** — capability-aware laboratory recommendations with directions
- 🛡️ **Evidence & Trust** — source-grounded, inferred, user-provided and unverified states
- 📄 **Document & Test Report AI** — structured extraction without inventing pass/fail results
- 🔔 **Regulatory Change Radar** — identify changes that may affect a product/workspace
- 🚨 **Suspicious Product Reports** — consumer-facing reporting workflow
- 🌐 **Indian-language experience** — English, Hindi, Kannada, Telugu and Tamil foundation
- 📊 **Reports & Compliance Passport** — auditable project history and readiness view

## Architecture

```text
BIS SmartHub
├── frontend/              # User-first web experience
├── backend/               # Unified API and orchestration layer
├── intelligence/          # Product intelligence, RAG, agent and evidence
├── verification/          # QR, ISI/CM-L, HUID, CRS
├── compliance/            # QCO, requirements, readiness and passport
├── cad/                   # CAD analysis and standards-aware checks
├── laboratories/          # Capability matching and directions
├── documents/             # Document and test-report intelligence
├── notifications/        # Notification adapters (real providers only)
├── data/                  # Standards and local datasets
└── tests/                 # Automated tests
```

## Trust rules

SmartHub must never present demo, simulated, hard-coded or locally snapshotted data as authoritative live BIS verification. When authoritative evidence is unavailable, the UI must clearly show **UNVERIFIED / SOURCE UNAVAILABLE**.

Engineering analysis such as CAD measurements is presented as an analytical aid, not as a legal certification.

## Development strategy

The original `SIH26107-BIS-SmartGuide` and `bis-sahayak` repositories remain unchanged. SmartHub selectively ports and rewrites capabilities rather than blindly merging repositories.

### Build order

1. User-first application shell and role selection
2. BIS Copilot orchestration layer
3. SmartGuide intelligence/evidence integration
4. Scan Anything workflow
5. MSME Compliance Workspace / Passport
6. CAD → Standard → Test → Lab workflow
7. Consumer verification and suspicious-product workflow
8. Regulatory updates, documents and notifications
9. PWA/mobile optimization and final SIH demo polish

## Status

🚧 **Phase 0 — Unified foundation**
