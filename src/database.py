import sqlite3

# Create Tables
def create_tables():
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    # Create User Table
    cursor.execute('''
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
    ''')

    # Create Image Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Image (
            imageID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            file_path TEXT,
            date_uploaded DATE,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    ''')

    # Create Medication Table (Updated)
    cursor.execute('''
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
    ''')

    # Create Patient Info Table (Updated)
    cursor.execute('''
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
    ''')

    # Create Appointment Table (Updated)
    cursor.execute('''
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
    ''')

    # Create Medical Profession Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Medical_Profession (
            professionID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            given_name TEXT,
            first_name TEXT,
            role TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

# Insert Functions

# Insert data into User Table
def insert_user(given_name, first_name, username, email, phone_number, password, register_type):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO User (given_name, first_name, username, email, phone_number, password, register_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (given_name, first_name, username, email, phone_number, password, register_type))

    conn.commit()
    conn.close()

# Insert data into the Image Table
def insert_image(userID, file_path, date_uploaded):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Image (userID, file_path, date_uploaded)
        VALUES (?, ?, ?)
    ''', (userID, file_path, date_uploaded))

    conn.commit()
    conn.close()

# Insert data into the Medication Table (Updated)
def insert_medication(medication_name, medication_type, userID, file_path, date_medication_prescribed, medication_treatment_used, side_effect):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Medication (medication_name, medication_type, userID, file_path, date_medication_prescribed, medication_treatment_used, side_effect)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (medication_name, medication_type, userID, file_path, date_medication_prescribed, medication_treatment_used, side_effect))

    conn.commit()
    conn.close()

# Insert data into the Patient Info Table (Updated)
def insert_patient_info(userID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Patient_Info (userID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (userID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note))

    conn.commit()
    conn.close()

# Insert data into the Appointment Table (Updated)
def insert_appointment(userID, treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Appointment (userID, treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (userID, treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time))

    conn.commit()
    conn.close()

# Insert data into the Medical Profession Table
def insert_medical_profession(userID, given_name, first_name, role):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Medical_Profession (userID, given_name, first_name, role)
        VALUES (?, ?, ?, ?)
    ''', (userID, given_name, first_name, role))

    conn.commit()
    conn.close()


# Update Functions

# Update data in the Medication Table (Updated)
def update_medication(medicationID, medication_name, medication_type, file_path, date_medication_prescribed, medication_treatment_used, side_effect):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Medication
        SET medication_name = ?, medication_type = ?, file_path = ?, date_medication_prescribed = ?, medication_treatment_used = ?, side_effect = ?
        WHERE medicationID = ?
    ''', (medication_name, medication_type, file_path, date_medication_prescribed, medication_treatment_used, side_effect, medicationID))

    conn.commit()
    conn.close()

# Update data in the Patient Info Table (Updated)
def update_patient_info(patientID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Patient_Info
        SET diagnosis = ?, treatment_type = ?, treatment_description = ?, bone_mass_density = ?, progress_note = ?
        WHERE patientID = ?
    ''', (diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note, patientID))

    conn.commit()
    conn.close()

# Update data in the Appointment Table (Updated)
def update_appointment(appointmentID, treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Appointment
        SET treatment_type = ?, appointment_type = ?, appointment_date = ?, appointment_time = ?, preop_date = ?, preop_time = ?, postop_date = ?, postop_time = ?
        WHERE appointmentID = ?
    ''', (treatment_type, appointment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time, appointmentID))

    conn.commit()
    conn.close()

# Delete Functions

# Delete data from the Medication Table (Updated)
def delete_medication(medicationID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Medication WHERE medicationID = ?', (medicationID,))

    conn.commit()
    conn.close()

# Delete data from the Patient Info Table (Updated)
def delete_patient_info(patientID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Patient_Info WHERE patientID = ?', (patientID,))

    conn.commit()
    conn.close()

# Delete data from the Appointment Table (Updated)
def delete_appointment(appointmentID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Appointment WHERE appointmentID = ?', (appointmentID,))

    conn.commit()
    conn.close()

# Get Functions

# Get data from the Medication Table (Updated)
def get_medication(medicationID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Medication WHERE medicationID = ?', (medicationID,))
    medication_data = cursor.fetchone()

    conn.close()
    return medication_data

# Get data from the Patient Info Table (Updated)
def get_patient_info(patientID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Patient_Info WHERE patientID = ?', (patientID,))
    patient_info_data = cursor.fetchone()

    conn.close()
    return patient_info_data

# Get data from the Appointment Table (Updated)
def get_appointment(appointmentID):
    conn = sqlite3.connect('../databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Appointment WHERE appointmentID = ?', (appointmentID,))
    appointment_data = cursor.fetchone()

    conn.close()
    return appointment_data

create_tables()