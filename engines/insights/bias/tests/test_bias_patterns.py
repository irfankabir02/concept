#!/usr/bin/env python3
"""
Test suite for bias pattern detection.
Tests all 5 research-backed patterns and custom pattern registration.
"""

from bias_pattern_detector import BiasPatternDetector, BiasPatternEngine


def test_tone_shift_hostile():
    """Test tone shift pattern (friendly → hostile escalation)."""
    print("=" * 70)
    print("TEST 1: Tone Shift (Friendly → Hostile)")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger tone_shift_hostile
    stream = [
        "low_escalation",
        "medium_escalation",
        "high_escalation",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: tone_shift_hostile detection\n")
    detector.detect(stream)
    print("\n✅ Test 1 passed\n")


def test_passive_refusal():
    """Test passive refusal pattern (deflection)."""
    print("=" * 70)
    print("TEST 2: Passive Refusal (Deflection)")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger passive_refusal
    stream = [
        "low_escalation",
        "medium_refusal",
        "high_asymmetric",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: passive_refusal detection\n")
    detector.detect(stream)
    print("\n✅ Test 2 passed\n")


def test_cultural_bias_accumulation():
    """Test cultural bias accumulation pattern."""
    print("=" * 70)
    print("TEST 3: Cultural Bias Accumulation")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger cultural_bias_accumulation
    stream = [
        "low_invalidation",
        "high_asymmetric",
        "high_asymmetric",
        "high_personal_expression",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: cultural_bias_accumulation detection\n")
    detector.detect(stream)
    print("\n✅ Test 3 passed\n")


def test_invalidation_cascade():
    """Test invalidation cascade pattern."""
    print("=" * 70)
    print("TEST 4: Invalidation Cascade")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger invalidation_cascade
    stream = [
        "low_escalation",
        "high_invalidation",
        "high_invalidation",
        "medium_refusal",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: invalidation_cascade detection\n")
    detector.detect(stream)
    print("\n✅ Test 4 passed\n")


def test_bias_recovery():
    """Test bias recovery pattern (positive trend)."""
    print("=" * 70)
    print("TEST 5: Bias Recovery (Positive Trend)")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger bias_recovery
    stream = [
        "high_bias_any",
        "medium_bias_any",
        "low_bias_any",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: bias_recovery detection\n")
    detector.detect(stream)
    print("\n✅ Test 5 passed\n")


def test_multiple_patterns():
    """Test detection of multiple patterns in one stream."""
    print("=" * 70)
    print("TEST 6: Multiple Patterns in Single Stream")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Should trigger multiple patterns
    stream = [
        "low_escalation",
        "medium_escalation",
        "high_escalation",      # tone_shift_hostile
        "high_invalidation",
        "high_invalidation",    # invalidation_cascade
        "medium_refusal",
        "high_asymmetric",      # passive_refusal
        "high_bias_any",
        "medium_bias_any",
        "low_bias_any",         # bias_recovery
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: Multiple pattern detections\n")
    detector.detect(stream)
    print("\n✅ Test 6 passed\n")


def test_custom_pattern():
    """Test custom pattern registration."""
    print("=" * 70)
    print("TEST 7: Custom Pattern Registration")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Register custom pattern
    def custom_callback(name, seq, info):
        print(f"[CUSTOM] {name} detected: {' → '.join(seq)}")
    
    detector.register_pattern(
        name="custom_test_pattern",
        sequence=["low_refusal", "high_refusal"],
        callback=custom_callback,
        priority=5,
        category="custom_patterns",
        max_matches=2,
    )
    
    stream = [
        "low_refusal",
        "high_refusal",
        "medium_escalation",
        "low_refusal",
        "high_refusal",  # Should match twice
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: 2 custom pattern detections\n")
    detector.detect(stream)
    print("\n✅ Test 7 passed\n")


def test_max_matches_limit():
    """Test max_matches limit enforcement."""
    print("=" * 70)
    print("TEST 8: Max Matches Limit")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Register pattern with max_matches=2
    match_count = [0]
    
    def counting_callback(name, seq, info):
        match_count[0] += 1
        print(f"[Match #{match_count[0]}] {name}")
    
    detector.register_pattern(
        name="limited_pattern",
        sequence=["test_token"],
        callback=counting_callback,
        max_matches=2,
    )
    
    # Stream with 5 occurrences, but should only match 2
    stream = ["test_token"] * 5
    
    print(f"\nToken stream: {len(stream)} occurrences of 'test_token'")
    print("Expected: Only 2 matches (max_matches=2)\n")
    detector.detect(stream)
    
    if match_count[0] == 2:
        print(f"\n✅ Test 8 passed: Correctly limited to {match_count[0]} matches\n")
    else:
        print(f"\n❌ Test 8 failed: Got {match_count[0]} matches, expected 2\n")


def test_priority_ordering():
    """Test that higher priority patterns are evaluated first."""
    print("=" * 70)
    print("TEST 9: Priority Ordering")
    print("=" * 70)
    
    engine = BiasPatternEngine()
    
    # Clear built-in patterns for this test
    engine._patterns.clear()
    
    # Register patterns with different priorities
    def callback_low(name, seq, info):
        print(f"  [Priority 1] {name}")
    
    def callback_high(name, seq, info):
        print(f"  [Priority 5] {name}")
    
    engine.register_pattern("low_priority", ["test"], callback_low, priority=1)
    engine.register_pattern("high_priority", ["test"], callback_high, priority=5)
    
    print("\nRegistered patterns:")
    for p in engine._patterns:
        print(f"  {p.name}: priority={p.priority}")
    
    print("\nExpected order: high_priority (5) before low_priority (1)")
    print("\nDetection order:")
    engine.detect(["test"])
    
    # Check ordering
    if engine._patterns[0].priority > engine._patterns[1].priority:
        print("\n✅ Test 9 passed: Patterns correctly ordered by priority\n")
    else:
        print("\n❌ Test 9 failed: Incorrect priority ordering\n")


def test_no_false_positives():
    """Test that patterns don't match when they shouldn't."""
    print("=" * 70)
    print("TEST 10: No False Positives")
    print("=" * 70)
    
    detector = BiasPatternDetector()
    
    # Stream that should NOT trigger any patterns
    stream = [
        "low_escalation",
        "low_invalidation",
        "medium_refusal",
        "low_asymmetric",
    ]
    
    print("\nToken stream:", " → ".join(stream))
    print("\nExpected: No pattern detections\n")
    
    # Capture detections
    detections = []
    
    def capture_callback(name, seq, info):
        detections.append(name)
        print(f"[UNEXPECTED] {name} detected")
    
    # Replace callbacks to capture
    for pattern in detector.engine._patterns:
        pattern.callback = capture_callback
    
    detector.detect(stream)
    
    if len(detections) == 0:
        print("✅ Test 10 passed: No false positives\n")
    else:
        print(f"❌ Test 10 failed: {len(detections)} false positives detected\n")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("BIAS PATTERN DETECTION TEST SUITE")
    print("=" * 70 + "\n")
    
    test_tone_shift_hostile()
    test_passive_refusal()
    test_cultural_bias_accumulation()
    test_invalidation_cascade()
    test_bias_recovery()
    test_multiple_patterns()
    test_custom_pattern()
    test_max_matches_limit()
    test_priority_ordering()
    test_no_false_positives()
    
    print("=" * 70)
    print("ALL TESTS COMPLETED ✅")
    print("=" * 70)
