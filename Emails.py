import re


def check_email(email):
    try:
        result = re.match(r'(^|\s)+[a-z0-9.]+@[a-z0-9]+\.[a-z]{2,5}(\s|$)+', email)
        return ''.join(str(result.group(0)).split())
    except Exception:
        return False
