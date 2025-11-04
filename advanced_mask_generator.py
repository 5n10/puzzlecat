import itertools
import argparse
import sys

# Define standard hashcat-like character sets
CHARSETS = {
    'l': 'abcdefghijklmnopqrstuvwxyz',
    'u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'd': '0123456789',
    's': '!@#$%^&*()-_+=~[]{}|:;,.?'
}

def generate_hybrid_passwords(wordlist_path, mask):
    """
    Generates passwords by combining words from a wordlist with a mask.

    :param wordlist_path: Path to the wordlist file.
    :param mask: The mask pattern (e.g., '?w?d?d?s').
    """
    if '?w' not in mask:
        print("Error: Mask must include the '?w' placeholder for a word from the wordlist.", file=sys.stderr)
        return

    # Find all placeholders in the mask (e.g., ?d, ?s)
    placeholders = []
    i = 0
    while i < len(mask):
        if mask[i] == '?':
            if i + 1 < len(mask) and mask[i+1] in CHARSETS:
                placeholders.append(CHARSETS[mask[i+1]])
            elif i + 1 < len(mask) and mask[i+1] == 'w':
                # We will substitute the word here later
                placeholders.append(None) 
            else:
                # Treat as a literal '?'
                placeholders.append(['?'])
            i += 2
        else:
            placeholders.append([mask[i]])
            i += 1
    
    # Create the generator for the mask part
    mask_generators = [p for p in placeholders if p is not None]
    mask_product = itertools.product(*mask_generators)

    # Read the wordlist and generate passwords
    try:
        with open(wordlist_path, 'r') as f:
            for word in f:
                word = word.strip()
                if not word:
                    continue
                
                # Reset the product generator for each new word
                mask_product, temp_product = itertools.tee(itertools.product(*mask_generators))

                for p in temp_product:
                    p_list = list(p)
                    output_parts = []
                    for placeholder in placeholders:
                        if placeholder is None:
                            output_parts.append(word)
                        else:
                            output_parts.append(p_list.pop(0))
                    yield "".join(output_parts)

    except FileNotFoundError:
        print(f"Error: Wordlist file not found at '{wordlist_path}'", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Advanced hybrid mask generator for hashcat.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('wordlist', help="Path to the wordlist file.")
    parser.add_argument('mask', help="Mask pattern to apply.\n"
                                     "Use ?w for the word from the wordlist.\n"
                                     "Use ?l, ?u, ?d, ?s for charsets.\n"
                                     "Example: '?w?d?d' for 'word12'\n"
                                     "Example: '?s?w?s' for '!word!'")
    
    args = parser.parse_args()

    print(f"Starting advanced mask generation with wordlist '{args.wordlist}' and mask '{args.mask}'...", file=sys.stderr)

    try:
        for password in generate_hybrid_passwords(args.wordlist, args.mask):
            # Note: Printing generated test passwords is intentional - this is a password generator tool
            print(password)
    except KeyboardInterrupt:
        print("\nPassword generation stopped.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
