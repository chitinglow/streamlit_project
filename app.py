import streamlit as st
import sqlite3

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None
    st.session_state["username"] = None  # Store the username for greetings


conn = sqlite3.connect("./databases/users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        userID TEXT PRIMARY KEY,
        given_name TEXT,
        first_name TEXT,
        email TEXT,
        username TEXT,
        password TEXT,
        role TEXT
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS images (
        imageID TEXT PRIMARY KEY,
        userID TEXT FOREIGN KEY,
        date_upload DATE,
        image_path TEXT,
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS medication (
    medicationID TEXT PRIMARY KEY,
    userID TEXT FOREIGN KEY,
    image_path TEXT,
    side_effect TEXT,
    )
    """
)

conn.commit()


def create_user(username, password, role):
   cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, role),
    )
   conn.commit()


def get_user(username):
    cursor.execute(
        "SELECT username, password, role FROM users WHERE username = ?", (username,)
    )
    return cursor.fetchone()


# Registration Page
def register():
    st.title("Register")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    role = st.selectbox("Select your role", ("admin", "user"))

    if st.button("Register"):
        user = get_user(new_username)
        if user:
            st.error("Username already exists. Try another.")
        else:
            create_user(new_username, new_password, role)
            st.success(f"User {new_username} registered successfully!")


def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username)
        if user and user[1] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = user[2]
            st.session_state["username"] = username  # Store the username for future use
        else:
            st.error("Invalid username or password.")


def admin_page():
    st.title("Admin Page")
    st.write(f"Welcome {st.session_state['username']} to the admin dashboard!")


def user_page():
    st.title("User Page")
    st.write(f"Welcome {st.session_state['username']} to the user dashboard!")


def main():
    if st.session_state["logged_in"]:
        if st.session_state["role"] == "admin":
            admin_page()
        elif st.session_state["role"] == "user":
            user_page()
    else:
        st.sidebar.title("Menu")
        option = st.sidebar.radio("Choose an option", ["Login", "Register"])
        if option == "Login":
            login()
        elif option == "Register":
            register()


if __name__ == "__main__":
    main()
