import streamlit as st
import sqlite3
import pandas as pd
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_id = os.getenv("TELEGRAM_CHAT_ID")

# Telegram token and chat ID
TELEGRAM_BOT_TOKEN = telegram_bot_token
TELEGRAM_CHAT_ID = telegram_id

DATABASE_URL = "./databases/healthcare.db"


def send_telegram_message(chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        response = requests.post(url, data=payload)

        if response.status_code != 200:
            st.error(
                f"Failed to send message: {response.json().get('description', 'Unknown error')}"
            )
            return False
        return True
    except Exception as e:
        st.error(f"Error sending message: {e}")
        return False


def get_upcoming_appointments(days_before):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        target_date = (datetime.now() + timedelta(days=days_before)).strftime(
            "%Y-%m-%d"
        )

        query = """
            SELECT User.given_name, User.first_name, User.phone_number, 
                   Appointment.treatment_type, Appointment.appointment_date, Appointment.appointment_time, Appointment.appointmentID
            FROM Appointment
            JOIN User ON Appointment.userID = User.userID
            WHERE Appointment.appointment_date = ?
        """
        cursor.execute(query, (target_date,))
        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=[
                "Given Name",
                "First Name",
                "Phone Number",
                "Treatment Type",
                "Appointment Date",
                "Appointment Time",
                "Appointment ID",
            ],
        )
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching appointments: {e}")
        return pd.DataFrame()


def send_reminders(appointments_df, reminder_days):
    for _, row in appointments_df.iterrows():
        appointment_date = row["Appointment Date"]
        appointment_time = row["Appointment Time"]

        message = (
            f"Reminder: Dear {row['Given Name']} {row['First Name']}, "
            f"your {row['Treatment Type']} appointment is on {appointment_date} "
            f"at {appointment_time}."
        )

        if not send_telegram_message(TELEGRAM_CHAT_ID, message):
            st.error(
                f"Failed to send reminder to {row['Given Name']} {row['First Name']}."
            )
        else:
            st.success(f"Reminder sent to {row['Given Name']} {row['First Name']}.")


def search_patient_info(patient_name):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
            SELECT User.given_name, User.first_name, diagnosis, treatment_type, treatment_description, 
                   bone_mass_density, progress_note
            FROM Patient_Info
            JOIN User ON Patient_Info.userID = User.userID
            WHERE User.given_name LIKE ? OR User.first_name LIKE ?
        """
        cursor.execute(query, ("%" + patient_name + "%", "%" + patient_name + "%"))
        data = cursor.fetchall()

        if len(data) == 0:
            st.warning("No patient found with the given name.")

        df = pd.DataFrame(
            data,
            columns=[
                "Given Name",
                "First Name",
                "Diagnosis",
                "Treatment Type",
                "Treatment Description",
                "Bone Mass Density",
                "Progress Note",
            ],
        )
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()


def search_medication_info(patient_name):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
            SELECT Medication.medicationID, User.given_name, User.first_name, medication_name, medication_type, 
                   date_medication_prescribed, medication_treatment_used, side_effect
            FROM Medication
            JOIN User ON Medication.userID = User.userID
            WHERE User.given_name LIKE ? OR User.first_name LIKE ?
        """
        cursor.execute(query, ("%" + patient_name + "%", "%" + patient_name + "%"))
        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=[
                "Medication ID",
                "Given Name",
                "First Name",
                "Medication Name",
                "Medication Type",
                "Date Prescribed",
                "Treatment Used",
                "Side Effect",
            ],
        )
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()


def search_appointments(patient_name):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
            SELECT Appointment.appointmentID, User.given_name, User.first_name, treatment_type, appointment_type, 
                   appointment_date, appointment_time
            FROM Appointment
            JOIN User ON Appointment.userID = User.userID
            WHERE User.given_name LIKE ? OR User.first_name LIKE ?
        """
        cursor.execute(query, ("%" + patient_name + "%", "%" + patient_name + "%"))
        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=[
                "Appointment ID",
                "Given Name",
                "First Name",
                "Treatment Type",
                "Appointment Type",
                "Appointment Date",
                "Appointment Time",
            ],
        )
        conn.close()
        return df
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()


def delete_medication(medication_id):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Medication WHERE medicationID = ?", (medication_id,)
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Failed to delete medication: {e}")
    except Exception as e:
        st.error(f"Error occurred while deleting medication: {e}")


def delete_appointment(appointment_id):
    try:
        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Appointment WHERE appointmentID = ?", (appointment_id,)
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Failed to delete appointment: {e}")
    except Exception as e:
        st.error(f"Error occurred while deleting appointment: {e}")


def update_medication(
    medication_id,
    medication_name,
    medication_type,
    date_prescribed,
    treatment_used,
    side_effect,
):
    try:
        if medication_name.strip() == "" or medication_type.strip() == "":
            st.error("Medication name and type cannot be empty.")
            return

        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Medication
            SET medication_name = ?, medication_type = ?, date_medication_prescribed = ?, 
                medication_treatment_used = ?, side_effect = ?
            WHERE medicationID = ?
        """,
            (
                medication_name,
                medication_type,
                date_prescribed,
                treatment_used,
                side_effect,
                medication_id,
            ),
        )

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Failed to update medication: {e}")
    except Exception as e:
        st.error(f"Error occurred while updating medication: {e}")


def update_appointment(
    appointment_id, appointment_date, appointment_time, treatment_type, appointment_type
):
    try:
        if treatment_type.strip() == "" or appointment_type.strip() == "":
            st.error("Treatment type and appointment type cannot be empty.")
            return

        # Convert date and time to the correct formats
        appointment_date_str = appointment_date.strftime(
            "%Y-%m-%d"
        )  # Convert date to YYYY-MM-DD format
        appointment_time_str = appointment_time.strftime(
            "%H:%M:%S"
        )  # Convert time to HH:MM:SS format

        conn = sqlite3.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Appointment
            SET appointment_date = ?, appointment_time = ?, treatment_type = ?, appointment_type = ?
            WHERE appointmentID = ?
        """,
            (
                appointment_date_str,
                appointment_time_str,
                treatment_type,
                appointment_type,
                appointment_id,
            ),
        )

        conn.commit()
        conn.close()
        st.success(f"Appointment {appointment_id} updated successfully!")
    except sqlite3.Error as e:
        st.error(f"Failed to update appointment: {e}")
    except Exception as e:
        st.error(f"Error occurred while updating appointment: {e}")


def professional_dashboard():
    try:
        st.title("Professional Dashboard")
        st.write("Welcome! Access detailed patient healthcare records here.")

        # Sidebar for search input
        st.sidebar.title("Search and Navigation")
        search_query = st.sidebar.text_input("Search by patient name")

        choice = st.sidebar.radio(
            "Select Information Type:",
            ("Patient Info", "Medication", "Images", "Appointments"),
        )

        # Send reminder for upcoming appointments (1 or 3 days)
        reminder_days = st.sidebar.radio(
            "Send reminder for upcoming appointments in:", (3, 1)
        )
        if st.sidebar.button(
            f"Send Reminder for Appointments in {reminder_days} Day(s)"
        ):
            appointments_df = get_upcoming_appointments(reminder_days)
            if not appointments_df.empty:
                st.write(
                    f"Sending reminders for appointments in the next {reminder_days} day(s):"
                )
                st.table(appointments_df)

                # Send reminders
                send_reminders(appointments_df, reminder_days)
            else:
                st.warning("No appointments in the next days to send reminders.")

        if search_query:
            if choice == "Patient Info":
                df = search_patient_info(search_query)
                st.subheader("Patient Information")
            elif choice == "Medication":
                df = search_medication_info(search_query)
                st.subheader("Medication Details")

                if not df.empty:
                    st.table(df)

                    # Update medication
                    medication_id = st.selectbox(
                        "Select Medication ID to Update", df["Medication ID"].unique()
                    )
                    selected_row = df[df["Medication ID"] == medication_id].iloc[0]

                    medication_name = st.text_input(
                        "Medication Name", value=selected_row["Medication Name"]
                    )
                    medication_type = st.text_input(
                        "Medication Type", value=selected_row["Medication Type"]
                    )
                    date_prescribed = st.date_input(
                        "Date Prescribed",
                        value=pd.to_datetime(selected_row["Date Prescribed"]),
                    )
                    treatment_used = st.text_input(
                        "Treatment Used", value=selected_row["Treatment Used"]
                    )
                    side_effect = st.text_input(
                        "Side Effect", value=selected_row["Side Effect"]
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update Medication"):
                            update_medication(
                                medication_id,
                                medication_name,
                                medication_type,
                                date_prescribed,
                                treatment_used,
                                side_effect,
                            )
                            st.success(
                                f"Medication {medication_id} updated successfully!"
                            )
                    with col2:
                        if st.button("Delete Medication"):
                            delete_medication(medication_id)
                            st.success(
                                f"Medication {medication_id} deleted successfully!"
                            )
                else:
                    st.warning("No medications found for the specified name.")

            elif choice == "Appointments":
                df = search_appointments(search_query)
                st.subheader("Appointments Details")

                if not df.empty:
                    st.table(df)

                    # Update appointment
                    appointment_id = st.selectbox(
                        "Select Appointment ID to Update", df["Appointment ID"].unique()
                    )
                    selected_row = df[df["Appointment ID"] == appointment_id].iloc[0]

                    appointment_date = st.date_input(
                        "Appointment Date",
                        value=pd.to_datetime(selected_row["Appointment Date"]),
                    )
                    appointment_time = st.time_input(
                        "Appointment Time",
                        value=pd.to_datetime(selected_row["Appointment Time"]).time(),
                    )
                    treatment_type = st.text_input(
                        "Treatment Type", value=selected_row["Treatment Type"]
                    )
                    appointment_type = st.text_input(
                        "Appointment Type", value=selected_row["Appointment Type"]
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Update Appointment"):
                            update_appointment(
                                appointment_id,
                                appointment_date,
                                appointment_time,
                                treatment_type,
                                appointment_type,
                            )
                            st.success(
                                f"Appointment {appointment_id} updated successfully!"
                            )
                    with col2:
                        if st.button("Delete Appointment"):
                            delete_appointment(appointment_id)
                            st.success(
                                f"Appointment {appointment_id} deleted successfully!"
                            )
                else:
                    st.warning("No appointments found for the specified name.")
        else:
            st.write("Please enter a name to begin the search.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    professional_dashboard()
