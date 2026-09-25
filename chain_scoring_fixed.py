"""
Vyaapti -- RTGS Risk-Chain Analyzer (FIXED VERSION)
====================================================
This is the corrected version with all 3 bugs fixed.
Keep this file separate -- use it ONLY in Step 9 to confirm all tests pass.

Fixes applied:
  Bug A: compute_time_span_hours() now divides by 3600 (not 60)
  Bug B: check_structuring() upper bound restored to STRUCTURING_UPPER_BOUND (51_00_000)
  Bug C: check_circular_pattern() compares first sender to last receiver (not last sender)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    timestamp: datetime


class RiskChainAnalyzer:
    CIRCULAR_PATTERN_SCORE  = 30
    RAPID_SUCCESSION_SCORE  = 25
    LAYERING_SCORE          = 20
    STRUCTURING_SCORE       = 15
    TIME_COMPRESSION_SCORE  = 10
    MAX_SCORE               = 100

    VELOCITY_THRESHOLD_PER_HOUR = 1_00_00_000
    LAYERING_HOP_THRESHOLD      = 5
    STRUCTURING_LOWER_BOUND     = 49_00_000
    STRUCTURING_UPPER_BOUND     = 51_00_000
    TIME_COMPRESSION_MAX_HOURS  = 1.0

    def compute_time_span_hours(self, chain: List[Transaction]) -> float:
        if len(chain) < 2:
            return 0.0
        timestamps = [txn.timestamp for txn in chain]
        delta_seconds = (max(timestamps) - min(timestamps)).total_seconds()
        # FIX A: divide by 3600 to convert seconds to hours
        return delta_seconds / 3600

    def compute_velocity(self, chain: List[Transaction]) -> float:
        span = self.compute_time_span_hours(chain)
        if span == 0:
            return float("inf")
        return sum(txn.amount for txn in chain) / span

    def check_circular_pattern(self, chain: List[Transaction]) -> bool:
        if len(chain) < 2:
            return False
        # FIX C: compare first sender to last RECEIVER
        return chain[0].sender == chain[-1].receiver

    def check_rapid_succession(self, chain: List[Transaction]) -> bool:
        return self.compute_velocity(chain) > self.VELOCITY_THRESHOLD_PER_HOUR

    def check_layering(self, chain: List[Transaction]) -> bool:
        return len(chain) >= self.LAYERING_HOP_THRESHOLD

    def check_structuring(self, chain: List[Transaction]) -> bool:
        if not chain:
            return False
        avg = sum(txn.amount for txn in chain) / len(chain)
        # FIX B: use the correct upper bound constant (51_00_000)
        return self.STRUCTURING_LOWER_BOUND <= avg <= self.STRUCTURING_UPPER_BOUND

    def check_time_compression(self, chain: List[Transaction]) -> bool:
        span = self.compute_time_span_hours(chain)
        return 0 < span < self.TIME_COMPRESSION_MAX_HOURS

    def calculate_risk_score(self, chain: List[Transaction]) -> Dict:
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
