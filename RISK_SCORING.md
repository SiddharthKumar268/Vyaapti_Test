# Vyaapti Risk Scoring — Reference

> **System:** RTGS Risk-Chain Analyzer (Vyaapti)
> **Owner:** Compliance & Fraud-Detection Team
> **Last updated:** 2024-09-01

---

## Purpose

Vyaapti scores every chain of RTGS transactions against five independent
fraud-risk factors.  Each factor that fires contributes a fixed number of
points; the total is **capped at 100**.  Scores drive automated alerting
and regulatory reporting.

---

## Risk Factors

| # | Factor | Points | Trigger condition | Compliance note |
|---|--------|-------:|-------------------|-----------------|
| 1 | **Circular Pattern** | 30 | Chain starts **and ends at the same account** (A→…→A). | Circular flows are a primary indicator in RBI's fraud-typology guidelines. |
| 2 | **Rapid Succession** | 25 | Total value moved exceeds **₹1 Cr per hour**. | High-velocity movement is flagged under the Prevention of Money Laundering Act (PMLA). |
| 3 | **Layering** | 20 | Chain contains **5 or more hops** (transactions). | Multiple intermediaries suggest layering — a known money-laundering technique. |
| 4 | **Structuring** | 15 | Average transfer amount falls in the **₹49 L – ₹51 L band**. | This band brackets the **₹50 L RBI reporting threshold**. Transfers deliberately kept just below the threshold are a structuring signal and **must** be reported to FIU-IND. |
| 5 | **Time Compression** | 10 | The entire chain completes in **under 1 hour**. | Unusually fast settlement across multiple hops is atypical of legitimate RTGS usage. |

---

## Score → Risk Level Mapping

| Score range | Risk level |
|-------------|------------|
| 75 – 100    | **CRITICAL** |
| 50 – 74     | **HIGH** |
| 25 – 49     | **MEDIUM** |
| 0 – 24      | **LOW** |

---

## Key Implementation Rules

1. **Time span** is measured from the earliest to the latest timestamp in
   the chain and must be expressed in **hours** (not minutes, not seconds).
2. **Velocity** = (sum of all transaction amounts) ÷ (time span in hours).
3. **Structuring band** is inclusive on both ends: `₹49,00,000 ≤ avg ≤ ₹51,00,000`.
4. **Circular check** compares the **first sender** to the **last receiver**.
5. All factors are evaluated independently; order does not matter.
6. The total score is `min(sum_of_fired_factors, 100)`.

---

## Why These Thresholds Matter

The ₹50 L reporting threshold is set by the Reserve Bank of India.
If the structuring detector silently stops flagging amounts in the
₹49 L – ₹51 L band, the system will **fail to generate mandatory
Suspicious Transaction Reports (STRs)** — exposing the institution to
regulatory penalties.  Any regression in structuring detection should be
treated as a **compliance-critical bug**, not a routine test failure.
