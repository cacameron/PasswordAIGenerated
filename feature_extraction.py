
#PasswordGuard AI Feature Extraction
import re


# 1. DETECT REPEATED CHARACTERS
def detect_repeated_characters(password):

    return int(
        len(set(password)) < len(password)
    )


# 2. DETECT SEQUENTIAL PATTERNS
def detect_sequential_patterns(password):

    sequences = [
        "123", "234", "345", "456", "567",
        "678", "789", "890",
        "abc", "bcd", "cde", "def", "efg",
        "fgh", "ghi", "hij", "ijk",
        "qwe", "wer", "ert", "rty",
        "tyu", "yui", "uio", "iop"
    ]

    password = password.lower()

    return int(any(
        sequence in password
        for sequence in sequences
    ))


# 3. DETECT COMMON PASSWORD PATTERNS
def detect_common_patterns(password):

    patterns = [
        r"password",
        r"admin",
        r"welcome",
        r"qwerty",
        r"letmein",
        r"123456"
    ]

    password = password.lower()

    return int(any(
        re.search(pattern, password)
        for pattern in patterns
    ))


# 4. EXTRACT PASSWORD FEATURES
def extract_features(password):

    features = {

        # Password length
        "length": len(password),

        # Character counts
        "uppercase_count": sum(c.isupper() for c in password),
        "lowercase_count": sum(c.islower() for c in password),
        "digit_count": sum(c.isdigit() for c in password),
        "special_count": sum(
            not c.isalnum() and not c.isspace()
            for c in password
        ),

        # Character presence
        "has_uppercase": int(any(c.isupper() for c in password)),
        "has_lowercase": int(any(c.islower() for c in password)),
        "has_digits": int(any(c.isdigit() for c in password)),
        "has_special": int(any(
            not c.isalnum() and not c.isspace()
            for c in password
        )),

        # Repeated consecutive characters
        "has_repeated_char": int(any(
            password[i] == password[i + 1]
            for i in range(len(password) - 1)
        )),

        # Additional vulnerability features
        "has_repeated_chars": detect_repeated_characters(password),
        "has_sequential_pattern": detect_sequential_patterns(password),
        "has_common_pattern": detect_common_patterns(password)
    }

    return features


# 5. TEST FEATURE EXTRACTION
if __name__ == "__main__":

    sample_password = "Password123412!"

    results = extract_features(sample_password)

    print("\nFeature Extraction Results:")
    print("---------------------------")

    for feature, value in results.items():

        print(feature, ":", value)
