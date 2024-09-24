import streamlit as st
from src.registration import user_registration
from src.dashboard import professional_dashboard
from src.image import ocr_page
import sqlite3
from PIL import Image
import base64

# Function to encode the image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the image to base64
image_path = "MISSY Bot.png"  # Adjust this path if the image is in a different location
base64_image = get_base64_image(image_path)

# Customizing the background image with base64 encoding
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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
    # Add high contrast toggle and font size slider
    st.sidebar.title("Accessibility Settings")
    high_contrast = st.sidebar.checkbox("High Contrast Mode")
    font_size = st.sidebar.slider("Font Size", 12, 32, 16)

    # Apply styles based on high contrast mode
    if high_contrast:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #000;
                color: #FFF;
            }
            .stButton>button {
                background-color: #FFF;
                color: #000;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    # Apply font size dynamically
    st.markdown(
        f"""
        <style>
        .stApp * {{
            font-size: {font_size}px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



    # Check session state for current page
    page = st.session_state.page

    if not st.session_state.logged_in:
        if page == "home":
            st.title("MISSY BOT")
            st.markdown("### Your Personalised AI Breast Care Nurse")

            col1, col2, col3 = st.columns([6, 1, 1])

            # Adding radio buttons for Login and Register in col3
            with col1:
                option = st.radio("", ["Login", "Register"], horizontal=True)


            #st.subheader("Welcome to Missy AI App")
            st.text("Please select 'Login' or 'Register' from the options to continue.")

            if option == "Login":
                st.subheader("Login Page")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                # Creating columns for login button and Singpass button
                col_login, col_singpass = st.columns([1, 1])

                # Display Login button
                with col_login:
                    if st.button("Login"):
                        user_role = check_user_role(username)
                        if user_role:
                            st.success(f"Logged in as {user_role}")
                            st.session_state.logged_in = True
                            st.session_state.user_role = user_role
                            if user_role == "Doctor/Nurse":
                                set_page("professional")
                            elif user_role == "Patient":
                                set_page("ocr_only")
                            elif user_role == "Admin":
                                set_page("admin")
                        else:
                            st.error("Invalid username or password.")
                # Custom CSS to style the "Login with Singpass" button
                m = st.markdown("""
                                <style>
                                div.stButton > button:first-child {
                                    background-color: red;
                                }
                                </style>""", unsafe_allow_html=True)
            
                # Display "Login with Singpass" button with custom styling
                with col_singpass:
                    if st.button("Login with Singpass", key="singpass"):
                        # Add the functionality for Singpass login here
                        st.success("Login with Singpass is currently not implemented.")



            # go to registration page
            elif option == "Register":
                user_registration()

    if st.session_state.logged_in:
        if st.session_state.user_role == "Doctor/Nurse":
            show_logout_button()

            option = st.sidebar.radio("Navigation", ["Dashboard", "Medication Image Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "Medication Image Analysis":
                ocr_page()

        elif st.session_state.user_role == "Patient":
            show_logout_button()


            ocr_page()

        elif st.session_state.user_role == "Admin":
            show_logout_button()
            # Show both professional dashboard and OCR options for Admin users
            option = st.sidebar.radio("Navigation", ["Dashboard", "OCR Image Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "OCR Image Analysis":
                ocr_page()


if __name__ == "__main__":
    main()
