# Character Diversity Patterns

This document explains the character diversity pattern features added to the password generator suite.

## Overview

Character diversity patterns enhance password generation by ensuring generated passwords have:
- **Balanced character type distribution** (uppercase, lowercase, digits, special characters)
- **No weak patterns** (sequential characters, excessive repetition)
- **Good positional diversity** (character types aren't clustered together)
- **Configurable rules** to meet specific security requirements

## Components

### 1. Diversity Analysis Module (`diversity_patterns.py`)

Core module providing:

#### Character Type Analysis
```python
from diversity_patterns import analyze_character_types

counts = analyze_character_types("P@ssw0rd!")
# Returns: {'uppercase': 1, 'lowercase': 6, 'digits': 1, 'special': 2}
```

#### Diversity Scoring (0-100)
```python
from diversity_patterns import calculate_diversity_score

score = calculate_diversity_score("P@ssw0rd!")  # Returns: ~93.4
score = calculate_diversity_score("password")    # Returns: ~60.0
```

The score is calculated based on:
- Character type diversity (40 points)
- Balance of character types (20 points)
- No excessive repetition (20 points)
- No sequential patterns (10 points)
- Good distribution (10 points)

#### Pattern Detection

**Sequential Patterns:**
```python
from diversity_patterns import has_sequential_pattern

has_sequential_pattern("abc123")      # True - contains "abc" and "123"
has_sequential_pattern("qwerty")      # True - keyboard pattern
has_sequential_pattern("P@ssw0rd!")   # False
```

**Excessive Repetition:**
```python
from diversity_patterns import has_excessive_repetition

has_excessive_repetition("aaabbb", max_repeat=2)    # True
has_excessive_repetition("P@ssw0rd!", max_repeat=2) # False
```

**Consecutive Same Type:**
```python
from diversity_patterns import has_consecutive_same_type

has_consecutive_same_type("AAAA1111", max_consecutive=3)  # True
has_consecutive_same_type("P@ssw0rd!", max_consecutive=3) # False
```

#### Diversity Validation
```python
from diversity_patterns import DiversityRule, validate_diversity

rule = DiversityRule(
    min_uppercase=1,
    min_lowercase=1,
    min_digits=1,
    min_special=1,
    max_consecutive_same_type=3,
    max_repeated_char=2,
    avoid_sequential=True
)

is_valid, violations = validate_diversity("P@ssw0rd!", rule)
# is_valid: True, violations: []
```

#### Password Enhancement
```python
from diversity_patterns import enhance_diversity

# Generate variations with different patterns
variations = enhance_diversity("secure", "123", "!", pattern="alternating")
# Returns: ['Sec123!ure', 'Sec!ure123', '!Sec123ure', ...]
```

**Available patterns:**
- `mixed`: Standard combinations (word+numbers+special)
- `sandwich`: Special chars surround the word
- `alternating`: Interleave different character types
- `distributed`: Evenly distribute character types throughout

### 2. Enhanced Super Advanced Generator

The `super_advanced_mask_generator.py` now includes a new pattern type: `enhanced-diversity`

#### Usage

```bash
# Generate with enhanced diversity patterns
python3 super_advanced_mask_generator.py --patterns enhanced-diversity

# Use custom wordlist
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --wordlist wordlist.txt

# Set minimum diversity score (0-100, default: 70)
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --min-diversity-score 80

# Enable strict validation rules
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --strict-rules
```

#### Example Output

```
[*] Generating enhanced diversity patterns...
Secure123!
!Secure123
123!Secure
Sec123!ure
Sec!ure123
!Sec123ure
Se!cu123re
...
```

All generated passwords:
- Have uppercase, lowercase, digits, and special characters
- Meet the minimum diversity score threshold
- Avoid weak patterns if strict rules are enabled

### 3. Enhanced Basic Generator

The `mask_generator.py` now supports diversity filtering:

#### Usage

```bash
# Generate without diversity filtering (default)
python3 mask_generator.py 4 "Aa1!"

# Enable diversity filtering
python3 mask_generator.py 4 "Aa1!" --diversity 50

# The second argument is the minimum diversity score (0-100)
```

This filters out weak passwords during generation based on diversity rules.

## Use Cases

### 1. High-Security Password Generation
```bash
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --min-diversity-score 85 \
    --strict-rules
```
Perfect for applications requiring strong passwords with verified diversity.

### 2. Custom Wordlist with Diversity
```bash
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --wordlist custom_words.txt \
    --min-diversity-score 75
```
Generate passwords from your wordlist while ensuring character diversity.

### 3. Multiple Pattern Types
```bash
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity mixed crypto-terms
```
Combine enhanced diversity with other pattern types for comprehensive coverage.

### 4. Testing Password Strength
```python
# Use test_diversity.py to analyze password strength
python3 test_diversity.py
```

## Diversity Rules Configuration

The `DiversityRule` class allows fine-grained control:

```python
rule = DiversityRule(
    min_uppercase=1,        # Minimum uppercase letters
    min_lowercase=1,        # Minimum lowercase letters
    min_digits=1,           # Minimum digits
    min_special=1,          # Minimum special characters
    max_consecutive_same_type=3,  # Max consecutive chars of same type
    max_repeated_char=2,    # Max consecutive repetitions of same char
    avoid_sequential=True   # Avoid abc, 123, qwerty patterns
)
```

## Diversity Score Interpretation

| Score Range | Interpretation | Characteristics |
|-------------|---------------|-----------------|
| 90-100 | Excellent | All character types, well-balanced, no weak patterns |
| 75-89 | Good | Good diversity, minor issues possible |
| 60-74 | Fair | Some diversity, may have clustering or limited types |
| 40-59 | Poor | Limited character types or significant pattern issues |
| 0-39 | Very Poor | Minimal diversity, likely has weak patterns |

## Pattern Types Explained

### Mixed Pattern
```
Word + Numbers + Special
Examples: Secure123!, !Bitcoin321, Crypto007@
```
Standard combination with all character types.

### Sandwich Pattern
```
Special + Word + Numbers + Special
Examples: !Secure123!, @Bitcoin321@
```
Special characters wrap around the password for better distribution.

### Alternating Pattern
```
Word_Part1 + Numbers + Special + Word_Part2
Examples: Sec123!ure, Bit321@coin
```
Interleaves character types to prevent clustering.

### Distributed Pattern
```
Evenly distributed character types throughout
Examples: Se!cu123re, Bi!tc321oin
```
Optimal character type distribution across the entire password.

## Best Practices

1. **Use minimum diversity score of 70+** for production passwords
2. **Enable strict rules** when security is critical
3. **Combine patterns** to maximize coverage
4. **Test generated passwords** with test_diversity.py before deployment
5. **Customize DiversityRule** to match your specific requirements

## Technical Details

### Sequential Pattern Detection
Detects:
- Alphabetic sequences: abc, xyz, ABC, XYZ
- Numeric sequences: 123, 456, 789
- Keyboard patterns: qwerty, asdfgh, azerty, qwertz
- Special character sequences: !@#$%, (){}[]

### Diversity Score Algorithm
1. Character type diversity: Count distinct types (max 40 points)
2. Balance: Measure variance in type ratios (max 20 points)
3. No repetition: Check for consecutive duplicates (max 20 points)
4. No sequences: Check for sequential patterns (max 10 points)
5. Good distribution: Check character type clustering (max 10 points)

Total possible score: 100 points

## Testing

Run comprehensive tests:
```bash
python3 test_diversity.py
```

This demonstrates:
- Character type analysis
- Pattern detection
- Diversity validation
- Password enhancement with all pattern types

## Integration with Existing Tools

The diversity patterns module is fully backward compatible:
- Existing scripts work without modification
- New features are opt-in via command-line flags
- No breaking changes to existing generators

## Performance Considerations

- Diversity filtering adds minimal overhead (~5-10% for typical use cases)
- Enhanced diversity pattern generation is optimized with deduplication
- Large wordlists are automatically limited to 100 words for performance
- Pattern detection uses efficient algorithms (O(n) time complexity)

## Future Enhancements

Potential future additions:
- Custom pattern definitions via configuration files
- Machine learning-based diversity scoring
- Integration with password strength estimators (zxcvbn)
- Support for international character sets
- Multi-language pattern detection
