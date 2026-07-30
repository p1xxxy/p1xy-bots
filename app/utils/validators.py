import re

def normalize_phone(raw_phone: str) -> str | None:
    digits = re.sub(r'\D', '', raw_phone)
    if len(digits) == 10:
        return "+7" + digits
    elif len(digits) == 11 and digits[0] == '8':
        return "+7" + digits[1:]
    elif len(digits) == 11 and digits[0] == '7':
        return "+" + digits
    else:
        return None

def validate_name(raw_name: str) -> bool:
    cleaned_name = raw_name.strip()
    
    if cleaned_name == "":
        return False
   
    has_letter = re.search(r'[а-яА-Яa-zA-Z]',raw_name)
    if not has_letter:
        return False
    
    has_digit = re.search(r"\d", cleaned_name)
    if has_digit:
        return False
    return True

def validate_email(raw_email: str) -> bool:
    cleaned_email = raw_email.strip()
    
    if cleaned_email == "":
        return False
    
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, cleaned_email):
        return False
    
    return True