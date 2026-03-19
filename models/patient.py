from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Any
from utils.validators import validate_security_number, calculate_age

@dataclass
class Patient:
    _security_number: str
    nom: str
    prenom: str
    date_naissance: date
    adresse: str
    telephone: str
    consultations_ids: List[str] = field(default_factory=list)

    def __post_init__(self):
        validate_security_number(self._security_number)

    @property
    def security_number(self) -> str:
        return self._security_number

    @property
    def age(self) -> int:
        return calculate_age(self.date_naissance)

    def ajouter_consultation_id(self, consultation_id: str):
        if consultation_id not in self.consultations_ids:
            self.consultations_ids.append(consultation_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "security_number": self._security_number,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance.isoformat(),
            "adresse": self.adresse,
            "telephone": self.telephone,
            "consultations_ids": list(self.consultations_ids),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Patient":
        return Patient(
            _security_number=data["security_number"],
            nom=data["nom"],
            prenom=data["prenom"],
            date_naissance=date.fromisoformat(data["date_naissance"]),
            adresse=data["adresse"],
            telephone=data["telephone"],
            consultations_ids=data.get("consultations_ids", []),
        )
