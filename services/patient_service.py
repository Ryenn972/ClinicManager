from __future__ import annotations
from typing import Dict, List, Optional
from models.patient import Patient
from utils.decorators import log_action, validate_patient

class PatientService:
    def __init__(self):
        self.patients: Dict[str, Patient] = {}

    @log_action("Ajout d'un patient")
    def ajouter_patient(self, patient: Patient) -> None:
        self.patients[patient.security_number] = patient

    @validate_patient
    def get_patient(self, security_number: str) -> Patient:
        return self.patients[security_number]

    def rechercher_patient(self, security_number: str) -> Optional[Patient]:
        return self.patients.get(security_number)

    def lister_patients(self) -> List[Patient]:
        return list(self.patients.values())

    def to_dict(self) -> Dict[str, dict]:
        return {nss: p.to_dict() for nss, p in self.patients.items()}

    def load_from_dict(self, data: Dict[str, dict]) -> None:
        self.patients = {nss: Patient.from_dict(pdata) for nss, pdata in data.items()}
