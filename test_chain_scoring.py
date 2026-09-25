"""
Test suite for Vyaapti RTGS Risk-Chain Analyzer
================================================
12 tests total — covers all five risk factors plus an integration scenario.

Expected passing tests  : 3   (layering + classification)
Expected failing tests  : 9   (see cluster notes below)

Failure clusters (for triage):
  Cluster A — time_span bug   : 5 failures  (rapid-succession ×2, time-compression ×2, integration ×1)
  Cluster B — structuring bug : 3 failures  (structuring ×3)
  Cluster C — circular bug    : 1 failure   (circular-pattern ×1)
"""

import pytest
from datetime import datetime, timedelta

from chain_scoring import Transaction, RiskChainAnalyzer


# ── fixtures / helpers ────────────────────────────────────────────────

@pytest.fixture
def analyzer():
    return RiskChainAnalyzer()


def _make_linear_chain(
    accounts: list[str],
    amount: float,
    start: datetime,
    interval_min: int,
) -> list[Transaction]:
    """Build a simple A→B→C→… chain with uniform amounts and spacing."""
    return [
        Transaction(
            sender=accounts[i],
            receiver=accounts[i + 1],
            amount=amount,
            timestamp=start + timedelta(minutes=interval_min * i),
        )
        for i in range(len(accounts) - 1)
    ]


# ═══════════════════════════════════════════════════════════════════════
# PASSING tests (not affected by any of the 3 bugs)
# ═══════════════════════════════════════════════════════════════════════

class TestLayering:
    """Layering only depends on hop count — unaffected by time/amount bugs."""

    def test_layering_detected(self, analyzer):
        """Chain with 6 hops (≥5) → layering should trigger."""
        chain = _make_linear_chain(
            ["A", "B", "C", "D", "E", "F", "G"],
            10_00_000,
            datetime(2024, 1, 1, 10, 0),
            interval_min=30,
        )
        assert analyzer.check_layering(chain) is True

    def test_layering_short_chain(self, analyzer):
        """Chain with 2 hops (<5) → layering should NOT trigger."""
        chain = _make_linear_chain(
            ["A", "B", "C"],
            10_00_000,
            datetime(2024, 1, 1, 10, 0),
            interval_min=30,
        )
        assert analyzer.check_layering(chain) is False


class TestClassification:
    def test_risk_level_thresholds(self, analyzer):
        """Verify all four classification buckets."""
        assert analyzer._classify_risk(80) == "CRITICAL"
        assert analyzer._classify_risk(75) == "CRITICAL"
        assert analyzer._classify_risk(50) == "HIGH"
        assert analyzer._classify_risk(25) == "MEDIUM"
        assert analyzer._classify_risk(10) == "LOW"
        assert analyzer._classify_risk(0)  == "LOW"


# ═══════════════════════════════════════════════════════════════════════
# CLUSTER A — failures caused by BUG A  (time_span / 60 instead of / 3600)
#
# compute_time_span_hours() returns a value 60× too large.
#   • velocity is 60× too small  → rapid-succession never fires
#   • apparent duration is 60× too long → time-compression never fires
# ═══════════════════════════════════════════════════════════════════════

class TestRapidSuccession:

    def test_high_velocity_chain(self, analyzer):
        """₹3 Cr moved in 30 min ⇒ ₹6 Cr/hr — must trigger rapid succession.

        Bug A makes time_span = 30 hrs → velocity ≈ ₹10 L/hr (below ₹1 Cr/hr).
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 1_00_00_000, start),
            Transaction("B", "C", 1_00_00_000, start + timedelta(minutes=15)),
            Transaction("C", "D", 1_00_00_000, start + timedelta(minutes=30)),
        ]
        assert analyzer.check_rapid_succession(chain) is True

    def test_velocity_just_above_threshold(self, analyzer):
        """₹1.1 Cr in 1 hr ⇒ ₹1.1 Cr/hr — barely above threshold.

        Bug A makes time_span = 60 hrs → velocity ≈ ₹1.83 L/hr.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 60_00_000, start),
            Transaction("B", "C", 50_00_000, start + timedelta(minutes=60)),
        ]
        assert analyzer.check_rapid_succession(chain) is True


class TestTimeCompression:

    def test_fast_chain(self, analyzer):
        """Chain spanning 15 min (< 1 hr) → time compression should fire.

        Bug A reports span as 15 hrs → check fails.
        """
        chain = _make_linear_chain(
            ["A", "B", "C", "D"],
            10_00_000,
            datetime(2024, 1, 1, 10, 0),
            interval_min=5,
        )
        assert analyzer.check_time_compression(chain) is True

    def test_compression_45_minutes(self, analyzer):
        """Chain spanning exactly 45 min (< 1 hr) → should trigger.

        Bug A reports span as 45 hrs.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 10_00_000, start),
            Transaction("B", "C", 10_00_000, start + timedelta(minutes=45)),
        ]
        assert analyzer.check_time_compression(chain) is True


class TestIntegration:

    def test_high_risk_multi_factor(self, analyzer):
        """6-hop chain moving ₹2 Cr in 25 min → layering + rapid + compression ≥ 55.

        Bug A kills both rapid-succession and time-compression, leaving only
        layering (20 pts) → total = 20, which is < 55.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 40_00_000, start),
            Transaction("B", "C", 35_00_000, start + timedelta(minutes=5)),
            Transaction("C", "D", 30_00_000, start + timedelta(minutes=10)),
            Transaction("D", "E", 35_00_000, start + timedelta(minutes=15)),
            Transaction("E", "F", 30_00_000, start + timedelta(minutes=20)),
            Transaction("F", "G", 30_00_000, start + timedelta(minutes=25)),
        ]
        result = analyzer.calculate_risk_score(chain)
        assert result["total_score"] >= 55, (
            f"Expected ≥55 (layering+rapid+compression) but got {result['total_score']}; "
            f"factors={result['factors']}"
        )
        assert result["risk_level"] in ("HIGH", "CRITICAL")


# ═══════════════════════════════════════════════════════════════════════
# CLUSTER B — failures caused by BUG B  (structuring upper bound 49.5L not 51L)
#
# Amounts between ₹49.5 L and ₹51 L are wrongly excluded from the
# structuring band, so transfers at ₹50 L (the RBI reporting line) go
# undetected — a compliance-relevant regression.
# ═══════════════════════════════════════════════════════════════════════

class TestStructuring:

    def test_average_at_reporting_line(self, analyzer):
        """Average exactly ₹50 L — smack on the RBI threshold — must trigger.

        Bug B caps the band at ₹49.5 L → ₹50 L is excluded.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 50_00_000, start),
            Transaction("B", "C", 50_00_000, start + timedelta(hours=2)),
            Transaction("C", "D", 50_00_000, start + timedelta(hours=4)),
        ]
        assert analyzer.check_structuring(chain) is True

    def test_average_just_below_threshold(self, analyzer):
        """Average ₹49.8 L — still inside the ₹49 L–₹51 L band.

        Bug B: ₹49.8 L > ₹49.5 L upper bound → not detected.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("A", "B", 49_80_000, start),
            Transaction("B", "C", 49_80_000, start + timedelta(hours=2)),
        ]
        assert analyzer.check_structuring(chain) is True

    def test_structuring_compliance_flag(self, analyzer):
        """Average ₹50.5 L should appear in the risk-score factor breakdown.

        This is the compliance-critical assertion: structuring near the RBI
        reporting line MUST be flagged, per RISK_SCORING.md.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("X", "Y", 50_50_000, start),
            Transaction("Y", "Z", 50_50_000, start + timedelta(hours=1)),
        ]
        result = analyzer.calculate_risk_score(chain)
        assert "structuring" in result["factors"], (
            f"Structuring factor missing — amounts averaging ₹50.5 L should be in the "
            f"₹49 L–₹51 L compliance band.  factors={result['factors']}"
        )


# ═══════════════════════════════════════════════════════════════════════
# CLUSTER C — failure caused by BUG C  (circular pattern: sender vs receiver)
#
# check_circular_pattern() compares chain[0].sender to chain[-1].sender
# instead of chain[-1].receiver, so A→B→C→A is not detected as circular.
# ═══════════════════════════════════════════════════════════════════════

class TestCircularPattern:

    def test_circular_chain_detected(self, analyzer):
        """A→B→C→A is circular (first sender == last receiver).

        Bug C compares first sender to last *sender* (C ≠ A) → not detected.
        """
        start = datetime(2024, 1, 1, 10, 0)
        chain = [
            Transaction("ACC_001", "ACC_002", 10_00_000, start),
            Transaction("ACC_002", "ACC_003", 10_00_000, start + timedelta(hours=2)),
            Transaction("ACC_003", "ACC_001", 10_00_000, start + timedelta(hours=4)),
        ]
        assert analyzer.check_circular_pattern(chain) is True
