import itertools
import sys
from diversity_patterns import calculate_diversity_score, validate_diversity, DiversityRule

def generate_passwords(charset, length, min_diversity_score=0.0, use_diversity_filter=False):
    """
    Generates passwords of a given length from a given character set.
    This function uses itertools.product to create a generator that yields
    all possible combinations of characters from the charset.
    
    :param charset: Character set to use
    :param length: Length of passwords to generate
    :param min_diversity_score: Minimum diversity score to filter (0-100)
    :param use_diversity_filter: Whether to apply diversity filtering
    """
    diversity_rule = DiversityRule(
        min_uppercase=0,
        min_lowercase=0,
        min_digits=0,
        min_special=0,
        max_consecutive_same_type=4,
        max_repeated_char=2,
        avoid_sequential=True
    ) if use_diversity_filter else None
    
    for p in itertools.product(charset, repeat=length):
        password = "".join(p)
        
        if use_diversity_filter:
            # Apply diversity filtering
            score = calculate_diversity_score(password)
            if score < min_diversity_score:
                continue
            
            is_valid, _ = validate_diversity(password, diversity_rule)
            if not is_valid:
                continue
        
        yield password

def main():
    """
    Main function to generate passwords and print them to standard output.
    You can customize the character set and length here, or pass them
    as command-line arguments.
    """
    # --- Customize your mask here ---
    # Default character set (e.g., lowercase letters)
    default_charset = "abcdefghijklmnopqrstuvwxyz"
    # Default password length
    default_length = 4
    # --------------------------------

    length = default_length
    charset = default_charset

    # Allow overriding from the command line for flexibility
    # Usage: python mask_generator.py [length] [charset] [--diversity] [min_score]
    use_diversity = False
    min_score = 0.0
    
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except ValueError:
            print(f"Error: Invalid length provided. Using default: {default_length}", file=sys.stderr)
    
    if len(sys.argv) > 2:
        charset = sys.argv[2]
    
    if len(sys.argv) > 3 and sys.argv[3] == '--diversity':
        use_diversity = True
        print("Diversity filtering enabled", file=sys.stderr)
        
        # Parse min_score if provided
        if len(sys.argv) > 4:
            try:
                min_score = float(sys.argv[4])
            except ValueError:
                print(f"Error: Invalid min-score. Using default: 0.0", file=sys.stderr)

    print(f"Generating passwords of length {length} from charset '{charset}'...", file=sys.stderr)

    try:
        for password in generate_passwords(charset, length, min_score, use_diversity):
            # Note: Printing generated test passwords is intentional - this is a password generator tool
            print(password)
    except KeyboardInterrupt:
        # Allows you to stop the script gracefully with Ctrl+C
        print("\nPassword generation stopped.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
