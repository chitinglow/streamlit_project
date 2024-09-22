import streamlit as st
from src.registration import user_registration, member_page, professional_page
from src.dashboard import professional_dashboard
import sqlite3

# Initialize session state for page and login status
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # User login status

if "user_role" not in st.session_state:
    st.session_state.user_role = None  # Track user's role


# Function to check the role of the user after registration or login
def check_user_role(username):
    conn = sqlite3.connect('./databases/healthcare.db')
    cursor = conn.cursor()

    cursor.execute('SELECT register_type FROM User WHERE username = ?', (username,))
    user_role = cursor.fetchone()

    conn.close()
    return user_role[0] if user_role else None


# Function to set page and simulate redirection
def set_page(page):
    st.session_state.page = page  # Update session state page


# Function to log out the user
def logout():
    st.session_state.logged_in = False
    st.session_state.page = "home"  # Redirect to home page
    st.session_state.user_role = None  # Clear the user role


# Function to show logout button in the top-right corner using columns
def show_logout_button():
    # Create columns with custom width to position the logout button in the top-right corner
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

            # Create columns layout to position buttons on the top-right
            col1, col2, col3 = st.columns([6, 1, 3])

            # Place Login and Register buttons in the top-right column (col3)
            with col3:
                option = st.radio("", ["Login", "Register"], horizontal=True)  # Login first, Register second

            # Display the home page content by default
            st.subheader("Welcome to Healthcare App")
            st.text("Please select 'Login' or 'Register' from the top-right options to continue.")

            # Handle the selected option
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
                            set_page("member")
                    else:
                        st.error("Invalid username or password.")

            elif option == "Register":
                user_registration()  # Call the registration page

    if st.session_state.logged_in:
        # Show the appropriate page based on the user role
        if st.session_state.user_role == "Professional":
            show_logout_button()
            professional_dashboard()
        elif st.session_state.user_role == "Member of Public":
            show_logout_button()
            member_page()  # Redirect to member page


if __name__ == '__main__':
    main()
