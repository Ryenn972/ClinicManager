import os
from datetime import datetime
from functools import wraps
from utils.exceptions import PatientNotFoundError

def log_action(description: str):
    """Log une action dans logs.txt (au même niveau que main.py)."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Log dans le répertoire racine du projet (là où se trouve main.py)
            project_root = os.path.dirname(os.path.dirname(__file__))
            log_path = os.path.join(project_root, "logs.txt")
            with open(log_path, "a", encoding="utf-8") as log:
                log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Action effectuée : {description}\n")
            return result
        return wrapper
    return decorator

def validate_patient(func):
    """Vérifie qu'un patient existe dans self.patients[security_number]."""
    @wraps(func)
    def wrapper(self, security_number, *args, **kwargs):
        if security_number not in self.patients:
            raise PatientNotFoundError(f"Patient introuvable (NSS={security_number}).")
        return func(self, security_number, *args, **kwargs)
    return wrapper
