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
