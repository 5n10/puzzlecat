import itertools
import sys

def generate_passwords(charset, length):
    """
    Generates passwords of a given length from a given character set.
    This function uses itertools.product to create a generator that yields
    all possible combinations of characters from the charset.
    """
    for p in itertools.product(charset, repeat=length):
        yield "".join(p)

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
    # Usage: python mask_generator.py [length] [charset]
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except ValueError:
            print(f"Error: Invalid length provided. Using default: {default_length}", file=sys.stderr)
    
    if len(sys.argv) > 2:
        charset = sys.argv[2]

    print(f"Generating passwords of length {length} from charset '{charset}'...", file=sys.stderr)

    try:
        for password in generate_passwords(charset, length):
            print(password)
    except KeyboardInterrupt:
        # Allows you to stop the script gracefully with Ctrl+C
        print("\nPassword generation stopped.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
