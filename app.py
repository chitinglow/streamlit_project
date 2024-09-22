import streamlit as st
from src.registration import user_registration
from src.dashboard import professional_dashboard
from src.image import ocr_page
import sqlite3

# Initialize session state for page and login status
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default at home page

if "logged_in" not in st.session_state:
    # Check user's login status
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    #  Track user's role
    st.session_state.user_role = None


# Check the role of the user after registration or login
def check_user_role(username):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()
    # get information from user table
    cursor.execute("SELECT register_type FROM User WHERE username = ?", (username,))
    user_role = cursor.fetchone()

    conn.close()
    return user_role[0] if user_role else None


def set_page(page):
    # Update session state page
    st.session_state.page = page


def logout():
    st.session_state.logged_in = False
    # direct back to home page
    st.session_state.page = "home"
    # clear user role session
    st.session_state.user_role = None


def show_logout_button():
    col1, col2, col3 = st.columns([6, 1, 1])

    with col3:
        if st.button("Logout"):
            logout()


# Main page
def main():
    # Check session state for current page
    page = st.session_state.page

    if not st.session_state.logged_in:
        if page == "home":
            st.title("Healthcare App")

            col1, col2, col3 = st.columns([6, 1, 3])

            with col3:
                option = st.radio("", ["Login", "Register"], horizontal=True)

            st.subheader("Welcome to Missy AI App")
            st.text("Please select 'Login' or 'Register' from the options to continue.")

            if option == "Login":
                st.subheader("Login Page")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.button("Login"):
                    user_role = check_user_role(username)
                    if user_role:
                        st.success(f"Logged in as {user_role}")
                        st.session_state.logged_in = True
                        st.session_state.user_role = user_role
                        if user_role == "Professional":
                            set_page("professional")
                        elif user_role == "Member of Public":
                            set_page("ocr_only")
                    else:
                        st.error("Invalid username or password.")

            # go to registration page
            elif option == "Register":
                user_registration()

    if st.session_state.logged_in:
        if st.session_state.user_role == "Professional":
            show_logout_button()

            option = st.sidebar.radio("Navigation", ["Dashboard", "OCR Image Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "OCR Image Analysis":
                ocr_page()

        elif st.session_state.user_role == "Member of Public":
            show_logout_button()

            ocr_page()


if __name__ == "__main__":
    main()
