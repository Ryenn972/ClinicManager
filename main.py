from __future__ import annotations

import os
from datetime import datetime, date

from models.patient import Patient
from models.consultation import Consultation
from models.prescription import (
    PrescriptionMedicamenteuse,
    PrescriptionExamen,
    PrescriptionKinesitherapie,
)
from services.cabinet_manager import CabinetManager
from utils.exceptions import (
    PatientNotFoundError,
    ConsultationNotFoundError,
    InvalidSecurityNumberError,
    InvalidConsultationStatusError,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "cabinet_data.json")

def input_date(prompt: str) -> date:
    while True:
        s = input(prompt).strip()
        try:
            # format attendu: YYYY-MM-DD
            return date.fromisoformat(s)
        except ValueError:
            print("❌ Date invalide. Format attendu: YYYY-MM-DD")

def input_datetime(prompt: str) -> datetime:
    while True:
        s = input(prompt).strip()
        try:
            # format attendu: YYYY-MM-DD HH:MM
            return datetime.strptime(s, "%Y-%m-%d %H:%M")
        except ValueError:
            print("❌ Date/heure invalide. Format attendu: YYYY-MM-DD HH:MM")

def print_patient(p: Patient) -> None:
    print(f"- NSS: {p.security_number} | {p.nom} {p.prenom} | Né(e) le {p.date_naissance.isoformat()} | Âge: {p.age}")
    print(f"  Adresse: {p.adresse} | Tél: {p.telephone}")
    print(f"  Consultations: {len(p.consultations_ids)}")

def print_consultation(c: Consultation) -> None:
    print(f"- ID: {c.id} | {c.date_heure.strftime('%Y-%m-%d %H:%M')} | Patient NSS: {c.patient_nss}")
    print(f"  Médecin: {c.medecin} | Motif: {c.motif} | Statut: {c.statut}")
    if c.diagnostic:
        print(f"  Diagnostic: {c.diagnostic}")
    if c.prescriptions:
        print("  Prescriptions:")
        for p in c.prescriptions:
            print(f"    • {p.afficher_details()}")

def menu():
    print("\n=== Cabinet médical (console) ===")
    print("1) Ajouter un patient")
    print("2) Rechercher un patient (par NSS)")
    print("3) Lister tous les patients")
    print("4) Afficher l'historique complet d'un patient")
    print("5) Planifier une consultation")
    print("6) Afficher les consultations à venir")
    print("7) Marquer une consultation comme réalisée")
    print("8) Annuler une consultation")
    print("9) Ajouter un diagnostic à une consultation réalisée")
    print("10) Ajouter une prescription à une consultation réalisée")
    print("0) Quitter")

def generate_consultation_id(nss: str, dt: datetime) -> str:
    # Identifiant simple et lisible
    return f"C-{nss}-{dt.strftime('%Y%m%d%H%M%S')}"

def main():
    manager = CabinetManager(DATA_PATH)
    print("✅ Données chargées depuis:", DATA_PATH)

    while True:
        menu()
        choice = input("\nVotre choix: ").strip()

        try:
            if choice == "1":
                nss = input("NSS (15 chiffres): ").strip()
                nom = input("Nom: ").strip()
                prenom = input("Prénom: ").strip()
                dn = input_date("Date de naissance (YYYY-MM-DD): ")
                adresse = input("Adresse: ").strip()
                tel = input("Téléphone: ").strip()
                patient = Patient(_security_number=nss, nom=nom, prenom=prenom, date_naissance=dn, adresse=adresse, telephone=tel)
                manager.add_patient(patient)
                print("✅ Patient ajouté.")
                print_patient(patient)

            elif choice == "2":
                nss = input("NSS: ").strip()
                p = manager.get_patient(nss)
                print("✅ Patient trouvé :")
                print_patient(p)

            elif choice == "3":
                patients = manager.list_patients()
                if not patients:
                    print("ℹ️ Aucun patient enregistré.")
                else:
                    print(f"📋 {len(patients)} patient(s) :")
                    for p in patients:
                        print_patient(p)

            elif choice == "4":
                nss = input("NSS: ").strip()
                history = manager.history_for_patient(nss)
                print(f"📚 Historique consultations (NSS={nss}) — {len(history)} consultation(s)")
                for c in history:
                    print_consultation(c)

            elif choice == "5":
                nss = input("NSS du patient: ").strip()
                dt = input_datetime("Date/heure (YYYY-MM-DD HH:MM): ")
                medecin = input("Médecin: ").strip()
                motif = input("Motif: ").strip()
                cid = generate_consultation_id(nss, dt)
                consult = Consultation(id=cid, date_heure=dt, patient_nss=nss, medecin=medecin, motif=motif)
                manager.schedule_consultation(consult)
                print("✅ Consultation planifiée.")
                print_consultation(consult)

            elif choice == "6":
                upcoming = manager.upcoming()
                if not upcoming:
                    print("ℹ️ Aucune consultation à venir.")
                else:
                    print(f"📅 Consultations à venir — {len(upcoming)}")
                    for c in upcoming:
                        print_consultation(c)

            elif choice == "7":
                cid = input("ID consultation: ").strip()
                manager.mark_done(cid)
                c = manager.consultation_service.get_consultation(cid)
                print("✅ Consultation marquée comme réalisée.")
                print_consultation(c)

            elif choice == "8":
                cid = input("ID consultation: ").strip()
                manager.cancel(cid)
                c = manager.consultation_service.get_consultation(cid)
                print("✅ Consultation annulée.")
                print_consultation(c)

            elif choice == "9":
                cid = input("ID consultation: ").strip()
                diag = input("Diagnostic: ").strip()
                manager.add_diagnostic(cid, diag)
                c = manager.consultation_service.get_consultation(cid)
                print("✅ Diagnostic ajouté.")
                print_consultation(c)

            elif choice == "10":
                cid = input("ID consultation: ").strip()
                print("Type de prescription:")
                print("  1) Médicamenteuse")
                print("  2) Examen")
                print("  3) Kinésithérapie")
                t = input("Choix: ").strip()

                if t == "1":
                    medicament = input("Médicament: ").strip()
                    dosage = input("Dosage: ").strip()
                    frequence = input("Fréquence: ").strip()
                    duree = input("Durée: ").strip()
                    p = PrescriptionMedicamenteuse(medicament, dosage, frequence, duree)
                elif t == "2":
                    type_examen = input("Type d'examen (radio/analyse/...): ").strip()
                    labo = input("Laboratoire recommandé: ").strip()
                    p = PrescriptionExamen(type_examen, labo)
                elif t == "3":
                    nb = int(input("Nombre de séances: ").strip())
                    zone = input("Zone à traiter: ").strip()
                    duree = input("Durée: ").strip()
                    p = PrescriptionKinesitherapie(nb, zone, duree)
                else:
                    print("❌ Choix invalide.")
                    continue

                manager.add_prescription(cid, p)
                c = manager.consultation_service.get_consultation(cid)
                print("✅ Prescription ajoutée.")
                print_consultation(c)

            elif choice == "0":
                print("👋 Au revoir.")
                break
            else:
                print("❌ Choix invalide.")

        except (PatientNotFoundError, ConsultationNotFoundError, InvalidSecurityNumberError, InvalidConsultationStatusError) as e:
            print(f"❌ Erreur: {e}")
        except ValueError as e:
            print(f"❌ Erreur de saisie: {e}")

if __name__ == "__main__":
    main()
