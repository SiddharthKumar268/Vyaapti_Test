"""Generate terminal-style screenshot images for the hackathon presentation."""

from PIL import Image, ImageDraw, ImageFont
import os

# Try to get a monospace font
try:
    font = ImageFont.truetype("consola.ttf", 16)
    font_small = ImageFont.truetype("consola.ttf", 13)
    font_title = ImageFont.truetype("consola.ttf", 14)
except:
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
        font_small = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
        font_title = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_small = font
        font_title = font

# Colors
BG = (22, 27, 34)
BAR_BG = (33, 38, 45)
BORDER = (48, 54, 61)
WHITE = (230, 237, 243)
GREEN = (63, 185, 80)
RED = (248, 81, 73)
DIM = (139, 148, 158)
BLUE = (121, 192, 255)
YELLOW = (210, 153, 34)
DOT_RED = (255, 95, 87)
DOT_YELLOW = (254, 188, 46)
DOT_GREEN = (40, 200, 64)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def draw_terminal(draw, w, y_start):
    """Draw terminal window chrome (title bar with dots)."""
    # Title bar background
    draw.rectangle([0, y_start, w, y_start + 40], fill=BAR_BG)
    draw.line([0, y_start + 40, w, y_start + 40], fill=BORDER)
    # Dots
    draw.ellipse([16, y_start + 13, 28, y_start + 25], fill=DOT_RED)
    draw.ellipse([34, y_start + 13, 46, y_start + 25], fill=DOT_YELLOW)
    draw.ellipse([52, y_start + 13, 64, y_start + 25], fill=DOT_GREEN)
    # Title
    draw.text((76, y_start + 12), "PowerShell - vyaapti-test-demo", fill=DIM, font=font_title)
    return y_start + 40


def draw_text_line(draw, x, y, text, color=WHITE):
    """Draw a single line of text."""
    draw.text((x, y), text, fill=color, font=font)
    return y + 22


# ============================================================
# SCREENSHOT 1: BEFORE - 9 Failing Tests
# ============================================================
def create_before_screenshot():
    w, h = 950, 820
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    y = draw_terminal(draw, w, 0)
    x = 24
    y += 16

    # Command line
    y = draw_text_line(draw, x, y, "PS C:\\vyaapti-test-demo> ", DIM)
    draw.text((x + 280, y - 22), "python run_tests.py", fill=BLUE, font=font)
    y += 8

    # Separator
    y = draw_text_line(draw, x, y, "=" * 72, BORDER)
    y = draw_text_line(draw, x, y, "  Vyaapti RTGS Risk-Chain Analyzer -- Test Suite", WHITE)
    y = draw_text_line(draw, x, y, "=" * 72, BORDER)
    y += 8

    # PASS tests
    y = draw_text_line(draw, x, y, "  [PASS]  test_layering_detected", GREEN)
    y = draw_text_line(draw, x, y, "  [PASS]  test_layering_short_chain", GREEN)
    y = draw_text_line(draw, x, y, "  [PASS]  test_risk_level_thresholds", GREEN)

    # FAIL tests
    fails = [
        ("test_rapid_succession_high_velocity",
         "-> Rs 3Cr in 30min = Rs 6Cr/hr should trigger rapid succession"),
        ("test_rapid_succession_boundary",
         "-> Rs 1.1Cr in 1hr should trigger rapid succession"),
        ("test_time_compression_fast_chain",
         "-> 15-minute chain should trigger time compression"),
        ("test_time_compression_45_minutes",
         "-> 45-minute chain should trigger time compression"),
        ("test_integration_high_risk",
         "-> Expected >=55 got 20; factors={'layering': 20}"),
        ("test_structuring_at_reporting_line",
         "-> Average Rs 50L should trigger structuring"),
        ("test_structuring_just_below_threshold",
         "-> Average Rs 49.8L should trigger structuring"),
        ("test_structuring_compliance_flag",
         "-> Structuring missing -- compliance violation!"),
        ("test_circular_pattern_detected",
         "-> A->B->C->A should be detected as circular"),
    ]

    for name, msg in fails:
        y = draw_text_line(draw, x, y, f"  [FAIL]  {name}", RED)
        y = draw_text_line(draw, x, y, f"          {msg}", DIM)

    y += 8
    y = draw_text_line(draw, x, y, "-" * 72, BORDER)

    # Summary line - draw in parts for coloring
    draw.text((x, y), "  TOTAL: 12  |  PASSED: 3  |  ", fill=WHITE, font=font)
    draw.text((x + 330, y), "FAILED: 9", fill=RED, font=font)
    y += 22

    y = draw_text_line(draw, x, y, "-" * 72, BORDER)

    path = os.path.join(OUT_DIR, "screenshot_before_9failures.jpg")
    img.save(path, "JPEG", quality=95)
    print(f"Saved: {path}")


# ============================================================
# SCREENSHOT 2: AFTER - All 12 Pass
# ============================================================
def create_after_screenshot():
    w, h = 950, 520
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    y = draw_terminal(draw, w, 0)
    x = 24
    y += 16

    y = draw_text_line(draw, x, y, "PS C:\\vyaapti-test-demo> ", DIM)
    draw.text((x + 280, y - 22), "python run_tests.py", fill=BLUE, font=font)
    y += 8

    y = draw_text_line(draw, x, y, "=" * 72, BORDER)
    y = draw_text_line(draw, x, y, "  Vyaapti RTGS Risk-Chain Analyzer -- Test Suite", WHITE)
    y = draw_text_line(draw, x, y, "=" * 72, BORDER)
    y += 8

    tests = [
        "test_layering_detected",
        "test_layering_short_chain",
        "test_risk_level_thresholds",
        "test_rapid_succession_high_velocity",
        "test_rapid_succession_boundary",
        "test_time_compression_fast_chain",
        "test_time_compression_45_minutes",
        "test_integration_high_risk",
        "test_structuring_at_reporting_line",
        "test_structuring_just_below_threshold",
        "test_structuring_compliance_flag",
        "test_circular_pattern_detected",
    ]

    for t in tests:
        y = draw_text_line(draw, x, y, f"  [PASS]  {t}", GREEN)

    y += 8
    y = draw_text_line(draw, x, y, "-" * 72, BORDER)
    draw.text((x, y), "  TOTAL: 12  |  ", fill=WHITE, font=font)
    draw.text((x + 175, y), "PASSED: 12", fill=GREEN, font=font)
    draw.text((x + 310, y), "  |  FAILED: 0", fill=WHITE, font=font)
    y += 22
    y = draw_text_line(draw, x, y, "-" * 72, BORDER)

    path = os.path.join(OUT_DIR, "screenshot_after_allgreen.jpg")
    img.save(path, "JPEG", quality=95)
    print(f"Saved: {path}")


# ============================================================
# SCREENSHOT 3: Triage Report Table
# ============================================================
def create_triage_report():
    w, h = 1050, 480
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    y = draw_terminal(draw, w, 0)
    x = 24
    y += 12

    draw.text((x, y), "Bob 2.0 Triage Report", fill=BLUE, font=font)
    y += 28

    # Table header
    cols = [x, x+130, x+370, x+650, x+850]
    headers = ["Cluster", "Affected Tests", "Root Cause", "Fix", "Compliance"]
    draw.rectangle([x-4, y-4, w-20, y+20], fill=BAR_BG)
    for i, hdr in enumerate(headers):
        draw.text((cols[i], y), hdr, fill=WHITE, font=font_small)
    y += 28
    draw.line([x-4, y-4, w-20, y-4], fill=BORDER)

    # Row A
    draw.text((cols[0], y), "A: Time Span", fill=RED, font=font_small)
    draw.text((cols[1], y), "rapid_succession (x2)", fill=DIM, font=font_small)
    draw.text((cols[2], y), "time_span divides by 60", fill=DIM, font=font_small)
    draw.text((cols[3], y), "/60 -> /3600", fill=GREEN, font=font_small)
    draw.text((cols[4], y), "HIGH", fill=RED, font=font_small)
    y += 20
    draw.text((cols[1], y), "time_compression (x2)", fill=DIM, font=font_small)
    draw.text((cols[2], y), "instead of 3600", fill=DIM, font=font_small)
    draw.text((cols[4], y), "PMLA velocity", fill=DIM, font=font_small)
    y += 20
    draw.text((cols[1], y), "integration (x1)", fill=DIM, font=font_small)
    draw.text((cols[4], y), "disabled", fill=DIM, font=font_small)
    y += 28
    draw.line([x-4, y-4, w-20, y-4], fill=BORDER)

    # Row B
    draw.text((cols[0], y), "B: Structuring", fill=YELLOW, font=font_small)
    draw.text((cols[1], y), "structuring_report (x1)", fill=DIM, font=font_small)
    draw.text((cols[2], y), "Upper bound 49.5L", fill=DIM, font=font_small)
    draw.text((cols[3], y), "49_50_000 ->", fill=GREEN, font=font_small)
    draw.text((cols[4], y), "CRITICAL", fill=RED, font=font_small)
    y += 20
    draw.text((cols[1], y), "structuring_below (x1)", fill=DIM, font=font_small)
    draw.text((cols[2], y), "instead of 51L", fill=DIM, font=font_small)
    draw.text((cols[3], y), "UPPER_BOUND", fill=GREEN, font=font_small)
    draw.text((cols[4], y), "STR filings", fill=DIM, font=font_small)
    y += 20
    draw.text((cols[1], y), "compliance_flag (x1)", fill=DIM, font=font_small)
    draw.text((cols[4], y), "skipped!", fill=DIM, font=font_small)
    y += 28
    draw.line([x-4, y-4, w-20, y-4], fill=BORDER)

    # Row C
    draw.text((cols[0], y), "C: Circular", fill=BLUE, font=font_small)
    draw.text((cols[1], y), "circular_detected (x1)", fill=DIM, font=font_small)
    draw.text((cols[2], y), "Compares .sender", fill=DIM, font=font_small)
    draw.text((cols[3], y), ".sender ->", fill=GREEN, font=font_small)
    draw.text((cols[4], y), "MEDIUM", fill=YELLOW, font=font_small)
    y += 20
    draw.text((cols[2], y), "instead of .receiver", fill=DIM, font=font_small)
    draw.text((cols[3], y), ".receiver", fill=GREEN, font=font_small)
    draw.text((cols[4], y), "RBI indicator", fill=DIM, font=font_small)
    y += 32

    # Summary
    draw.text((x, y), "3 root causes identified | 9 tests explained | 2 compliance regressions flagged", fill=GREEN, font=font_small)

    path = os.path.join(OUT_DIR, "screenshot_triage_report.jpg")
    img.save(path, "JPEG", quality=95)
    print(f"Saved: {path}")


# ============================================================
# SCREENSHOT 4: Bob Prompt
# ============================================================
def create_prompt_screenshot():
    w, h = 950, 500
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    y = draw_terminal(draw, w, 0)
    draw.text((76, 12), "IBM Bob 2.0 - Agent Mode", fill=DIM, font=font_title)
    x = 24
    y += 16

    draw.text((x, y), "You:", fill=BLUE, font=font)
    y += 28

    prompt_lines = [
        'Run the failing tests using python run_tests.py.',
        'For each failure, identify the root cause by reading',
        'chain_scoring.py and cross-checking RISK_SCORING.md.',
        '',
        'Group failures sharing the same root cause. Use',
        'parallel subagents (one per cluster) to investigate.',
        'Each subagent should:',
        '  1. Identify the exact bug (wrong line)',
        '  2. Explain WHY it causes the failures',
        '  3. Cross-check RISK_SCORING.md for compliance impact',
        '  4. Provide the exact code fix',
        '',
        'Merge results into a structured triage report.',
        'Apply fixes and re-run to confirm all pass.',
    ]

    for line in prompt_lines:
        draw.text((x + 16, y), line, fill=WHITE if line.strip() else DIM, font=font_small)
        y += 18

    y += 16
    # Feature tags
    tags = [
        ("Agent Mode", BLUE),
        ("Document Understanding", (203, 166, 247)),
        ("Subagents", RED),
        ("Parallel Tasks", GREEN),
    ]
    tx = x
    for label, color in tags:
        tw = len(label) * 8 + 20
        draw.rounded_rectangle([tx, y, tx+tw, y+24], radius=12, outline=color, fill=(color[0]//8, color[1]//8, color[2]//8))
        draw.text((tx+10, y+5), label, fill=color, font=font_small)
        tx += tw + 10

    path = os.path.join(OUT_DIR, "screenshot_bob_prompt.jpg")
    img.save(path, "JPEG", quality=95)
    print(f"Saved: {path}")


# ============================================================
# SCREENSHOT 5: Impact Comparison
# ============================================================
def create_impact_screenshot():
    w, h = 950, 420
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    y = draw_terminal(draw, w, 0)
    x = 24
    y += 20

    draw.text((x, y), "Impact: Before vs After", fill=BLUE, font=font)
    y += 36

    # Table
    headers = ["Metric", "Manual", "Bob 2.0", "Improvement"]
    col_x = [x, x+300, x+480, x+660]
    draw.rectangle([x-4, y-4, w-20, y+22], fill=BAR_BG)
    for i, h_text in enumerate(headers):
        draw.text((col_x[i], y), h_text, fill=WHITE, font=font)
    y += 30
    draw.line([x-4, y, w-20, y], fill=BORDER)
    y += 8

    rows = [
        ("Diagnosis time", "~18 minutes", "~45 seconds", "24x faster"),
        ("Duplicated effort", "~80%", "0%", "Eliminated"),
        ("Compliance flags", "0 (missed)", "2 flagged", "Zero missed"),
        ("Root cause grouping", "Manual", "Automatic", "3 clusters"),
        ("Verified fix", "No", "Yes", "Re-run confirmed"),
    ]

    for metric, manual, bob, imp in rows:
        draw.text((col_x[0], y), metric, fill=DIM, font=font)
        draw.text((col_x[1], y), manual, fill=RED, font=font)
        draw.text((col_x[2], y), bob, fill=GREEN, font=font)
        draw.text((col_x[3], y), imp, fill=BLUE, font=font)
        y += 26
        draw.line([x-4, y+4, w-20, y+4], fill=(30, 35, 42))
        y += 10

    y += 16
    draw.text((x, y), "18 min", fill=RED, font=font)
    draw.text((x+90, y), " --> ", fill=DIM, font=font)
    draw.text((x+140, y), "45 sec", fill=GREEN, font=font)
    draw.text((x+240, y), "  =  24x faster with IBM Bob 2.0", fill=WHITE, font=font)

    path = os.path.join(OUT_DIR, "screenshot_impact_comparison.jpg")
    img.save(path, "JPEG", quality=95)
    print(f"Saved: {path}")


if __name__ == "__main__":
    print("Generating screenshots...")
    create_before_screenshot()
    create_after_screenshot()
    create_triage_report()
    create_prompt_screenshot()
    create_impact_screenshot()
    print("\nAll 5 screenshots saved!")
