'''or PasswordGuard AI, you could extract features such as:
length, uppercase, lowercase, digit count
special count, has uppercase, has lowercase
has digits, has special, has repeated chars, etc. 
'''

def exectract_features(password):

    features = { 
        # password length
        "lenght": len(password),
        # character counts
        "uppercase_count": sum(c.isupper() for c in password),
        "lowercase_count": sum(c.islower() for c in password),
        "digit_count": sum(c.isdigit() for c in password),
        "special_count": sum(not c.isalnum() and not c.isspace() for c in password),

        #character presence
        "has_uppercase": int(any(c.isupper() for c in password)),
        "has_lowercase": int(any(c.islower() for c in password)),
        "has_digits": int(any(c.isdigit() for c in password)),
        "has_special": int(any(not c.isalnum() and not c.isspace() for c in password)),

        #repeated characters
        "has_repeated_char": int(any(
            password[i] == password[i+1] 
            for i in range(len(password) - 1)))
    }
    return features

#test the feacture extractions

if __name__ == "__main__":

    sample_password = "Hello1234!"

    results = exectract_features(sample_password)

    print("Feature Extraction Results:")

    for feature, value in results.items():
        print(feature, ":", value)