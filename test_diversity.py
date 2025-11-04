#!/usr/bin/env python3
"""
Test script to demonstrate character diversity patterns functionality.
"""

from diversity_patterns import (
    DiversityRule,
    analyze_character_types,
    validate_diversity,
    calculate_diversity_score,
    has_sequential_pattern,
    has_excessive_repetition,
    has_consecutive_same_type,
    enhance_diversity
)


def test_analysis():
    """Test character type analysis."""
    print("=" * 60)
    print("Testing Character Type Analysis")
    print("=" * 60)
    
    test_passwords = [
        "password123",
        "P@ssw0rd!",
        "ALLUPPERCASE",
        "alllowercase123",
        "Mixed123!@#"
    ]
    
    for pwd in test_passwords:
        counts = analyze_character_types(pwd)
        score = calculate_diversity_score(pwd)
        # Note: These are test passwords for demonstration purposes, not real user passwords
        print(f"\nPassword: {pwd}")
        print(f"  Uppercase: {counts['uppercase']}, Lowercase: {counts['lowercase']}")
        print(f"  Digits: {counts['digits']}, Special: {counts['special']}")
        print(f"  Diversity Score: {score:.1f}/100")


def test_pattern_detection():
    """Test pattern detection."""
    print("\n" + "=" * 60)
    print("Testing Pattern Detection")
    print("=" * 60)
    
    patterns_to_test = [
        ("abc123xyz", True, "Sequential (abc, 123)"),
        ("qwerty123", True, "Keyboard pattern (qwerty)"),
        ("aaabbbccc", True, "Excessive repetition"),
        ("AAAAA11111", True, "Consecutive same type"),
        ("P@ssw0rd!", False, "Good diversity"),
        ("Secure123!", False, "Good diversity"),
    ]
    
    for pwd, should_fail, description in patterns_to_test:
        has_seq = has_sequential_pattern(pwd)
        has_rep = has_excessive_repetition(pwd, 2)
        has_cons = has_consecutive_same_type(pwd, 3)
        
        print(f"\nPassword: {pwd} ({description})")
        print(f"  Sequential: {has_seq}")
        print(f"  Repetition: {has_rep}")
        print(f"  Consecutive same type: {has_cons}")
        print(f"  Expected to fail: {should_fail}")


def test_diversity_validation():
    """Test diversity rule validation."""
    print("\n" + "=" * 60)
    print("Testing Diversity Validation")
    print("=" * 60)
    
    rule = DiversityRule(
        min_uppercase=1,
        min_lowercase=1,
        min_digits=1,
        min_special=1,
        max_consecutive_same_type=3,
        max_repeated_char=2,
        avoid_sequential=True
    )
    
    test_cases = [
        "password",           # Missing uppercase, digits, special
        "Password",           # Missing digits, special
        "Password1",          # Missing special
        "Password1!",         # Valid
        "PASSWORD1!",         # Missing lowercase
        "abc123!@#",          # Has sequential pattern
        "Passsword1!",        # Excessive repetition
        "AAAA1111!!!!",       # Consecutive same type
        "P@ssw0rd!",          # Valid
        "Secure123!",         # Valid
    ]
    
    for pwd in test_cases:
        is_valid, violations = validate_diversity(pwd, rule)
        score = calculate_diversity_score(pwd)
        print(f"\nPassword: {pwd}")
        print(f"  Valid: {is_valid}")
        print(f"  Score: {score:.1f}/100")
        if violations:
            print(f"  Violations:")
            for v in violations:
                print(f"    - {v}")


def test_enhancement():
    """Test password enhancement with diversity patterns."""
    print("\n" + "=" * 60)
    print("Testing Password Enhancement")
    print("=" * 60)
    
    base_words = ["secure", "bitcoin", "wallet"]
    patterns = ["mixed", "sandwich", "alternating", "distributed"]
    
    for word in base_words:
        print(f"\nBase word: {word}")
        for pattern in patterns:
            variations = enhance_diversity(word, "123", "!", pattern)
            print(f"  Pattern '{pattern}':")
            for var in variations[:3]:  # Show first 3 variations
                score = calculate_diversity_score(var)
                print(f"    {var} (score: {score:.1f})")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CHARACTER DIVERSITY PATTERNS - DEMONSTRATION")
    print("=" * 60)
    
    test_analysis()
    test_pattern_detection()
    test_diversity_validation()
    test_enhancement()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
