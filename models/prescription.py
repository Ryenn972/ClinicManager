from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Type

class Prescription(ABC):
    def __init__(self, traitement: str, posologie: str, duree: str):
        self.traitement = traitement
        self.posologie = posologie
        self.duree = duree

    @abstractmethod
    def afficher_details(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Prescription":
        p_type = data.get("type")
        mapping: Dict[str, Type[Prescription]] = {
            "PrescriptionMedicamenteuse": PrescriptionMedicamenteuse,
            "PrescriptionExamen": PrescriptionExamen,
            "PrescriptionKinesitherapie": PrescriptionKinesitherapie,
        }
        cls = mapping.get(p_type)
        if cls is None:
            raise ValueError(f"Type de prescription inconnu: {p_type}")
        return cls._from_dict(data)  # type: ignore

class PrescriptionMedicamenteuse(Prescription):
    def __init__(self, medicament: str, dosage: str, frequence: str, duree: str):
        super().__init__(medicament, dosage, duree)
        self.frequence = frequence

    def afficher_details(self) -> str:
        return (
            f"[Médicamenteuse] Médicament: {self.traitement} | Dosage: {self.posologie} | "
            f"Fréquence: {self.frequence} | Durée: {self.duree}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "medicament": self.traitement,
            "dosage": self.posologie,
            "frequence": self.frequence,
            "duree": self.duree,
        }

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "PrescriptionMedicamenteuse":
        return PrescriptionMedicamenteuse(
            medicament=data["medicament"],
            dosage=data["dosage"],
            frequence=data["frequence"],
            duree=data["duree"],
        )

class PrescriptionExamen(Prescription):
    def __init__(self, type_examen: str, laboratoire: str, duree: str = "N/A"):
        super().__init__(type_examen, "N/A", duree)
        self.laboratoire = laboratoire

    def afficher_details(self) -> str:
        return f"[Examen] Type: {self.traitement} | Laboratoire recommandé: {self.laboratoire}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "type_examen": self.traitement,
            "laboratoire": self.laboratoire,
            "duree": self.duree,
        }

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "PrescriptionExamen":
        return PrescriptionExamen(
            type_examen=data["type_examen"],
            laboratoire=data["laboratoire"],
            duree=data.get("duree", "N/A"),
        )

class PrescriptionKinesitherapie(Prescription):
    def __init__(self, nb_seances: int, zone: str, duree: str):
        super().__init__("Kinésithérapie", f"{nb_seances} séances", duree)
        self.nb_seances = nb_seances
        self.zone = zone

    def afficher_details(self) -> str:
        return f"[Kinésithérapie] Séances: {self.nb_seances} | Zone: {self.zone} | Durée: {self.duree}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "nb_seances": self.nb_seances,
            "zone": self.zone,
            "duree": self.duree,
        }

    @staticmethod
    def _from_dict(data: Dict[str, Any]) -> "PrescriptionKinesitherapie":
        return PrescriptionKinesitherapie(
            nb_seances=int(data["nb_seances"]),
            zone=data["zone"],
            duree=data["duree"],
        )
