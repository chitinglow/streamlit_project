import streamlit as st
import sqlite3

# insert data into database
def insert_user(given_name, first_name, username, email, phone_number, password, register_type):
    conn = sqlite3.connect('./databases/healthcare.db')  # Ensure correct path
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO User (given_name, first_name, username, email, phone_number, password, register_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (given_name, first_name, username, email, phone_number, password, register_type))

    conn.commit()
    conn.close()


# Registration form
def user_registration():
    st.title("User Registration")

    # Input fields for the registration form
    given_name = st.text_input("Given Name")
    first_name = st.text_input("First Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    register_type = st.selectbox("Register as:", ["Professional", "Member of Public"])

    if st.button("Register"):
        if given_name and first_name and username and email and password:
            # Insert the user data into the database
            try:
                insert_user(given_name, first_name, username, email, phone_number, password, register_type)
                st.success(f"Account created successfully as {register_type}!")
            except sqlite3.IntegrityError:
                st.error("Username or email already exists. Please try again.")
        else:
            st.warning("Please fill out all required fields.")

    st.text("Already have an account? Go to Login page from the sidebar.")


# Page for different role access
def member_page():
    st.title("Member of Public Dashboard")
    st.write("Welcome! You can access general healthcare resources.")


def professional_page():
    st.title("🧑‍⚕️ Professional Dashboard")
    st.write("Welcome! You can access professional healthcare resources.")
