from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from utils.exceptions import InvalidConsultationStatusError
from models.prescription import Prescription

STATUT_PLANIFIEE = "planifiée"
STATUT_REALISEE = "réalisée"
STATUT_ANNULEE = "annulée"

@dataclass
class Consultation:
    id: str
    date_heure: datetime
    patient_nss: str
    medecin: str
    motif: str
    diagnostic: Optional[str] = None
    prescriptions: List[Prescription] = field(default_factory=list)
    statut: str = STATUT_PLANIFIEE

    def _ensure_modifiable(self):
        if self.statut != STATUT_PLANIFIEE:
            raise InvalidConsultationStatusError("La consultation n'est modifiable que si elle est planifiée.")

    def annuler(self):
        self._ensure_modifiable()
        self.statut = STATUT_ANNULEE

    def realiser(self):
        self._ensure_modifiable()
        self.statut = STATUT_REALISEE

    def ajouter_diagnostic(self, diagnostic: str):
        if self.statut != STATUT_REALISEE:
            raise InvalidConsultationStatusError("Diagnostic autorisé uniquement pour une consultation réalisée.")
        self.diagnostic = diagnostic

    def ajouter_prescription(self, prescription: Prescription):
        if self.statut != STATUT_REALISEE:
            raise InvalidConsultationStatusError("Prescription autorisée uniquement pour une consultation réalisée.")
        self.prescriptions.append(prescription)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "date_heure": self.date_heure.isoformat(),
            "patient_nss": self.patient_nss,
            "medecin": self.medecin,
            "motif": self.motif,
            "diagnostic": self.diagnostic,
            "prescriptions": [p.to_dict() for p in self.prescriptions],
            "statut": self.statut,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Consultation":
        return Consultation(
            id=data["id"],
            date_heure=datetime.fromisoformat(data["date_heure"]),
            patient_nss=data["patient_nss"],
            medecin=data["medecin"],
            motif=data["motif"],
            diagnostic=data.get("diagnostic"),
            prescriptions=[Prescription.from_dict(p) for p in data.get("prescriptions", [])],
            statut=data.get("statut", STATUT_PLANIFIEE),
        )
