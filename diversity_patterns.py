"""
Character Diversity Patterns Module

This module provides functions to validate and enhance password character diversity.
It ensures passwords have good distribution of different character types and
avoids weak patterns like sequential characters or excessive repetition.
"""

from typing import Dict, List, Tuple


class DiversityRule:
    """Define character diversity rules for password generation."""
    
    def __init__(self, 
                 min_uppercase: int = 1,
                 min_lowercase: int = 1,
                 min_digits: int = 1,
                 min_special: int = 1,
                 max_consecutive_same_type: int = 3,
                 max_repeated_char: int = 2,
                 avoid_sequential: bool = True):
        """
        Initialize diversity rules.
        
        :param min_uppercase: Minimum number of uppercase letters
        :param min_lowercase: Minimum number of lowercase letters
        :param min_digits: Minimum number of digits
        :param min_special: Minimum number of special characters
        :param max_consecutive_same_type: Maximum consecutive characters of same type
        :param max_repeated_char: Maximum times a character can repeat consecutively
        :param avoid_sequential: Whether to avoid sequential patterns (abc, 123, etc.)
        """
        self.min_uppercase = min_uppercase
        self.min_lowercase = min_lowercase
        self.min_digits = min_digits
        self.min_special = min_special
        self.max_consecutive_same_type = max_consecutive_same_type
        self.max_repeated_char = max_repeated_char
        self.avoid_sequential = avoid_sequential


def analyze_character_types(password: str) -> Dict[str, int]:
    """
    Analyze the character types in a password.
    
    :param password: The password to analyze
    :return: Dictionary with counts of each character type
    """
    counts = {
        'uppercase': sum(1 for c in password if c.isupper()),
        'lowercase': sum(1 for c in password if c.islower()),
        'digits': sum(1 for c in password if c.isdigit()),
        'special': sum(1 for c in password if not c.isalnum())
    }
    return counts


def has_sequential_pattern(password: str, min_length: int = 3) -> bool:
    """
    Check if password contains sequential patterns.
    
    Sequential patterns include:
    - Alphabetic sequences: abc, xyz, ABC
    - Numeric sequences: 123, 789
    - Keyboard sequences: qwerty, asdfgh
    
    :param password: The password to check
    :param min_length: Minimum length of sequence to detect
    :return: True if sequential pattern found
    """
    password_lower = password.lower()
    
    # Check alphabetic sequences
    for i in range(len(password) - min_length + 1):
        is_seq = True
        for j in range(min_length - 1):
            if i + j + 1 >= len(password):
                is_seq = False
                break
            curr = password_lower[i + j]
            next_char = password_lower[i + j + 1]
            if curr.isalpha() and next_char.isalpha():
                if ord(next_char) != ord(curr) + 1:
                    is_seq = False
                    break
            elif curr.isdigit() and next_char.isdigit():
                if ord(next_char) != ord(curr) + 1:
                    is_seq = False
                    break
            else:
                is_seq = False
                break
        if is_seq:
            return True
    
    # Check common keyboard sequences
    keyboard_patterns = [
        # Standard QWERTY keyboard rows
        'qwerty', 'asdfgh', 'zxcvbn',
        # International keyboard layouts
        'qwertz', 'azerty',
        # Common special character sequences
        '!@#$%', '(){}[]'
    ]
    
    for pattern in keyboard_patterns:
        if pattern in password_lower:
            return True
        # Check reverse
        if pattern[::-1] in password_lower:
            return True
    
    return False


def has_excessive_repetition(password: str, max_repeat: int = 2) -> bool:
    """
    Check if password has excessive character repetition.
    
    :param password: The password to check
    :param max_repeat: Maximum allowed consecutive repetitions
    :return: True if excessive repetition found
    """
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i-1]:
            count += 1
            if count > max_repeat:
                return True
        else:
            count = 1
    return False


def has_consecutive_same_type(password: str, max_consecutive: int = 3) -> bool:
    """
    Check if password has too many consecutive characters of the same type.
    
    :param password: The password to check
    :param max_consecutive: Maximum allowed consecutive chars of same type
    :return: True if excessive consecutive same type found
    """
    if not password:
        return False
    
    def char_type(c: str) -> str:
        if c.isupper():
            return 'upper'
        elif c.islower():
            return 'lower'
        elif c.isdigit():
            return 'digit'
        else:
            return 'special'
    
    current_type = char_type(password[0])
    count = 1
    
    for i in range(1, len(password)):
        this_type = char_type(password[i])
        if this_type == current_type:
            count += 1
            if count > max_consecutive:
                return True
        else:
            current_type = this_type
            count = 1
    
    return False


def validate_diversity(password: str, rule: DiversityRule) -> Tuple[bool, List[str]]:
    """
    Validate if a password meets diversity requirements.
    
    :param password: The password to validate
    :param rule: The diversity rule to check against
    :return: Tuple of (is_valid, list_of_violations)
    """
    violations = []
    
    # Check character type counts
    counts = analyze_character_types(password)
    
    if counts['uppercase'] < rule.min_uppercase:
        violations.append(f"Need at least {rule.min_uppercase} uppercase letters")
    
    if counts['lowercase'] < rule.min_lowercase:
        violations.append(f"Need at least {rule.min_lowercase} lowercase letters")
    
    if counts['digits'] < rule.min_digits:
        violations.append(f"Need at least {rule.min_digits} digits")
    
    if counts['special'] < rule.min_special:
        violations.append(f"Need at least {rule.min_special} special characters")
    
    # Check for excessive repetition
    if has_excessive_repetition(password, rule.max_repeated_char):
        violations.append(f"Character repeated more than {rule.max_repeated_char} times")
    
    # Check for consecutive same type
    if has_consecutive_same_type(password, rule.max_consecutive_same_type):
        violations.append(f"More than {rule.max_consecutive_same_type} consecutive chars of same type")
    
    # Check for sequential patterns
    if rule.avoid_sequential and has_sequential_pattern(password):
        violations.append("Contains sequential pattern (abc, 123, qwerty, etc.)")
    
    return (len(violations) == 0, violations)


def calculate_diversity_score(password: str) -> float:
    """
    Calculate a diversity score for a password (0-100).
    
    Higher scores indicate better character diversity.
    
    :param password: The password to score
    :return: Diversity score (0-100)
    """
    if not password:
        return 0.0
    
    score = 0.0
    
    # Character type diversity (40 points max)
    counts = analyze_character_types(password)
    types_present = sum(1 for count in counts.values() if count > 0)
    score += (types_present / 4) * 40
    
    # Balance of character types (20 points max)
    total_chars = len(password)
    if total_chars > 0:
        type_ratios = [count / total_chars for count in counts.values() if count > 0]
        if type_ratios:
            # Perfect balance would be all types equal
            avg_ratio = sum(type_ratios) / len(type_ratios)
            variance = sum((r - avg_ratio) ** 2 for r in type_ratios) / len(type_ratios)
            # Scale variance (typical values 0-0.1) to 0-1 range for scoring
            VARIANCE_SCALE_FACTOR = 10
            balance_score = max(0, 1 - (variance * VARIANCE_SCALE_FACTOR))
            score += balance_score * 20
    
    # No excessive repetition (20 points)
    if not has_excessive_repetition(password, 2):
        score += 20
    elif not has_excessive_repetition(password, 3):
        score += 10
    
    # No sequential patterns (10 points)
    if not has_sequential_pattern(password):
        score += 10
    
    # Good distribution - no consecutive same type (10 points)
    if not has_consecutive_same_type(password, 3):
        score += 10
    elif not has_consecutive_same_type(password, 4):
        score += 5
    
    return min(100.0, score)


def enhance_diversity(base_word: str, 
                      numbers: str = "123", 
                      special: str = "!",
                      pattern: str = "mixed") -> List[str]:
    """
    Generate password variations with enhanced character diversity.
    
    :param base_word: The base word to use
    :param numbers: Number string to incorporate
    :param special: Special character(s) to incorporate
    :param pattern: Pattern type ('mixed', 'sandwich', 'alternating', 'distributed')
    :return: List of password variations with good diversity
    """
    variations = []
    
    # Ensure base_word has mixed case
    base_variants = [
        base_word.capitalize(),
        base_word.upper(),
        ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(base_word))
    ]
    
    for base in base_variants:
        if pattern == "mixed":
            # Standard combinations
            variations.extend([
                f"{base}{numbers}{special}",
                f"{special}{base}{numbers}",
                f"{numbers}{special}{base}"
            ])
        
        elif pattern == "sandwich":
            # Special chars sandwich the word
            variations.extend([
                f"{special}{base}{numbers}{special}",
                f"{special[0]}{base}{special}{numbers}"
            ])
        
        elif pattern == "alternating":
            # Interleave different types
            mid = len(base) // 2
            variations.extend([
                f"{base[:mid]}{numbers}{special}{base[mid:]}",
                f"{base[:mid]}{special}{base[mid:]}{numbers}",
                f"{special}{base[:mid]}{numbers}{base[mid:]}"
            ])
        
        elif pattern == "distributed":
            # Distribute evenly
            third = len(base) // 3
            if third > 0:
                variations.extend([
                    f"{base[:third]}{special}{base[third:2*third]}{numbers}{base[2*third:]}",
                    f"{special}{base[:third]}{numbers}{base[third:]}"
                ])
    
    return variations
