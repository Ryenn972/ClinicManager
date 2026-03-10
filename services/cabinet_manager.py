from __future__ import annotations
import os
from datetime import datetime
from typing import Optional
from models.patient import Patient
from models.consultation import Consultation
from models.prescription import Prescription
from services.patient_service import PatientService
from services.consultation_service import ConsultationService
from services.storage import load_json, save_json
from utils.exceptions import PatientNotFoundError

class CabinetManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.patient_service = PatientService()
        self.consultation_service = ConsultationService()
        self.load()

    def load(self) -> None:
        data = load_json(self.data_path)
        self.patient_service.load_from_dict(data.get("patients", {}))
        self.consultation_service.load_from_dict(data.get("consultations", {}))

    def save(self) -> None:
        data = {
            "patients": self.patient_service.to_dict(),
            "consultations": self.consultation_service.to_dict(),
        }
        save_json(self.data_path, data)

    # ---- Patient ----
    def add_patient(self, patient: Patient) -> None:
        self.patient_service.ajouter_patient(patient)
        self.save()

    def get_patient(self, nss: str) -> Patient:
        return self.patient_service.get_patient(nss)

    def list_patients(self):
        return self.patient_service.lister_patients()

    # ---- Consultation ----
    def schedule_consultation(self, consultation: Consultation) -> None:
        # patient must exist
        p = self.patient_service.rechercher_patient(consultation.patient_nss)
        if p is None:
            raise PatientNotFoundError(f"Patient introuvable (NSS={consultation.patient_nss}).")
        self.consultation_service.planifier_consultation(consultation)
        p.ajouter_consultation_id(consultation.id)
        self.save()

    def mark_done(self, consultation_id: str) -> None:
        c = self.consultation_service.get_consultation(consultation_id)
        c.realiser()
        self.save()

    def cancel(self, consultation_id: str) -> None:
        c = self.consultation_service.get_consultation(consultation_id)
        c.annuler()
        self.save()

    def add_diagnostic(self, consultation_id: str, diagnostic: str) -> None:
        c = self.consultation_service.get_consultation(consultation_id)
        c.ajouter_diagnostic(diagnostic)
        self.save()

    def add_prescription(self, consultation_id: str, prescription: Prescription) -> None:
        c = self.consultation_service.get_consultation(consultation_id)
        c.ajouter_prescription(prescription)
        self.save()

    def upcoming(self):
        return self.consultation_service.consultations_a_venir()

    def history_for_patient(self, nss: str):
        # validate patient exists
        self.patient_service.get_patient(nss)
        return self.consultation_service.toutes_consultations_patient(nss)
