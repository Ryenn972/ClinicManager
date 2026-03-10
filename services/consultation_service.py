from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Optional
from models.consultation import Consultation, STATUT_PLANIFIEE
from utils.decorators import log_action
from utils.exceptions import ConsultationNotFoundError

class ConsultationService:
    def __init__(self):
        self.consultations: Dict[str, Consultation] = {}

    @log_action("Planification d'une consultation")
    def planifier_consultation(self, consultation: Consultation) -> None:
        self.consultations[consultation.id] = consultation

    def get_consultation(self, consultation_id: str) -> Consultation:
        c = self.consultations.get(consultation_id)
        if c is None:
            raise ConsultationNotFoundError(f"Consultation introuvable (id={consultation_id}).")
        return c

    def consultations_a_venir(self, now: Optional[datetime] = None) -> List[Consultation]:
        now = now or datetime.now()
        return sorted(
            [c for c in self.consultations.values() if c.statut == STATUT_PLANIFIEE and c.date_heure >= now],
            key=lambda x: x.date_heure,
        )

    def toutes_consultations_patient(self, patient_nss: str) -> List[Consultation]:
        return sorted(
            [c for c in self.consultations.values() if c.patient_nss == patient_nss],
            key=lambda x: x.date_heure,
        )

    def to_dict(self) -> Dict[str, dict]:
        return {cid: c.to_dict() for cid, c in self.consultations.items()}

    def load_from_dict(self, data: Dict[str, dict]) -> None:
        self.consultations = {cid: Consultation.from_dict(cdata) for cid, cdata in data.items()}
