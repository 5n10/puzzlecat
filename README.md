# PuzzleCat - Advanced Password Generation Suite

A comprehensive suite of password generators with advanced character diversity patterns for security testing and password cracking research.

> **⚠️ Security Notice**: This tool generates and outputs passwords in plain text for security research and testing purposes. Generated passwords are test data, not actual user credentials. All password output is intentional and required for the tool's functionality.

## Features

- **Multiple Generator Types**: Basic, advanced hybrid, and super advanced with 13+ pattern types
- **Character Diversity Patterns**: Ensure strong passwords with balanced character types
- **Pattern Detection**: Avoid weak patterns like sequential chars and excessive repetition
- **Configurable Rules**: Customize diversity requirements for your specific needs
- **Diversity Scoring**: Quantitative assessment of password strength (0-100 scale)

## Components

### 1. Basic Mask Generator (`mask_generator.py`)
Simple brute-force password generation from character sets.

```bash
# Generate 4-character passwords from charset
python3 mask_generator.py 4 "abcABC123!@#"

# With diversity filtering
python3 mask_generator.py 4 "abcABC123!@#" --diversity 60
```

### 2. Advanced Hybrid Generator (`advanced_mask_generator.py`)
Combines wordlists with mask patterns (hashcat-style).

```bash
# Generate with wordlist and mask
python3 advanced_mask_generator.py wordlist.txt "?w?d?d?s"

# Placeholders: ?w=word, ?l=lowercase, ?u=uppercase, ?d=digit, ?s=special
```

### 3. Super Advanced Generator (`super_advanced_mask_generator.py`)
Comprehensive pattern library with 13 specialized generators.

```bash
# Generate specific pattern types
python3 super_advanced_mask_generator.py --patterns crypto-terms

# Generate all patterns
python3 super_advanced_mask_generator.py --patterns all --wordlist wordlist.txt \
    --start-year 2020 --end-year 2024

# Use enhanced diversity patterns (NEW!)
python3 super_advanced_mask_generator.py --patterns enhanced-diversity \
    --min-diversity-score 80 --strict-rules
```

**Available Pattern Types:**
- `dates` - Date-based combinations
- `repeating` - Repetition and alternation patterns
- `crypto-terms` - Cryptocurrency vocabulary
- `common-words` - Common password words
- `numerical` - Extended numerical patterns
- `sentences` - Sentence structures
- `leet` - Leetspeak variations
- `multilingual` - Multi-language terms
- `typos` - Common typos
- `years` - Year combinations
- `dictionary` - Word combinations
- `mixed` - Mixed-case alphanumeric
- `enhanced-diversity` - **NEW!** Advanced diversity patterns

### 4. Character Diversity Patterns Module (`diversity_patterns.py`)
**NEW!** Core library for analyzing and ensuring password character diversity.

```python
from diversity_patterns import calculate_diversity_score, validate_diversity, DiversityRule

# Calculate diversity score
score = calculate_diversity_score("P@ssw0rd!")  # Returns: 93.4

# Validate against rules
rule = DiversityRule(min_uppercase=1, min_lowercase=1, min_digits=1, min_special=1)
is_valid, violations = validate_diversity("P@ssw0rd!", rule)
```

See [DIVERSITY_PATTERNS.md](DIVERSITY_PATTERNS.md) for comprehensive documentation.

## New: Enhanced Diversity Patterns

The enhanced diversity pattern generator provides:

✓ **Balanced Character Types**: Ensures uppercase, lowercase, digits, and special characters  
✓ **Pattern Detection**: Avoids sequential patterns (abc, 123, qwerty)  
✓ **No Excessive Repetition**: Prevents character repetition (aaa, 111)  
✓ **Good Distribution**: Avoids clustering of same character types  
✓ **Configurable Scoring**: Set minimum diversity scores (0-100)  
✓ **Multiple Pattern Types**: mixed, sandwich, alternating, distributed  

### Quick Start with Diversity Patterns

```bash
# Generate high-quality passwords
python3 super_advanced_mask_generator.py --patterns enhanced-diversity

# Set minimum diversity score (0-100)
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --min-diversity-score 85

# Enable strict validation
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --strict-rules

# Use custom wordlist
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --wordlist my_words.txt
```

### Testing Diversity Features

Run the comprehensive test suite:

```bash
python3 test_diversity.py
```

This demonstrates:
- Character type analysis
- Pattern detection capabilities
- Diversity validation rules
- Password enhancement patterns

## Installation

No dependencies required - uses Python standard library only.

```bash
# Clone the repository
git clone https://github.com/5n10sndkts-eng/puzzlecat.git
cd puzzlecat

# Run any generator
python3 mask_generator.py 4 "abc123"
```

## Requirements

- Python 3.6 or higher
- No external dependencies

## Usage Examples

### Example 1: High-Security Password Generation
```bash
python3 super_advanced_mask_generator.py \
    --patterns enhanced-diversity \
    --min-diversity-score 90 \
    --strict-rules \
    --wordlist corporate_words.txt
```

### Example 2: Cryptocurrency Wallet Testing
```bash
python3 super_advanced_mask_generator.py \
    --patterns crypto-terms years enhanced-diversity
```

### Example 3: Date-Based Patterns
```bash
python3 super_advanced_mask_generator.py \
    --patterns dates \
    --wordlist names.txt \
    --start-year 1990 \
    --end-year 2024 \
    --date-formats "MMDDYYYY,YYYYMMDD" \
    --capitalize
```

### Example 4: Diversity-Filtered Brute Force
```bash
# Only generate passwords with good diversity
python3 mask_generator.py 6 "abcABC123!@#" --diversity 70
```

## Diversity Score Interpretation

| Score | Quality | Description |
|-------|---------|-------------|
| 90-100 | Excellent | Perfect balance, no weak patterns |
| 75-89 | Good | Strong diversity, minor issues possible |
| 60-74 | Fair | Acceptable diversity, some clustering |
| 40-59 | Poor | Limited types or pattern issues |
| 0-39 | Very Poor | Minimal diversity, weak patterns |

## Pattern Types Explained

### Enhanced Diversity Patterns

**Mixed**: `Secure123!`, `!Bitcoin321`  
Standard combinations with all character types

**Sandwich**: `!Secure123!`, `@Bitcoin321@`  
Special characters wrap the password

**Alternating**: `Sec123!ure`, `Bit321@coin`  
Interleaved character types

**Distributed**: `Se!cu123re`, `Bi!tc321oin`  
Optimal distribution throughout

## Command-Line Options

### Super Advanced Generator
```
--patterns TYPE [TYPE ...]     Pattern type(s) to generate
--wordlist PATH                 Wordlist file path
--start-year YEAR              Start year for date patterns
--end-year YEAR                End year for date patterns
--min-diversity-score SCORE    Minimum diversity score (0-100)
--strict-rules                 Enable strict validation
```

### Basic Generator
```
LENGTH                         Password length
CHARSET                        Character set to use
--diversity SCORE              Enable diversity filtering with min score
```

## Use Cases

- **Security Research**: Generate test passwords for vulnerability assessment
- **Password Cracking**: Create targeted wordlists for penetration testing
- **Compliance Testing**: Validate password policies against real-world patterns
- **Education**: Demonstrate weak vs. strong password patterns

## Best Practices

1. **Use diversity scoring** for production password generation (score ≥ 70)
2. **Enable strict rules** when security is critical
3. **Combine patterns** for comprehensive coverage
4. **Test outputs** with test_diversity.py before deployment
5. **Customize rules** to match specific security requirements

## Performance

- Basic generator: ~1M passwords/second (depends on charset/length)
- Advanced generator: ~100K passwords/second (with wordlist processing)
- Super advanced: Varies by pattern type (optimized with deduplication)
- Diversity filtering: ~5-10% overhead

## Testing

### Run Diversity Tests
```bash
python3 test_diversity.py
```

### Manual Testing
```bash
# Test basic generator
python3 mask_generator.py 3 abc | head -20

# Test advanced generator
python3 advanced_mask_generator.py wordlist.txt "?w?d?d" | head -20

# Test super advanced generator
python3 super_advanced_mask_generator.py --patterns mixed | head -20

# Test diversity patterns
python3 super_advanced_mask_generator.py --patterns enhanced-diversity | head -20
```

## Documentation

- [DIVERSITY_PATTERNS.md](DIVERSITY_PATTERNS.md) - Comprehensive diversity patterns documentation
- Code comments inline with each function
- Examples in test_diversity.py

## License

This is a research and educational tool. Use responsibly and only on systems you own or have permission to test.

## Contributing

Contributions welcome! Areas for enhancement:
- Additional pattern types
- Performance optimizations
- Custom configuration file support
- Integration with password strength estimators

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Acknowledgments

- Inspired by hashcat mask attack modes
- Built for cryptocurrency security research
- Enhanced with modern password security best practices

---

**⚠️ Ethical Use Notice**: This tool is intended for legitimate security testing, research, and educational purposes only. Always obtain proper authorization before testing systems you do not own.
