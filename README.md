# ClinicManager 🏥

**ClinicManager** is a Python command-line application that simulates the management of a small medical practice.

The program allows a user (doctor or staff) to manage patients, schedule consultations, record diagnoses, and create prescriptions through an interactive console menu.

All data is stored in a JSON file and loaded automatically when the program starts.

---

## Features

- Patient registration and management
- Search patient by social security number (NSS)
- View patient consultation history
- Schedule consultations
- View upcoming consultations
- Mark consultations as completed
- Cancel consultations
- Add diagnoses to completed consultations
- Add different types of prescriptions:
  - Medication prescriptions
  - Medical examination prescriptions
  - Physiotherapy prescriptions
- Persistent data storage using JSON

---

## How It Works

The application runs entirely in the terminal and uses a simple numbered menu system.

Example menu:

=== Medical Practice (Console) ===

1. Add a patient

2. Search patient (by NSS)

3. List all patients

4. Show full patient history

5. Schedule a consultation

6. Show upcoming consultations

7. Mark consultation as completed

8. Cancel a consultation

9. Add diagnosis to consultation

10. Add prescription to consultation

0. Exit

The user simply enters the corresponding number to perform an action.

---

## Project Structure

The architecture follows a modular approach:

- **models** → data structures (Patient, Consultation, Prescriptions)
- **services** → application logic
- **utils** → custom exceptions
- **data** → persistent JSON storage

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ryenn972/ClinicManager.git
cd ClinicManager
python main.py
```

## Data Storage

All application data is stored in:

```data/cabinet_data.json```

This file is automatically created/updated when the application runs.

## Technologies Used

- Python

- Object-Oriented Programming

- JSON data persistence

- Command Line Interface (CLI)

## Learning Goals

This project was created to practice:

- Python object-oriented programming

- Application architecture (models / services separation)

- Exception handling

- File persistence with JSON

- Building a CLI application

## Possible Improvements

Future improvements could include:

- Database integration (SQLite / PostgreSQL)

- Graphical user interface (GUI)

- Authentication system

- Better search and filtering for patients

- Calendar visualization for consultations

- REST API version

## Author

Developed by [Ryenn M.](https://github.com/Ryenn972), [Nolhann G.](https://github.com/phelioume11), [Yarno C](https://github.com/Gosthwatching).
