import streamlit as st
from database import init_db, get_user_data, add_health_data, get_doctors, add_message

# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Health Monitoring App",
    page_icon="🏥",
    layout="wide"
)

# Session state management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Main app function
def main():
    if not st.session_state.logged_in:
        show_login()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.current_user['username']}")
        st.sidebar.button("Logout", on_click=logout)
        show_main_app()

def show_login():
    st.title("Health Monitoring App")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if new_password == confirm_password:
                    if register_user(new_username, new_email, new_password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists")
                else:
                    st.error("Passwords do not match")

def show_main_app():
    st.title("Health Monitoring Dashboard")
    st.sidebar.success("Select a page above.")
    
    # Navigation would be handled by Streamlit's pages feature
    # The actual content is in the pages/ directory

def authenticate_user(username, password):
    # Implement your authentication logic
    user_data = get_user_data(username)
    if user_data and user_data['password'] == password:  # In real app, use hashing
        return user_data
    return None

def register_user(username, email, password):
    # Implement your registration logic
    existing_user = get_user_data(username)
    if existing_user:
        return False
    # Add user to database
    return True

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

if __name__ == "__main__":
    main()
