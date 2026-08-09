
def validate_password(password: str) -> bool:
    return 8 <= len(password) <= 16 and " " not in password

def validate_username(username: str) -> bool:
    return 3 <= len(username) <= 10 and " " not in username

