# Vyaapti Test-Triage Copilot
### Autonomous Test-Failure Clustering, Regulatory Compliance Triage & Leakage Audit with IBM Bob 2.0

> **Hackathon Track:** Open Track — Improving Developer Workflows (Testing & Debugging)  
> **Tool:** IBM Bob 2.0 (Agent Mode, Parallel Tasks, Subagents, Document Understanding)  
> **Target Domain:** RTGS Risk-Chain Analyzer (Financial Crime Compliance & Anti-Money Laundering)  
> **Live Demo Portal:** [https://siddharthkumar268.github.io/Vyaapti_Test/](https://siddharthkumar268.github.io/Vyaapti_Test/)

---

## ⚡ Executive Summary

In mission-critical fraud-detection engines, a single defect in a shared calculation or utility helper cascades into a wall of seemingly unrelated test failures. Developers spend **~18 minutes** diagnosing failures one-by-one, repeatedly re-deriving the same shared root cause while blind to high-severity regulatory violations.

**Vyaapti Test-Triage Copilot** elevates test triage from routine debugging into an **Autonomous Enterprise Compliance Operating System**:
From a **single natural-language prompt**, IBM Bob 2.0:
1. **Executes the broken test suite** autonomously without manual configuration.
2. **Ingests regulatory domain documentation** (`RISK_SCORING.md`) via Document Understanding.
3. **Clusters failures by shared root cause** and spins up **parallel subagents** to isolate and patch defects simultaneously.
4. **Produces a structured triage matrix** mapping code bugs directly to RBI Master Directions and PMLA statutory violations.
5. **Applies verified code diffs** and confirms 100% green tests (12/12 passing).
6. **Goes beyond fixing:**
   - **Historical Stream Replay Audit:** Simulates 500 historical settlement transactions, identifying **₹4.12 Crore in suspicious fund leakage** that bypassed the broken engine, and auto-drafts a retroactive STR manifest for FIU-IND.
   - **Hardening Edge Tests:** Auto-generates **7 new boundary and negative test cases**.
   - **CI/CD Governance:** Establishes **5 permanent pre-commit and deployment policies**.

---

## 📊 Key Results & Impact Metrics

| Metric | Traditional Manual Triage | With IBM Bob 2.0 Copilot | Impact |
|---|---|---|---|
| **Diagnosis Duration** | ~18 minutes | **~45 seconds** | **24x Faster** |
| **Duplicated Investigation** | ~80% (re-tracing same roots) | **0% (auto-clustered)** | **100% Eliminated** |
| **Regulatory Risk Visibility** | 0 flags (treated as routine bugs) | **2 P0 Violations Caught** | **Zero Compliance Blindspots** |
| **Financial Leakage Audit** | None (undetected) | **₹4.12 Cr Leakage Flagged** | **Auto-Generated FIU-IND Manifest** |
| **Codebase Hardening** | 0 new tests created | **7 auto-generated edge tests** | **Permanent Regression Barrier** |
| **Release Gatekeeping** | Manual sign-off | **Automated CI/CD Blocker** | **Audit-Ready Governance** |

---

## 🌐 4-Page Enterprise Web Portal

The repository includes a complete, zero-dependency interactive portal ready for GitHub Pages, Replit, or local execution:

| Page | File | Core Functionality |
|---|---|---|
| **1. Test Mission Control** | [`index.html`](index.html) | Live interactive test runner (broken vs green), failure clustering grid, and the **Live Subagent Telemetry Terminal** streaming asynchronous agent logs. |
| **2. Regulatory Audit & Incidents** | [`compliance.html`](compliance.html) | Formal RBI KYC §29 & PMLA compliance portal with an **Interactive Statutory Penalty Calculator** (₹10L/transaction fine estimator) and tri-party digital sign-off. |
| **3. Live RTGS Chain Simulator** | [`risk_chains.html`](risk_chains.html) | Interactive transaction graph visualizer ($A \to B \to C \to A$), **Preset Attack Typologies** (Smurfing, Flash Velocity, Circular Mule), and the **500-Transaction Historical Replay Engine**. |
| **4. CI/CD Governance & Hardening** | [`governance.html`](governance.html) | Live deployment gatekeeper (blocks release on compliance failure), in-browser **7 Edge-Test Suite runner**, and pre-commit linter policies. |

---

## 🧠 IBM Bob 2.0 Feature Mapping

### 1. Agent Mode
Bob operates autonomously end-to-end: discovering test runners, executing commands, parsing tracebacks, reading source modules, generating regulatory reports, writing edge-case tests, and executing verification commands without human intervention.

### 2. Document Understanding (`RISK_SCORING.md`)
Unlike generic LLMs that only evaluate code syntax, Bob ingests regulatory domain documentation. It recognizes that a threshold bug in `check_structuring()` violates the **Reserve Bank of India Master Direction on KYC (Section 29)** and suppresses mandatory **Suspicious Transaction Reports (STRs) to FIU-IND**, elevating a routine test failure into an executive P0 incident.

### 3. Parallel Tasks & Subagents
Instead of serial analysis, Bob clusters failures and spins up 3 concurrent subagents:
- **Subagent A (Time/Velocity Cluster):** Analyzes 5 failures caused by `delta_seconds / 60` unit error.
- **Subagent B (Structuring Cluster):** Analyzes 3 failures caused by hardcoded `49_50_000` upper bound.
- **Subagent C (Circular Flow Cluster):** Analyzes 1 failure in sender-receiver comparison.

Execution wall-clock time is bounded by the slowest cluster, not the sum of all failures.

---

## 🖼️ Visual Session & Verification Evidence

All high-resolution verification screenshots are included in the repository:

1. **Before Triage (9 Failures, No Grouping):** `screenshot_before_9failures.jpg`
2. **Bob 2.0 Multi-Agent Prompt:** `screenshot_bob_prompt.jpg`
3. **Structured Root-Cause Triage Matrix:** `screenshot_triage_report.jpg`
4. **Verified Remediation (12/12 Passing):** `screenshot_after_allgreen.jpg`
5. **Formal Compliance Incident Report:** `screenshot_compliance_report.jpg`
6. **Codebase Hardening (7 Auto-Generated Tests):** `screenshot_new_tests.jpg`
7. **CI/CD Governance Policies:** `screenshot_ci_rules.jpg`
8. **Impact ROI Comparison:** `screenshot_impact_comparison.jpg`

---

## 📂 Project Structure

```
vyaapti-test-demo/
│
├── chain_scoring.py                    # Core RTGS scoring logic (3 planted defects)
├── chain_scoring_fixed.py              # Reference corrected version
├── test_chain_scoring.py               # 12-test suite covering all 5 risk factors
├── run_tests.py                        # Zero-dependency test runner
├── RISK_SCORING.md                     # Regulatory compliance documentation (RBI/PMLA)
│
├── index.html                          # Mission Control + Subagent Telemetry Terminal
├── compliance.html                     # Regulatory Audit Center + Penalty Calculator
├── risk_chains.html                    # RTGS Chain Visualizer + Historical Replay Engine
├── governance.html                     # CI/CD Deployment Gatekeeper + Edge-Test Runner
│
├── replay_audit.py                     # Historical 500-transaction stream replay script
├── MISSED_TRANSACTIONS_STR_MANIFEST.json # Auto-generated retroactive FIU-IND STR manifest
├── compliance_report.py                # Formal audit report generator
├── COMPLIANCE_INCIDENT_REPORT.txt      # Regulatory incident transcript
├── test_autogenerated_edgecases.py     # 7 Bob-generated hardening edge tests
├── REGRESSION_PREVENTION.md            # Pre-commit hooks & CI/CD governance policies
│
├── app.py                              # Flask application for Replit / cloud hosting
├── .replit & requirements.txt          # 1-click cloud deployment configuration
├── Vyaapti_TestTriage_Copilot.pptx     # 20-slide presentation deck
└── README.md                           # Comprehensive documentation
```

---

## 🚀 Quickstart & Reproduction

```bash
# 1. Run the broken test suite (shows 9 failures across 3 clusters)
python run_tests.py

# 2. Run the historical 500-transaction stream replay audit
python replay_audit.py

# 3. View the auto-generated compliance incident report
python compliance_report.py

# 4. Run the 7 auto-generated edge-case hardening tests
python test_autogenerated_edgecases.py

# 5. Launch the interactive web portal locally
# Either double-click index.html in your browser or run:
python app.py
```

---

## 🌍 Why This Generalizes Across Software Engineering

Cascading test failures caused by shared utilities occur across all complex architectures:
- **Banking & FinTech:** Compliance thresholds, currency conversion rounding, fee ladders.
- **Healthcare & MedTech:** Unit conversion in drug dosage algorithms, clinical threshold alerts.
- **E-Commerce & Logistics:** Pricing engines, discount tax brackets, delivery SLA countdowns.

Vyaapti Test-Triage Copilot proves that combining **Agent Mode**, **Concurrent Subagents**, and **Domain Document Understanding** delivers not just faster code fixes, but **complete developer workflow automation and compliance assurance**.
