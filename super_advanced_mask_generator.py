import argparse
import sys
import itertools
from datetime import date, timedelta
from diversity_patterns import (
    DiversityRule, 
    validate_diversity, 
    calculate_diversity_score,
    enhance_diversity
)

# ================================================================
# TIER 1: DATE-BASED PATTERNS
# ================================================================

def generate_dates(start_year, end_year):
    """Generator for all dates within a given year range."""
    start_dt = date(start_year, 1, 1)
    end_dt = date(end_year, 12, 31)
    for i in range((end_dt - start_dt).days + 1):
        yield start_dt + timedelta(days=i)

def generate_date_based_masks(wordlist_path, start_year, end_year, date_formats, separators, append_special, capitalize):
    """
    The main generator function that combines words with dates.
    """
    sys.stderr.write("[*] Generating date-based patterns...\n")
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Wordlist file not found at '{wordlist_path}'", file=sys.stderr)
        sys.exit(1)

    py_date_formats = [
        fmt.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d').replace('YY', '%y')
        for fmt in date_formats
    ]

    for word in words:
        if capitalize:
            word = word.capitalize()
        
        for dt in generate_dates(start_year, end_year):
            for fmt in py_date_formats:
                date_str = dt.strftime(fmt)
                
                for sep in separators:
                    base_candidate = f"{word}{sep}{date_str}"
                    
                    if append_special:
                        for char in append_special:
                            yield f"{base_candidate}{char}"
                    else:
                        yield base_candidate

# ================================================================
# TIER 2: REPEATING PATTERNS
# ================================================================

def generate_repeating_patterns():
    """Repeating and alternating patterns"""
    sys.stderr.write("[*] Generating repeating patterns...\n")

    short_words = ['btc', 'eth', 'xrp', 'ada', 'sol', 'dot', 'key']

    for word in short_words:
        # Repeat word
        for count in range(2, 5):
            yield word * count
            yield (word.capitalize()) * count

        # Alternating caps
        yield word.upper() + word.lower()
        yield word.lower() + word.upper()

    # Number patterns
    for digit in '0123456789':
        yield digit * 8
        yield digit * 10
        yield digit * 12

        # Alternating
        for other in '0123456789':
            if digit != other:
                pattern = (digit + other) * 4
                yield pattern
                pattern_6 = (digit + other) * 6
                yield pattern_6

# ================================================================
# TIER 3: EXTENDED CRYPTO VOCABULARY
# ================================================================

def generate_extended_crypto_terms():
    """Extended cryptocurrency terminology"""
    sys.stderr.write("[*] Generating extended crypto vocabulary...\n")

    terms = [
        # DeFi terms
        'defi', 'DeFi', 'yield', 'farm', 'stake', 'staking', 'liquidity', 'pool', 'swap', 'dex', 'DEX', 'uniswap',
        'aave', 'compound', 'curve', 'maker', 'dai', 'flash', 'loan', 'arbitrage', 'slippage',
        # NFT terms
        'nft', 'NFT', 'ape', 'punk', 'cryptopunk', 'bayc', 'opensea', 'jpeg', 'pfp', 'mint', 'minting',
        'metadata', 'collection', 'floor', 'sweep',
        # Layer 2 / Scaling
        'layer2', 'l2', 'lightning', 'ln', 'channel', 'rollup', 'optimism', 'arbitrum', 'polygon', 'matic',
        'zk', 'zkrollup', 'zksync', 'sidechains',
        # Consensus / Mining
        'mining', 'miner', 'asic', 'gpu', 'hashrate', 'proof', 'pow', 'pos', 'stake', 'validator',
        'block', 'blockchain', 'difficulty', 'nonce', 'mempool', 'fee', 'gas', 'gwei', 'sat', 'satoshi',
        # Wallets / Security
        'seed', 'phrase', 'mnemonic', 'bip39', 'bip32', 'private', 'public', 'address', 'multisig',
        'cold', 'hot', 'hardware', 'ledger', 'trezor', 'metamask', 'trust', 'exodus', 'electrum',
        # Market terms
        'bull', 'bear', 'crab', 'whale', 'shrimp', 'long', 'short', 'leverage', 'margin', 'perp',
        'futures', 'options', 'derivative', 'hedge', 'spot', 'market', 'limit', 'stop', 'loss',
        # Analysis
        'ta', 'technical', 'fundamental', 'chart', 'candle', 'wick', 'support', 'resistance',
        'fibonacci', 'fib', 'elliot', 'wave', 'rsi', 'macd', 'ema', 'sma', 'bollinger',
        # Regulation / Legal
        'sec', 'SEC', 'cftc', 'kyc', 'aml', 'regulation', 'legal', 'etf', 'ETF',
        'security', 'commodity', 'futures',
    ]

    for term in terms:
        yield term
        yield term.upper()
        yield term.capitalize()
        yield term + '123'
        yield term + '2024'
        yield 'my' + term
        if len(term) <= 6:
            yield term + 'wallet'
            yield term + 'moon'
            yield term + 'hodl'

# ================================================================
# TIER 4: COMMON WORD PATTERNS
# ================================================================

def generate_common_word_patterns():
    """Most common passwords from data breaches adapted for crypto"""
    sys.stderr.write("[*] Generating common word patterns...\n")

    common = [
        'love', 'money', 'god', 'baby', 'jesus', 'dragon', 'master', 'sunshine', 'princess', 'superman', 'michael',
        'charlie', 'freedom', 'ninja', 'mustang', 'mercedes', 'shadow', 'angel', 'cookie', 'whatever', 'tigger',
        'summer', 'hockey', 'ranger', 'buster', 'pepper', 'hunter', 'soccer', 'killer', 'harley', 'batman',
        'trust', 'fear', 'power', 'matrix', 'ghost', 'cheese', 'coffee', 'chicken', 'monkey', 'purple', 'flower',
        'pepper', 'starwars', 'computer', 'maverick', 'cookie', 'ginger', 'danger', 'nothing', 'everything', 'forever',
        'admin', 'user', 'root', 'guest', 'owner', 'king', 'queen', 'prince', 'duke', 'lord', 'lady', 'magic',
        'wizard', 'witch', 'pirate', 'viking', 'knight', 'warrior', 'fighter', 'soldier', 'captain', 'major',
        'general', 'admiral', 'marshal', 'tiger', 'lion', 'bear', 'wolf', 'eagle', 'hawk', 'falcon', 'snake',
        'spider', 'shark', 'dolphin', 'whale', 'panda', 'red', 'blue', 'green', 'black', 'white', 'gold', 'silver',
        'bronze', 'steel', 'iron', 'copper', 'diamond', 'ruby', 'sapphire', 'emerald', 'pearl', 'crystal', 'platinum',
    ]

    for word in common:
        yield word
        yield word.capitalize()
        yield word.upper()
        yield word + '1'
        yield word + '12'
        yield word + '123'
        yield word + '1234'
        yield word + '!'
        yield word + '!!'
        yield word + '@'
        yield word + '#'
        yield word + '$'
        yield '1' + word
        yield 'i' + word
        yield 'I' + word
        yield word + '2024'
        yield word + '2023'
        yield word + '2022'
        yield word + '2021'
        yield word + '2020'
        if len(word) >= 4:
            yield word + '123!'
            yield word + '12345'
            yield word + '!23'
            yield '123' + word

# ================================================================
# TIER 5: EXTENDED NUMERICAL PATTERNS
# ================================================================

def generate_extended_numerical():
    """Extended numerical patterns including crypto-relevant numbers"""
    sys.stderr.write("[*] Generating extended numerical patterns...\n")

    crypto_numbers = [
        '21000000', '2100000000000000', '100000000', '210000', '10', '2016', '144', '6', '51',
        '18446744073709551615',
        # Fibonacci
        '1', '2', '3', '5', '8', '13', '21', '34', '55', '89', '144', '233', '377', '610', '987', '1597', '2584',
        # Primes
        '2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71',
        '73', '79', '83', '89', '97', '101', '103', '107', '109',
        # Powers of 2
        '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192', '16384', '32768', '65536',
        # Round numbers
        '1000', '5000', '10000', '50000', '100000', '1000000', '10000000', '100000000',
    ]

    for num in crypto_numbers:
        yield num

    # Phone number patterns
    for area in ['212', '310', '415', '650', '408', '202', '312']:
        for exchange in range(200, 300, 10):
            yield f"{area}{exchange}0000"
            yield f"{area}{exchange}1234"

    # Repeating patterns
    for base in ['12', '123', '1234']:
        for count in range(2, 5):
            yield base * count

# ================================================================
# TIER 6: SENTENCE PATTERNS
# ================================================================

def generate_sentence_patterns():
    """Common sentence structures people use"""
    sys.stderr.write("[*] Generating sentence patterns...\n")

    subjects = ['i', 'I', 'we', 'my', 'My']
    verbs = ['love', 'like', 'hate', 'want', 'need', 'hodl', 'buy']
    objects = ['bitcoin', 'btc', 'crypto', 'money', 'eth', 'satoshi']

    for subj in subjects:
        for verb in verbs:
            for obj in objects:
                yield f"{subj}{verb}{obj}"
                yield f"{subj} {verb} {obj}"
                yield f"{subj}{verb}{obj}123"
                yield f"{subj}{verb}{obj}!"

    questions = [
        'when moon', 'when lambo', 'wen moon', 'wen lambo', 'why bitcoin', 'how bitcoin', 'what is bitcoin',
        'where bitcoin', 'who is satoshi',
    ]

    for q in questions:
        yield q
        yield q.replace(' ', '')
        yield q + '?'

# ================================================================
# TIER 7: LEETSPEAK EXTENDED
# ================================================================

def generate_extended_leet():
    """Extended leet speak patterns"""
    sys.stderr.write("[*] Generating extended leet patterns...\n")

    leet_words = {
        'bitcoin': ['b1tc01n', 'b!tc0!n', 'b17c01n', '8itcoin', '81tc01n'],
        'password': ['p4ssw0rd', 'p@ssw0rd', 'p4ssw()rd', 'passw0rd'],
        'satoshi': ['s4t0sh1', 's@t0shi', 's4t05h1', 'sat0shi'],
        'crypto': ['crypt0', 'cr1pt0', 'cryp70', 'c®yp†0'],
        'wallet': ['w4ll3t', 'w@llet', 'wa11et', 'w4113t'],
        'money': ['m0n3y', 'm()ney', 'm0ney', 'mon3y'],
        'ethereum': ['3th3r3um', 'eth3reum', '3thereum', 'eth3r3um'],
        'hodl': ['h0dl', 'h()dl', 'hodl', 'HODL'],
        'lambo': ['l4mb0', 'lam8o', '14mb0', 'l@mbo'],
        'moon': ['m00n', 'm()()n', 'm0on', 'mo0n'],
    }

    for word, variants in leet_words.items():
        for variant in variants:
            yield variant
            yield variant.upper()
            yield variant.capitalize()
            yield variant + '123'
            yield variant + '!'
            yield '!' + variant

# ================================================================
# TIER 8: MULTILINGUAL PATTERNS
# ================================================================

def generate_multilingual():
    """Common crypto words in other languages"""
    sys.stderr.write("[*] Generating multilingual patterns...\n")

    translations = {
        'es': ['bitcoin', 'dinero', 'moneda', 'billetera', 'clave', 'contraseña', 'secreto'],
        'fr': ['bitcoin', 'argent', 'monnaie', 'portefeuille', 'cle', 'motdepasse', 'secret'],
        'de': ['bitcoin', 'geld', 'munze', 'brieftasche', 'schlussel', 'passwort', 'geheim'],
        'pt': ['bitcoin', 'dinheiro', 'moeda', 'carteira', 'chave', 'senha', 'segredo'],
        'ru': ['bitkoin', 'dengi', 'koshelek', 'parol', 'sekret'],
        'zh': ['bitcoin', 'qian', 'qianbao', 'mima', 'mimi'],
        'ja': ['bitcoin', 'okane', 'saifu', 'pasuwado', 'himitsu'],
        'ko': ['bitcoin', 'don', 'jigap', 'bimil'],
    }

    for lang, words in translations.items():
        for word in words:
            yield word
            yield word.capitalize()
            yield word + '123'
            yield word + '2024'

# ================================================================
# TIER 9: TYPOS AND MISTAKES
# ================================================================

def generate_typos():
    """Common typos and mistakes"""
    sys.stderr.write("[*] Generating typo patterns...\n")

    typos = {
        'bitcoin': ['bitcion', 'bitcoim', 'bitocin', 'bicoin', 'bitvoin', 'bitcon', 'bitconi', 'bitcooin', 'bitcin'],
        'password': ['pasword', 'passord', 'passwrod', 'passwod', 'passowrd'],
        'satoshi': ['satosih', 'satos', 'satoshii', 'satoshhi', 'sato shi'],
        'wallet': ['walet', 'wlalet', 'walllet', 'walet', 'walelt'],
        'ethereum': ['etherium', 'etherum', 'ehthereum', 'ethreum'],
    }

    for correct, mistakes in typos.items():
        for typo in mistakes:
            yield typo
            yield typo.capitalize()
            yield typo + '123'

# ================================================================
# TIER 10: COMBINATIONS WITH YEARS
# ================================================================

def generate_year_combinations():
    """Extensive year combinations"""
    sys.stderr.write("[*] Generating year combinations...\n")

    bases = ['bitcoin', 'btc', 'crypto', 'satoshi', 'wallet', 'password', 'secret', 'key', 'money', 'hodl', 'eth',
             'ethereum', 'coin', 'chain', 'block', 'hash']

    years = list(range(2009, 2026))  # Bitcoin era
    years.extend(range(1970, 2010))  # Birth years

    for base in bases:
        for year in years:
            yield base + str(year)
            yield str(year) + base
            yield base.capitalize() + str(year)
            # Two digit years
            yield base + str(year)[-2:]
            yield str(year)[-2:] + base
            # With special chars
            yield base + str(year) + '!'
            yield base + str(year) + '@'
            yield base + str(year) + '#'

# ================================================================
# TIER 11: DICTIONARY COMBINATIONS
# ================================================================

def generate_dictionary_combos(wordlist_path):
    """Two and three-word combinations (very common in brainwallets)"""
    sys.stderr.write("[*] Generating dictionary combinations...\n")
    if not wordlist_path:
        sys.stderr.write("[!] Wordlist required for dictionary combinations. Skipping.\n")
        return

    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Wordlist file not found at '{wordlist_path}'", file=sys.stderr)
        return

    # Two-word combinations
    short_words = [w for w in words if 3 <= len(w) <= 8][:300]
    count = 0
    for w1, w2 in itertools.combinations(short_words, 2):
        if count > 50000: break
        count += 1
        yield w1 + w2
        yield w2 + w1
        yield w1.capitalize() + w2.capitalize()
        yield w1 + '_' + w2
        yield w1 + '-' + w2
        yield w1 + w2 + '123'
        yield w1 + w2 + '1'

    # Three-word combinations
    very_short = [w for w in words if 3 <= len(w) <= 6][:100]
    count = 0
    for w1, w2, w3 in itertools.combinations(very_short, 3):
        if count > 10000: break
        count += 1
        yield w1 + w2 + w3
        yield w1 + ' ' + w2 + ' ' + w3
        yield w1.capitalize() + w2.capitalize() + w3.capitalize()

# ================================================================
# TIER 12: MIXED CASE ALPHANUMERIC COMBINATIONS
# ================================================================

def generate_mixed_case_patterns(wordlist_path=None):
    """Combinations guaranteeing uppercase letters, digits, and special characters"""
    sys.stderr.write("[*] Generating mixed-case alphanumeric patterns...\n")

    defaults = [
        'bitcoin', 'crypto', 'wallet', 'satoshi', 'ethereum', 'ledger', 'trezor',
        'defender', 'guardian', 'secure', 'vault', 'freedom', 'passphrase',
    ]

    words = defaults
    if wordlist_path:
        try:
            with open(wordlist_path, 'r') as f:
                loaded = [line.strip() for line in f if line.strip()]
                if loaded:
                    words = loaded
        except FileNotFoundError:
            print(f"Error: Wordlist file not found at '{wordlist_path}'", file=sys.stderr)

    number_chunks = ['123', '321', '007', '1337', '2024', '2025', '69', '420']
    special_chars = list('!@#$%^&*?')
    seen = set()

    replacements = {
        'a': '@',
        's': '$',
        'o': '0',
        'i': '1',
        'e': '3',
        't': '7',
    }

    for word in words:
        base = word.strip()
        if not base:
            continue

        variants = {
            base.lower(),
            base.capitalize(),
            base.upper(),
        }

        alt = ''.join(ch.upper() if idx % 2 == 0 else ch.lower() for idx, ch in enumerate(base))
        variants.add(alt)

        leet_variant = ''.join(replacements.get(ch.lower(), ch) for ch in base.capitalize())
        variants.add(leet_variant)

        for variant in variants:
            if not any(c.isalpha() for c in variant):
                continue

            for numbers in number_chunks:
                for special in special_chars:
                    combos = [
                        f"{variant}{numbers}{special}",
                        f"{special}{variant}{numbers}",
                        f"{variant}{special}{numbers}",
                    ]

                    split_index = max(1, len(variant) // 2)
                    combos.append(f"{variant[:split_index]}{numbers}{special}{variant[split_index:]}")

                    for candidate in combos:
                        if candidate in seen:
                            continue

                        has_upper = any(c.isupper() for c in candidate)
                        has_digit = any(c.isdigit() for c in candidate)
                        has_special = any(not c.isalnum() for c in candidate)

                        if has_upper and has_digit and has_special:
                            seen.add(candidate)
                            yield candidate

# ================================================================
# TIER 13: ENHANCED DIVERSITY PATTERNS
# ================================================================

def generate_enhanced_diversity_patterns(wordlist_path=None, min_score=70.0, use_strict_rules=False):
    """
    Generate passwords with enhanced character diversity patterns.
    
    This uses the diversity_patterns module to ensure:
    - Proper distribution of character types (uppercase, lowercase, digits, special)
    - No excessive repetition (same character repeated > 2 times)
    - No sequential patterns (abc, 123, qwerty, etc.)
    - Good positional diversity (character types not clustered together)
    
    Positional diversity means avoiding consecutive characters of the same type.
    For example, "AAAA1111!!!!" has poor positional diversity, while
    "A1a!A2b@" has good positional diversity with types well-distributed.
    
    :param wordlist_path: Optional wordlist for base words
    :param min_score: Minimum diversity score (0-100)
    :param use_strict_rules: Whether to use strict diversity validation
    """
    sys.stderr.write("[*] Generating enhanced diversity patterns...\n")
    
    defaults = [
        'secure', 'crypto', 'wallet', 'bitcoin', 'guardian', 'vault', 'fortress',
        'shield', 'protect', 'defend', 'safety', 'privacy', 'liberty', 'master'
    ]
    
    words = defaults
    if wordlist_path:
        try:
            with open(wordlist_path, 'r') as f:
                loaded = [line.strip() for line in f if line.strip() and len(line.strip()) >= 4]
                if loaded:
                    words = loaded[:100]  # Limit for performance
        except FileNotFoundError:
            sys.stderr.write(f"[!] Wordlist not found, using defaults\n")
    
    number_sets = ['123', '321', '007', '2024', '8675', '1337']
    special_sets = ['!', '@', '#', '$', '!@', '@#', '#$']
    patterns = ['mixed', 'sandwich', 'alternating', 'distributed']
    
    # Define diversity rule
    rule = DiversityRule(
        min_uppercase=1,
        min_lowercase=1,
        min_digits=1,
        min_special=1,
        max_consecutive_same_type=3,
        max_repeated_char=2,
        avoid_sequential=True
    )
    
    seen = set()
    
    for word in words:
        base = word.strip()
        if not base or len(base) < 4:
            continue
        
        for numbers in number_sets:
            for special in special_sets:
                for pattern in patterns:
                    variations = enhance_diversity(base, numbers, special, pattern)
                    
                    for candidate in variations:
                        if candidate in seen:
                            continue
                        
                        # Calculate diversity score
                        score = calculate_diversity_score(candidate)
                        
                        if score >= min_score:
                            # Optionally validate with strict rules
                            if use_strict_rules:
                                is_valid, _ = validate_diversity(candidate, rule)
                                if not is_valid:
                                    continue
                            
                            seen.add(candidate)
                            yield candidate

# ================================================================
# MAIN GENERATION LOGIC
# ================================================================

def main():
    GENERATORS = {
        'dates': generate_date_based_masks,
        'repeating': generate_repeating_patterns,
        'crypto-terms': generate_extended_crypto_terms,
        'common-words': generate_common_word_patterns,
        'numerical': generate_extended_numerical,
        'sentences': generate_sentence_patterns,
        'leet': generate_extended_leet,
        'multilingual': generate_multilingual,
        'typos': generate_typos,
        'years': generate_year_combinations,
        'dictionary': generate_dictionary_combos,
        'mixed': generate_mixed_case_patterns,
        'enhanced-diversity': generate_enhanced_diversity_patterns,
    }

    parser = argparse.ArgumentParser(
        description="Super Advanced Hybrid Mask Generator with Multiple Strategies.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('--patterns', nargs='+', required=True, choices=list(GENERATORS.keys()) + ['all'],
                        help=f"One or more pattern types to generate. Choices: {', '.join(GENERATORS.keys())}, or 'all'.")

    # Arguments for 'dates' pattern
    parser.add_argument('--wordlist', help="Path to the wordlist file (required for 'dates' and 'dictionary').")
    parser.add_argument('--start-year', type=int, help="Start year for date generation (for 'dates').")
    parser.add_argument('--end-year', type=int, help="End year for date generation (for 'dates').")
    parser.add_argument('--date-formats', type=str, default="YYYYMMDD,MMDDYYYY,MMDDYY", help="Date formats for 'dates'.")
    parser.add_argument('--separators', type=str, default="", help="Separators for 'dates'.")
    parser.add_argument('--append-special', type=str, default="!@#$", help="Special characters to append for 'dates'.")
    parser.add_argument('--capitalize', action='store_true', help="Capitalize words for 'dates'.")
    
    # Arguments for 'enhanced-diversity' pattern
    parser.add_argument('--min-diversity-score', type=float, default=70.0, 
                        help="Minimum diversity score for 'enhanced-diversity' (0-100, default 70).")
    parser.add_argument('--strict-rules', action='store_true', 
                        help="Use strict diversity validation rules for 'enhanced-diversity'.")

    args = parser.parse_args()

    patterns_to_run = GENERATORS.keys() if 'all' in args.patterns else args.patterns

    for pattern_name in patterns_to_run:
        generator_func = GENERATORS[pattern_name]
        
        try:
            # Call generator with specific arguments if needed
            if pattern_name == 'dates':
                if not all([args.wordlist, args.start_year, args.end_year]):
                    parser.error("--wordlist, --start-year, and --end-year are required for the 'dates' pattern.")
                date_formats_list = args.date_formats.split(',')
                separators_list = args.separators.split(',')
                for password in generate_date_based_masks(args.wordlist, args.start_year, args.end_year, date_formats_list, separators_list, args.append_special, args.capitalize):
                    # Note: Printing generated test passwords is intentional - this is a password generator tool
                    print(password)
            elif pattern_name == 'dictionary':
                if not args.wordlist:
                    parser.error("--wordlist is required for the 'dictionary' pattern.")
                for password in generate_dictionary_combos(args.wordlist):
                    # Note: Printing generated test passwords is intentional - this is a password generator tool
                    print(password)
            elif pattern_name == 'mixed':
                for password in generate_mixed_case_patterns(args.wordlist):
                    # Note: Printing generated test passwords is intentional - this is a password generator tool
                    print(password)
            elif pattern_name == 'enhanced-diversity':
                for password in generate_enhanced_diversity_patterns(
                    args.wordlist, 
                    args.min_diversity_score, 
                    args.strict_rules
                ):
                    # Note: Printing generated test passwords is intentional - this is a password generator tool
                    print(password)
            else:
                for password in generator_func():
                    # Note: Printing generated test passwords is intentional - this is a password generator tool
                    print(password)

        except KeyboardInterrupt:
            print("\nPassword generation stopped.", file=sys.stderr)
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred in pattern '{pattern_name}': {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
