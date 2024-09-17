import sqlite3


def create_tables():
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Medication (
            medicationID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            file_path TEXT,
            date_medication_prescribed DATE,
            medication_treatment_used TEXT,
            side_effect TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Patient_Info (
            userID INTEGER PRIMARY KEY,
            diagnosis TEXT,
            treatment_type TEXT,
            treatment_description TEXT,
            bone_mass_density REAL,
            progress_note TEXT,
            FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Appointment (
            userID INTEGER PRIMARY KEY,
            treatment_type TEXT,
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
    print("Tables created")


def insert_user(
    given_name, first_name, username, email, phone_number, password, register_type
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO User (given_name, first_name, username, email, phone_number, password, register_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            given_name,
            first_name,
            username,
            email,
            phone_number,
            password,
            register_type,
        ),
    )

    conn.commit()
    conn.close()
    print("User data inserted")


def update_user(userID, given_name, first_name, email, phone_number, password):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE User
        SET given_name = ?, first_name = ?, email = ?, phone_number = ?, password = ?
        WHERE userID = ?
    """,
        (given_name, first_name, email, phone_number, password, userID),
    )

    conn.commit()
    conn.close()
    print("User data updated")


def delete_user(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM User WHERE userID = ?", (userID,))

    conn.commit()
    conn.close()
    print(f"User with ID {userID} deleted")


def get_user(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM User WHERE userID = ?", (userID,))
    user_data = cursor.fetchone()

    conn.close()
    return user_data


def insert_image(userID, file_path, date_uploaded):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Image (userID, file_path, date_uploaded)
        VALUES (?, ?, ?)
    """,
        (userID, file_path, date_uploaded),
    )

    conn.commit()
    conn.close()
    print("Image data inserted")


def update_image(imageID, file_path, date_uploaded):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Image
        SET file_path = ?, date_uploaded = ?
        WHERE imageID = ?
    """,
        (file_path, date_uploaded, imageID),
    )

    conn.commit()
    conn.close()
    print(f"Image with ID {imageID} updated")


def delete_image(imageID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Image WHERE imageID = ?", (imageID,))

    conn.commit()
    conn.close()
    print(f"Image with ID {imageID} deleted")


def get_image(imageID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Image WHERE imageID = ?", (imageID,))
    image_data = cursor.fetchone()

    conn.close()
    return image_data


def insert_medication(
    userID,
    file_path,
    date_medication_prescribed,
    medication_treatment_used,
    side_effect,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Medication (userID, file_path, date_medication_prescribed, medication_treatment_used, side_effect)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            userID,
            file_path,
            date_medication_prescribed,
            medication_treatment_used,
            side_effect,
        ),
    )

    conn.commit()
    conn.close()
    print("Medication data inserted")


def update_medication(
    medicationID,
    file_path,
    date_medication_prescribed,
    medication_treatment_used,
    side_effect,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Medication
        SET file_path = ?, date_medication_prescribed = ?, medication_treatment_used = ?, side_effect = ?
        WHERE medicationID = ?
    """,
        (
            file_path,
            date_medication_prescribed,
            medication_treatment_used,
            side_effect,
            medicationID,
        ),
    )

    conn.commit()
    conn.close()
    print(f"Medication with ID {medicationID} updated")


# Function to delete data from the Medication table
def delete_medication(medicationID):
    conn = sqlite3.connect("./databases//healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Medication WHERE medicationID = ?", (medicationID,))

    conn.commit()
    conn.close()
    print(f"Medication with ID {medicationID} deleted")


def get_medication(medicationID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Medication WHERE medicationID = ?", (medicationID,))
    medication_data = cursor.fetchone()

    conn.close()
    return medication_data


def insert_patient_info(
    userID,
    diagnosis,
    treatment_type,
    treatment_description,
    bone_mass_density,
    progress_note,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Patient_Info (userID, diagnosis, treatment_type, treatment_description, bone_mass_density, progress_note)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            userID,
            diagnosis,
            treatment_type,
            treatment_description,
            bone_mass_density,
            progress_note,
        ),
    )

    conn.commit()
    conn.close()
    print("Patient info data inserted")


def update_patient_info(
    userID,
    diagnosis,
    treatment_type,
    treatment_description,
    bone_mass_density,
    progress_note,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Patient_Info
        SET diagnosis = ?, treatment_type = ?, treatment_description = ?, bone_mass_density = ?, progress_note = ?
        WHERE userID = ?
    """,
        (
            diagnosis,
            treatment_type,
            treatment_description,
            bone_mass_density,
            progress_note,
            userID,
        ),
    )

    conn.commit()
    conn.close()
    print(f"Patient info for user ID {userID} updated")


def delete_patient_info(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Patient_Info WHERE userID = ?", (userID,))

    conn.commit()
    conn.close()
    print(f"Patient info for user ID {userID} deleted")


def get_patient_info(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Patient_Info WHERE userID = ?", (userID,))
    patient_info_data = cursor.fetchone()

    conn.close()
    return patient_info_data


def insert_appointment(
    userID,
    treatment_type,
    appointment_date,
    appointment_time,
    preop_date,
    preop_time,
    postop_date,
    postop_time,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Appointment (userID, treatment_type, appointment_date, appointment_time, preop_date, preop_time, postop_date, postop_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            userID,
            treatment_type,
            appointment_date,
            appointment_time,
            preop_date,
            preop_time,
            postop_date,
            postop_time,
        ),
    )

    conn.commit()
    conn.close()
    print("Appointment data inserted")


def update_appointment(
    userID,
    treatment_type,
    appointment_date,
    appointment_time,
    preop_date,
    preop_time,
    postop_date,
    postop_time,
):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Appointment
        SET treatment_type = ?, appointment_date = ?, appointment_time = ?, preop_date = ?, preop_time = ?, postop_date = ?, postop_time = ?
        WHERE userID = ?
    """,
        (
            treatment_type,
            appointment_date,
            appointment_time,
            preop_date,
            preop_time,
            postop_date,
            postop_time,
            userID,
        ),
    )

    conn.commit()
    conn.close()
    print(f"Appointment for user ID {userID} updated")


def delete_appointment(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Appointment WHERE userID = ?", (userID,))

    conn.commit()
    conn.close()
    print(f"Appointment for user ID {userID} deleted")


def get_appointment(userID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Appointment WHERE userID = ?", (userID,))
    appointment_data = cursor.fetchone()

    conn.close()
    return appointment_data


def insert_medical_profession(userID, given_name, first_name, role):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Medical_Profession (userID, given_name, first_name, role)
        VALUES (?, ?, ?, ?)
    """,
        (userID, given_name, first_name, role),
    )

    conn.commit()
    conn.close()
    print("Medical profession data inserted")


def update_medical_profession(professionID, given_name, first_name, role):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Medical_Profession
        SET given_name = ?, first_name = ?, role = ?
        WHERE professionID = ?
    """,
        (given_name, first_name, role, professionID),
    )

    conn.commit()
    conn.close()
    print(f"Medical profession with ID {professionID} updated")


def delete_medical_profession(professionID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Medical_Profession WHERE professionID = ?", (professionID,)
    )

    conn.commit()
    conn.close()
    print(f"Medical profession with ID {professionID} deleted")


def get_medical_profession(professionID):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Medical_Profession WHERE professionID = ?", (professionID,)
    )
    profession_data = cursor.fetchone()

    conn.close()
    return profession_data


create_tables()
