import streamlit as st
import sqlite3


# Function to fetch patient info by patient name
def search_patient_info(patient_name):
    conn = sqlite3.connect('./databases/healthcare.db')
    cursor = conn.cursor()

    query = '''
        SELECT * FROM Patient_Info
        JOIN User ON Patient_Info.userID = User.userID
        WHERE User.given_name LIKE ? OR User.first_name LIKE ?
    '''
    cursor.execute(query, ('%' + patient_name + '%', '%' + patient_name + '%'))
    data = cursor.fetchall()

    conn.close()
    return data


# Function to fetch medication info by patient name
def search_medication_info(patient_name):
    conn = sqlite3.connect('./databases/healthcare.db')
    cursor = conn.cursor()

    query = '''
        SELECT * FROM Medication
        JOIN User ON Medication.userID = User.userID
        WHERE User.given_name LIKE ? OR User.first_name LIKE ?
    '''
    cursor.execute(query, ('%' + patient_name + '%', '%' + patient_name + '%'))
    data = cursor.fetchall()

    conn.close()
    return data


# Function to fetch images by patient name
def search_images(patient_name):
    conn = sqlite3.connect('./databases/healthcare.db')
    cursor = conn.cursor()

    query = '''
        SELECT * FROM Image
        JOIN User ON Image.userID = User.userID
        WHERE User.given_name LIKE ? OR User.first_name LIKE ?
    '''
    cursor.execute(query, ('%' + patient_name + '%', '%' + patient_name + '%'))
    data = cursor.fetchall()

    conn.close()
    return data


# Function to fetch appointments by patient name
def search_appointments(patient_name):
    conn = sqlite3.connect('./databases/healthcare.db')
    cursor = conn.cursor()

    query = '''
        SELECT * FROM Appointment
        JOIN User ON Appointment.userID = User.userID
        WHERE User.given_name LIKE ? OR User.first_name LIKE ?
    '''
    cursor.execute(query, ('%' + patient_name + '%', '%' + patient_name + '%'))
    data = cursor.fetchall()

    conn.close()
    return data


# Professional dashboard
def professional_dashboard():
    st.title("Professional Dashboard")
    st.write(
        "Welcome! You can access professional healthcare resources, including patient information, medication, and more.")

    # Sidebar search input
    st.sidebar.title("Navigation")
    search_query = st.sidebar.text_input("Search by patient name", "")

    # Sidebar for selection
    choice = st.sidebar.radio("Choose an option:", ("Patient Info", "Medication", "Images", "Appointments"))

    if search_query:
        if choice == "Patient Info":
            st.subheader("Patient Information")
            patient_info = search_patient_info(search_query)
            if patient_info:
                st.table(patient_info)
            else:
                st.write("No patient information found for the specified name.")

        elif choice == "Medication":
            st.subheader("Medication Information")
            medication_info = search_medication_info(search_query)
            if medication_info:
                st.table(medication_info)
            else:
                st.write("No medication information found for the specified name.")

        elif choice == "Images":
            st.subheader("Patient Images")
            images = search_images(search_query)
            if images:
                for img in images:
                    st.image(img[2], caption=f"Uploaded on {img[3]}")
            else:
                st.write("No images found for the specified name.")

        elif choice == "Appointments":
            st.subheader("Appointments")
            appointments = search_appointments(search_query)
            if appointments:
                st.table(appointments)
            else:
                st.write("No appointments found for the specified name.")
    else:
        st.write("Please enter a patient's name to search.")

