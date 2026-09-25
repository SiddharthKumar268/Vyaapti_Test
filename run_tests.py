"""
Standalone test runner for Vyaapti -- no pytest dependency required.
Run with:  python run_tests.py

Outputs a clear pass/fail table plus a summary count.
"""

import sys
import traceback
from datetime import datetime, timedelta
from chain_scoring import Transaction, RiskChainAnalyzer


# -- helpers ---------------------------------------------------------------

def _make_linear_chain(accounts, amount, start, interval_min):
    return [
        Transaction(
            sender=accounts[i],
            receiver=accounts[i + 1],
            amount=amount,
            timestamp=start + timedelta(minutes=interval_min * i),
        )
        for i in range(len(accounts) - 1)
    ]


# -- test definitions ------------------------------------------------------

def test_layering_detected():
    a = RiskChainAnalyzer()
    chain = _make_linear_chain(["A","B","C","D","E","F","G"], 10_00_000, datetime(2024,1,1,10,0), 30)
    assert a.check_layering(chain) is True, "Layering should trigger for 6-hop chain"

def test_layering_short_chain():
    a = RiskChainAnalyzer()
    chain = _make_linear_chain(["A","B","C"], 10_00_000, datetime(2024,1,1,10,0), 30)
    assert a.check_layering(chain) is False, "Layering should NOT trigger for 2-hop chain"

def test_risk_level_thresholds():
    a = RiskChainAnalyzer()
    assert a._classify_risk(80) == "CRITICAL"
    assert a._classify_risk(75) == "CRITICAL"
    assert a._classify_risk(50) == "HIGH"
    assert a._classify_risk(25) == "MEDIUM"
    assert a._classify_risk(10) == "LOW"
    assert a._classify_risk(0)  == "LOW"

def test_rapid_succession_high_velocity():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",1_00_00_000, s),
        Transaction("B","C",1_00_00_000, s+timedelta(minutes=15)),
        Transaction("C","D",1_00_00_000, s+timedelta(minutes=30)),
    ]
    assert a.check_rapid_succession(chain) is True, \
        "Rs 3Cr in 30min = Rs 6Cr/hr should trigger rapid succession"

def test_rapid_succession_boundary():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",60_00_000, s),
        Transaction("B","C",50_00_000, s+timedelta(minutes=60)),
    ]
    assert a.check_rapid_succession(chain) is True, \
        "Rs 1.1Cr in 1hr should trigger rapid succession"

def test_time_compression_fast_chain():
    a = RiskChainAnalyzer()
    chain = _make_linear_chain(["A","B","C","D"], 10_00_000, datetime(2024,1,1,10,0), 5)
    assert a.check_time_compression(chain) is True, \
        "15-minute chain should trigger time compression"

def test_time_compression_45_minutes():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",10_00_000, s),
        Transaction("B","C",10_00_000, s+timedelta(minutes=45)),
    ]
    assert a.check_time_compression(chain) is True, \
        "45-minute chain should trigger time compression"

def test_integration_high_risk():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",40_00_000, s),
        Transaction("B","C",35_00_000, s+timedelta(minutes=5)),
        Transaction("C","D",30_00_000, s+timedelta(minutes=10)),
        Transaction("D","E",35_00_000, s+timedelta(minutes=15)),
        Transaction("E","F",30_00_000, s+timedelta(minutes=20)),
        Transaction("F","G",30_00_000, s+timedelta(minutes=25)),
    ]
    r = a.calculate_risk_score(chain)
    assert r["total_score"] >= 55, \
        "Expected >=55 (layering+rapid+compression) got %d; factors=%s" % (r["total_score"], r["factors"])
    assert r["risk_level"] in ("HIGH","CRITICAL"), \
        "Expected HIGH/CRITICAL, got %s" % r["risk_level"]

def test_structuring_at_reporting_line():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",50_00_000, s),
        Transaction("B","C",50_00_000, s+timedelta(hours=2)),
        Transaction("C","D",50_00_000, s+timedelta(hours=4)),
    ]
    assert a.check_structuring(chain) is True, \
        "Average Rs 50L should trigger structuring"

def test_structuring_just_below_threshold():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("A","B",49_80_000, s),
        Transaction("B","C",49_80_000, s+timedelta(hours=2)),
    ]
    assert a.check_structuring(chain) is True, \
        "Average Rs 49.8L should trigger structuring"

def test_structuring_compliance_flag():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("X","Y",50_50_000, s),
        Transaction("Y","Z",50_50_000, s+timedelta(hours=1)),
    ]
    r = a.calculate_risk_score(chain)
    assert "structuring" in r["factors"], \
        "Structuring missing for Rs 50.5L avg -- compliance violation! factors=%s" % r["factors"]

def test_circular_pattern_detected():
    a = RiskChainAnalyzer()
    s = datetime(2024,1,1,10,0)
    chain = [
        Transaction("ACC_001","ACC_002",10_00_000, s),
        Transaction("ACC_002","ACC_003",10_00_000, s+timedelta(hours=2)),
        Transaction("ACC_003","ACC_001",10_00_000, s+timedelta(hours=4)),
    ]
    assert a.check_circular_pattern(chain) is True, \
        "A->B->C->A should be detected as circular"


# -- runner ----------------------------------------------------------------

ALL_TESTS = [
    test_layering_detected,
    test_layering_short_chain,
    test_risk_level_thresholds,
    test_rapid_succession_high_velocity,
    test_rapid_succession_boundary,
    test_time_compression_fast_chain,
    test_time_compression_45_minutes,
    test_integration_high_risk,
    test_structuring_at_reporting_line,
    test_structuring_just_below_threshold,
    test_structuring_compliance_flag,
    test_circular_pattern_detected,
]

if __name__ == "__main__":
    passed = 0
    failed = 0
    errors = []

    print("=" * 72)
    print("  Vyaapti RTGS Risk-Chain Analyzer -- Test Suite")
    print("=" * 72)
    print()

    for test_fn in ALL_TESTS:
        name = test_fn.__name__
        try:
            test_fn()
            print("  [PASS]  %s" % name)
            passed += 1
        except AssertionError as e:
            print("  [FAIL]  %s" % name)
            print("          -> %s" % e)
            errors.append((name, str(e)))
            failed += 1
        except Exception as e:
            print("  [ERR]   %s" % name)
            print("          -> %s" % e)
            traceback.print_exc()
            errors.append((name, str(e)))
            failed += 1

    print()
    print("-" * 72)
    print("  TOTAL: %d  |  PASSED: %d  |  FAILED: %d" % (passed + failed, passed, failed))
    print("-" * 72)

    if errors:
        print()
        print("  Failed tests:")
        for name, msg in errors:
            print("    - %s: %s" % (name, msg))
        print()

    sys.exit(1 if failed else 0)
