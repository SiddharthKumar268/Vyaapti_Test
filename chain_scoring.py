"""
Vyaapti — RTGS Risk-Chain Analyzer
===================================
Scores chains of RTGS transactions against five fraud-risk factors
defined in RISK_SCORING.md.

Each factor contributes a fixed number of points to a total that is
capped at 100.  The analyzer is used downstream by compliance dashboards
and automated alerting pipelines.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


# ──────────────────────────────────────────────
# Domain model
# ──────────────────────────────────────────────

@dataclass
class Transaction:
    """A single RTGS leg between two accounts."""
    sender: str
    receiver: str
    amount: float        # in INR (₹)
    timestamp: datetime


# ──────────────────────────────────────────────
# Analyzer
# ──────────────────────────────────────────────

class RiskChainAnalyzer:
    """Analyzes a chain of RTGS transactions for fraud-risk indicators.

    Risk factors and their point values are defined in RISK_SCORING.md.
    """

    # Point allocations (must match RISK_SCORING.md)
    CIRCULAR_PATTERN_SCORE  = 30
    RAPID_SUCCESSION_SCORE  = 25
    LAYERING_SCORE          = 20
    STRUCTURING_SCORE       = 15
    TIME_COMPRESSION_SCORE  = 10
    MAX_SCORE               = 100

    # Detection thresholds
    VELOCITY_THRESHOLD_PER_HOUR = 1_00_00_000   # ₹1 Cr / hour
    LAYERING_HOP_THRESHOLD      = 5
    STRUCTURING_LOWER_BOUND     = 49_00_000     # ₹49 L
    STRUCTURING_UPPER_BOUND     = 51_00_000     # ₹51 L
    TIME_COMPRESSION_MAX_HOURS  = 1.0           # 1 hour

    # ── helpers ───────────────────────────────

    def compute_time_span_hours(self, chain: List[Transaction]) -> float:
        """Return the elapsed time of the chain **in hours**.

        Used by both the rapid-succession and time-compression checks.
        """
        if len(chain) < 2:
            return 0.0
        timestamps = [txn.timestamp for txn in chain]
        delta_seconds = (max(timestamps) - min(timestamps)).total_seconds()
        # BUG A ▸ divides by 60 (minutes) instead of 3600 (seconds→hours)
        return delta_seconds / 60

    def compute_velocity(self, chain: List[Transaction]) -> float:
        """Total value moved per hour (₹/hr)."""
        span = self.compute_time_span_hours(chain)
        if span == 0:
            return float("inf")
        return sum(txn.amount for txn in chain) / span

    # ── individual risk-factor checks ─────────

    def check_circular_pattern(self, chain: List[Transaction]) -> bool:
        """True if the chain starts and ends at the **same account**.

        A circular pattern (A→B→C→A) means the first sender equals the
        last *receiver*.
        """
        if len(chain) < 2:
            return False
        # BUG C ▸ compares first sender to last *sender* (should be last receiver)
        return chain[0].sender == chain[-1].sender

    def check_rapid_succession(self, chain: List[Transaction]) -> bool:
        """True if value moved exceeds ₹1 Cr / hour."""
        return self.compute_velocity(chain) > self.VELOCITY_THRESHOLD_PER_HOUR

    def check_layering(self, chain: List[Transaction]) -> bool:
        """True if the chain has ≥ 5 hops (transactions)."""
        return len(chain) >= self.LAYERING_HOP_THRESHOLD

    def check_structuring(self, chain: List[Transaction]) -> bool:
        """True if the average transfer sits in the ₹49 L – ₹51 L band.

        This band brackets the ₹50 L RBI reporting threshold, a classic
        structuring signal.
        """
        if not chain:
            return False
        avg = sum(txn.amount for txn in chain) / len(chain)
        # BUG B ▸ upper bound hard-coded as 49_50_000 instead of STRUCTURING_UPPER_BOUND (51_00_000)
        return self.STRUCTURING_LOWER_BOUND <= avg <= 49_50_000

    def check_time_compression(self, chain: List[Transaction]) -> bool:
        """True if the entire chain completes in under 1 hour."""
        span = self.compute_time_span_hours(chain)
        return 0 < span < self.TIME_COMPRESSION_MAX_HOURS

    # ── aggregate scoring ─────────────────────

    def calculate_risk_score(self, chain: List[Transaction]) -> Dict:
        """Return a dict with total score, factor breakdown, and risk level."""
        factors: Dict[str, int] = {}
        total = 0

        if self.check_circular_pattern(chain):
            factors["circular_pattern"] = self.CIRCULAR_PATTERN_SCORE
            total += self.CIRCULAR_PATTERN_SCORE

        if self.check_rapid_succession(chain):
            factors["rapid_succession"] = self.RAPID_SUCCESSION_SCORE
            total += self.RAPID_SUCCESSION_SCORE

        if self.check_layering(chain):
            factors["layering"] = self.LAYERING_SCORE
            total += self.LAYERING_SCORE

        if self.check_structuring(chain):
            factors["structuring"] = self.STRUCTURING_SCORE
            total += self.STRUCTURING_SCORE

        if self.check_time_compression(chain):
            factors["time_compression"] = self.TIME_COMPRESSION_SCORE
            total += self.TIME_COMPRESSION_SCORE

        total = min(total, self.MAX_SCORE)

        return {
            "total_score": total,
            "factors": factors,
            "risk_level": self._classify_risk(total),
        }

    @staticmethod
    def _classify_risk(score: int) -> str:
        if score >= 75:
            return "CRITICAL"
        if score >= 50:
            return "HIGH"
        if score >= 25:
            return "MEDIUM"
        return "LOW"
