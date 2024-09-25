import streamlit as st
from src.registration import user_registration
from src.dashboard import professional_dashboard
from src.image import ocr_page
from src.wound_care import wound_care_analysis
import sqlite3
from PIL import Image
import base64
import os
import openai


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


# Function to get OpenAI API key
def get_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found in environment variables. Please set the API key.")
    return api_key


# Function to interact with OpenAI API using the correct syntax
def ask_missy(prompt):
    try:
        api_key = get_api_key()
        if not api_key:
            return "No API key available."

        openai.api_key = api_key
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a helpful medical assistant capable of answering a wide range of medical and health-related questions. Keep your answers brief and supportive, focusing on providing clear and accurate information."},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message["content"]
    except Exception as e:
        st.write(f"Error during OpenAI API call: {str(e)}")  # Debug message
        return f"An error occurred: {str(e)}"


if "page" not in st.session_state:
    st.session_state.page = "home"  # Default at home page

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "user_query" not in st.session_state:
    st.session_state.user_query = ""

if "missy_response" not in st.session_state:
    st.session_state.missy_response = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

def check_user_credentials(username, password):
    conn = sqlite3.connect("./databases/healthcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT userID, register_type FROM User WHERE username = ? AND password = ?", (username, password))
    user_data = cursor.fetchone()
    conn.close()
    return user_data if user_data else None


def set_page(page):
    st.session_state.page = page


def logout():
    st.session_state.logged_in = False
    st.session_state.page = "home"
    st.session_state.user_role = None
    st.session_state.user_id = None  # Clear the user_id on logout


def show_logout_button():
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Logout"):
            logout()


def show_ask_missy_button():
    if st.session_state.user_role == "Patient":
        col1, col2 = st.columns([8, 2])
        with col2:
            st.markdown("## Need Help?")
            if st.button("Ask MISSY", key="ask_missy"):
                st.session_state.show_missy_form = True


def main():

    if "show_missy_form" not in st.session_state:
        st.session_state.show_missy_form = False

    if "current_navigation" not in st.session_state:
        st.session_state.current_navigation = ""

    st.sidebar.title("Accessibility Settings")
    high_contrast = st.sidebar.checkbox("High Contrast Mode")
    font_size = st.sidebar.slider("Font Size", 12, 32, 16)

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

    page = st.session_state.page

    if not st.session_state.logged_in:
        if page == "home":
            st.title("MISSY BOT")
            st.markdown("### Your Personalised AI Breast Care Nurse")

            col1, col2, col3 = st.columns([6, 1, 1])
            with col1:
                option = st.radio("Choose an option", ["Login", "Register"], horizontal=True)
            st.text("Please select 'Login' or 'Register' from the options to continue.")

            if option == "Login":
                st.subheader("Login Page")
                username = st.text_input("Username", label_visibility="hidden")
                password = st.text_input("Password", type="password", label_visibility="hidden")

                col_login, col_singpass = st.columns([1, 1])
                with col_login:
                    if st.button("Login"):
                        user_data = check_user_credentials(username, password)
                        if user_data:
                            user_id, user_role = user_data
                            st.success(f"Logged in as {user_role}")
                            st.session_state.logged_in = True
                            st.session_state.user_role = user_role
                            st.session_state.user_id = user_id  # Store user_id in session
                            if user_role == "Doctor/Nurse":
                                set_page("professional")
                            elif user_role == "Patient":
                                set_page("ocr_only")
                            elif user_role == "Admin":
                                set_page("admin")
                        else:
                            st.error("Invalid username or password.")
                with col_singpass:
                    if st.button("Login with Singpass", key="singpass"):
                        st.success("Login with Singpass is currently not implemented.")

            elif option == "Register":
                user_registration()

    if st.session_state.logged_in:
        # Show logout and "Ask MISSY" buttons at the top
        show_logout_button()
        show_ask_missy_button()

        if st.session_state.user_role == "Doctor/Nurse":
            option = st.sidebar.radio("Navigation", ["Dashboard", "Medication Image Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "Medication Image Analysis":
                ocr_page()

        elif st.session_state.user_role == "Patient":
            option = st.sidebar.radio("Navigation", ["Dashboard", "Medication Image Analysis", "Wound Care Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "Medication Image Analysis":
                ocr_page()
            elif option == "Wound Care Analysis":
                wound_care_analysis()

            # Show "Ask MISSY" form if the button was clicked
            if st.session_state.show_missy_form:
                with st.form(key="missy_form"):
                    # Store user input in session state
                    st.session_state.user_query = st.text_input(
                        "Enter your medical query or health concern:", label_visibility="hidden"
                    )
                    col_submit, col_clear, col_close = st.columns([1, 1, 1])
                    with col_submit:
                        submit_query = st.form_submit_button(label="Submit Query")
                    with col_clear:
                        clear_response = st.form_submit_button(label="Clear Response")
                    with col_close:
                        close_form = st.form_submit_button(label="Close Form")

                    if submit_query and st.session_state.user_query:
                        # Get response from OpenAI API
                        st.session_state.missy_response = ask_missy(f"Patient query: {st.session_state.user_query}")
                        st.session_state.user_query = ""  # Clear the input after submission

                    # Clear response when "Clear Response" button is clicked
                    if clear_response:
                        st.session_state.missy_response = ""
                        st.session_state.user_query = ""

                    # Close the "Ask MISSY" form when "Close Form" button is clicked
                    if close_form:
                        st.session_state.missy_response = ""
                        st.session_state.user_query = ""
                        st.session_state.show_missy_form = False

            # Display response if available
            if st.session_state.missy_response:
                st.markdown("### MISSY's Response")
                st.write(st.session_state.missy_response)

        elif st.session_state.user_role == "Admin":
            option = st.sidebar.radio("Navigation", ["Dashboard", "OCR Image Analysis"])
            if option == "Dashboard":
                professional_dashboard()
            elif option == "OCR Image Analysis":
                ocr_page()


if __name__ == "__main__":
    main()
