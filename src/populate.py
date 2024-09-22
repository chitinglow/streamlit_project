import sqlite3

conn = sqlite3.connect("../databases/healthcare.db")
cursor = conn.cursor()


# Insert sample data into User table
def populate_users():
    users = [
        (
            "John",
            "Doe",
            "jdoe",
            "john.doe@example.com",
            "1234567890",
            "password1",
            "Professional",
        ),
        (
            "Jane",
            "Smith",
            "jsmith1",
            "jane.smith@example.com",
            "2345678901",
            "password2",
            "Professional",
        ),
        (
            "Alice",
            "Brown",
            "abrown",
            "alice.brown@example.com",
            "3456789012",
            "password3",
            "Member of Public",
        ),
        (
            "Bob",
            "White",
            "bwhite",
            "bob.white@example.com",
            "4567890123",
            "password4",
            "Member of Public",
        ),
        (
            "Charlie",
            "Green",
            "cgreen",
            "charlie.green@example.com",
            "5678901234",
            "password5",
            "Professional",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO User (given_name, first_name, username, email, phone_number, password, register_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        users,
    )
    conn.commit()


# Insert sample data into Patient_Info table
def populate_patient_info():
    patient_info = [
        (
            1,
            "Diabetes",
            "Medication",
            "Daily insulin injections",
            2.5,
            "Patient shows improvement",
        ),
        (
            2,
            "Hypertension",
            "Medication",
            "Daily blood pressure monitoring",
            1.8,
            "Blood pressure under control",
        ),
        (3, "Asthma", "Inhaler", "Inhaler usage twice a day", 2.0, "Condition stable"),
        (
            4,
            "Osteoporosis",
            "Treatment",
            "Weekly calcium supplements",
            1.2,
            "Bone density stable",
        ),
        (
            5,
            "Chronic Pain",
            "Physical Therapy",
            "Weekly sessions",
            2.3,
            "Pain management effective",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO Patient_Info (userID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        patient_info,
    )
    conn.commit()


# Insert sample data into Medication table
def populate_medication():
    medications = [
        (
            "Insulin",
            "Injection",
            1,
            None,
            "2024-01-01",
            "Diabetes treatment",
            "Low blood sugar",
        ),
        (
            "Lisinopril",
            "Tablet",
            2,
            None,
            "2024-02-01",
            "Blood pressure treatment",
            "Dizziness",
        ),
        (
            "Albuterol",
            "Inhaler",
            3,
            None,
            "2024-03-01",
            "Asthma treatment",
            "Throat irritation",
        ),
        (
            "Calcium",
            "Supplement",
            4,
            None,
            "2024-04-01",
            "Bone density treatment",
            "Nausea",
        ),
        ("Ibuprofen", "Tablet", 5, None, "2024-05-01", "Pain relief", "Stomach upset"),
    ]
    cursor.executemany(
        """
        INSERT INTO Medication (medication_name, medication_type, userID, file_path, date_medication_prescribed, medication_treatment_used, side_effect)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        medications,
    )
    conn.commit()


# Insert sample data into Image table
def populate_images():
    images = [
        (1, "/path/to/image1.jpg", "2024-01-15"),
        (2, "/path/to/image2.jpg", "2024-02-15"),
        (3, "/path/to/image3.jpg", "2024-03-15"),
        (4, "/path/to/image4.jpg", "2024-04-15"),
        (5, "/path/to/image5.jpg", "2024-05-15"),
    ]
    cursor.executemany(
        """
        INSERT INTO Image (userID, file_path, date_uploaded)
        VALUES (?, ?, ?)
    """,
        images,
    )
    conn.commit()


# Insert sample data into Appointment table
def populate_appointments():
    appointments = [
        (
            1,
            "Medication",
            "Checkup",
            "2024-06-01",
            "10:00",
            "2024-05-15",
            "09:00",
            "2024-06-02",
            "11:00",
        ),
        (
            2,
            "Medication",
            "Follow-up",
            "2024-07-01",
            "11:00",
            "2024-06-15",
            "10:00",
            "2024-07-02",
            "12:00",
        ),
        (
            3,
            "Inhaler",
            "Checkup",
            "2024-08-01",
            "12:00",
            "2024-07-15",
            "11:00",
            "2024-08-02",
            "13:00",
        ),
        (
            4,
            "Treatment",
            "Consultation",
            "2024-09-01",
            "13:00",
            "2024-08-15",
            "12:00",
            "2024-09-02",
            "14:00",
        ),
        (
            5,
            "Physical Therapy",
            "Follow-up",
            "2024-10-01",
            "14:00",
            "2024-09-15",
            "13:00",
            "2024-10-02",
            "15:00",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO Appointment (userID, treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        appointments,
    )
    conn.commit()


def populate_all():
    populate_users()
    populate_patient_info()
    populate_medication()
    populate_images()
    populate_appointments()
    print("Data population complete.")


if __name__ == "__main__":
    populate_all()

# Close the connection
conn.close()
