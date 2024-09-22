import sqlite3


# Create Tables
def create_tables():
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    # Create User Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS User (
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            given_name TEXT,
            first_name TEXT,
            username TEXT UNIQUE,
            email TEXT,
            phone_number TEXT,
            password TEXT,
            register_type TEXT
        )
    """
    )

    # Create Image Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Image (
            imageID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            file_path TEXT,
            date_uploaded DATE,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    # Create Medication Table (Updated)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Medication (
            medicationID INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_name TEXT,
            medication_type TEXT,
            userID INTEGER,
            file_path TEXT,
            date_medication_prescribed DATE,
            medication_treatment_used TEXT,
            side_effect TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    # Create Patient Info Table (Updated)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Patient_Info (
            patientID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            diagnosis TEXT,
            treatment_type TEXT,
            treatment_description TEXT,
            bone_mass_density REAL,
            progress_note TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    # Create Appointment Table (Updated)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Appointment (
            appointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            treatment_type TEXT,
            appointment_type TEXT,
            appointment_date DATE,
            appointment_time TIME,
            preop_date DATE,
            preop_time TIME,
            postop_date DATE,
            postop_time TIME,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    # Create Medical Profession Table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Medical_Profession (
            professionID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            given_name TEXT,
            first_name TEXT,
            role TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    conn.commit()
    conn.close()


def update_medication(
    medicationID,
    medication_name,
    medication_type,
    file_path,
    date_medication_prescribed,
    medication_treatment_used,
    side_effect,
):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Medication
        SET medication_name = ?, medication_type = ?, file_path = ?, date_medication_prescribed = ?, medication_treatment_used = ?, side_effect = ?
        WHERE medicationID = ?
    """,
        (
            medication_name,
            medication_type,
            file_path,
            date_medication_prescribed,
            medication_treatment_used,
            side_effect,
            medicationID,
        ),
    )

    conn.commit()
    conn.close()


def update_patient_info(
    patientID,
    diagnosis,
    treatment_type,
    treatment_description,
    bone_mass_density,
    progress_note,
):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Patient_Info
        SET diagnosis = ?, treatment_type = ?, treatment_description = ?, bone_mass_density = ?, progress_note = ?
        WHERE patientID = ?
    """,
        (
            diagnosis,
            treatment_type,
            treatment_description,
            bone_mass_density,
            progress_note,
            patientID,
        ),
    )

    conn.commit()
    conn.close()


def update_appointment(
    appointmentID,
    treatment_type,
    appointment_type,
    appointment_date,
    appointment_time,
    preop_date,
    preop_time,
    postop_date,
    postop_time,
):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Appointment
        SET treatment_type = ?, appointment_type = ?, appointment_date = ?, appointment_time = ?, preop_date = ?, preop_time = ?, postop_date = ?, postop_time = ?
        WHERE appointmentID = ?
    """,
        (
            treatment_type,
            appointment_type,
            appointment_date,
            appointment_time,
            preop_date,
            preop_time,
            postop_date,
            postop_time,
            appointmentID,
        ),
    )

    conn.commit()
    conn.close()


def delete_medication(medicationID):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Medication WHERE medicationID = ?", (medicationID,))

    conn.commit()
    conn.close()


def delete_patient_info(patientID):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Patient_Info WHERE patientID = ?", (patientID,))

    conn.commit()
    conn.close()


def delete_appointment(appointmentID):
    conn = sqlite3.connect("../databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Appointment WHERE appointmentID = ?", (appointmentID,))

    conn.commit()
    conn.close()


create_tables()
