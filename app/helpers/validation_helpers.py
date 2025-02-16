def validate_name(name, name_type="Name"):
    if not name:
        return False, f"{name_type} is required."

    name = name.strip()

    if not all(c.isalpha() or c.isspace() for c in name):
        return False, f"{name_type} must contain only alphabetic characters."

    if len(name) < 1 or len(name) > 100:
        return False, f"{name_type} must be 1 - 100 characters long."

    return True, None  # None means no error, validation is successful
