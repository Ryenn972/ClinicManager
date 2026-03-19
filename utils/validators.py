import re
from datetime import date
from utils.exceptions import InvalidSecurityNumberError

def validate_security_number(number: str) -> bool:
    """Valide un NIR simplifié : 15 chiffres."""
    if not re.fullmatch(r"\d{15}", str(number)):
        raise InvalidSecurityNumberError("Le numéro de sécurité sociale doit contenir 15 chiffres.")
    return True

def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
