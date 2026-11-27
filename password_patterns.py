"""Find predictable patterns without changing the password being tested."""

COMMON_WORDS = ["password", "admin", "welcome", "qwerty", "letmein"]
REPLACEMENTS = str.maketrans({
    "@": "a", "0": "o", "1": "i", "3": "e", "4": "a",
    "5": "s", "$": "s", "7": "t", "!": "i"
})


# FIND FORWARD OR REVERSED SEQUENCES OF THREE CHARACTERS
def has_sequence(password, sequences):
    password = password.casefold()
    for sequence in sequences:
        for index in range(len(sequence) - 2):
            pattern = sequence[index:index + 3]
            if pattern in password or pattern[::-1] in password:
                return True
    return False


def detect_sequential_patterns(password):
    return has_sequence(password, ["0123456789", "abcdefghijklmnopqrstuvwxyz"])


# FIND THREE OR MORE OF THE SAME CHARACTER IN A ROW
def detect_repeated_characters(password):
    return any(
        password[index] == password[index + 1] == password[index + 2]
        for index in range(len(password) - 2)
    )


# FIND A PASSWORD MADE BY REPEATING A SHORT BLOCK
def has_repeated_block(password):
    for block_size in range(1, min(8, len(password) // 2) + 1):
        if len(password) % block_size == 0:
            block = password[:block_size]
            if block * (len(password) // block_size) == password:
                return True
    return False


def detect_repeated_sequences(password):
    return detect_repeated_characters(password) or has_repeated_block(password)


# INCLUDE SIMPLE SUBSTITUTIONS, SUCH AS P@ssw0rd
def detect_common_patterns(password):
    normalized = password.casefold().translate(REPLACEMENTS)
    return any(word in normalized for word in COMMON_WORDS)


def detect_keyboard_patterns(password):
    return has_sequence(password, ["qwertyuiop", "asdfghjkl", "zxcvbnm"])


def detect_patterns(password):
    return {
        "sequence": detect_sequential_patterns(password),
        "repeated_characters": detect_repeated_characters(password),
        "repeated_block": has_repeated_block(password),
        "common_word": detect_common_patterns(password),
        "keyboard": detect_keyboard_patterns(password)
    }


if __name__ == "__main__":
    for pattern, found in detect_patterns("Password123!").items():
        print(pattern, ":", found)
