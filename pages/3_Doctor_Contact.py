import streamlit as st
from database import get_doctors, add_message, get_messages

st.title("Contact a Doctor")

if 'current_user' not in st.session_state:
    st.warning("Please login to contact doctors")
else:
    user_id = st.session_state.current_user['id']
    doctors = get_doctors()
    
    if not doctors:
        st.error("No doctors available")
    else:
        doctor_names = [f"{doc[1]} ({doc[2]})" for doc in doctors]
        selected_doctor = st.selectbox("Select a doctor", options=doctor_names)
        
        if selected_doctor:
            doctor_index = doctor_names.index(selected_doctor)
            doctor_id = doctors[doctor_index][0]
            doctor_info = doctors[doctor_index]
            
            st.subheader(f"Contact {doctor_info[1]}")
            st.write(f"**Specialty:** {doctor_info[2]}")
            st.write(f"**Availability:** {doctor_info[4]}")
            st.write(f"**Contact:** {doctor_info[3]}")
            st.write(f"**Bio:** {doctor_info[5]}")
            
            st.divider()
            
            # Message history
            st.subheader("Message History")
            messages = get_messages(user_id, doctor_id)
            
            if messages:
                for msg in messages:
                    role = "Doctor" if msg[4] else "You"
                    st.write(f"**{role}** ({msg[3]}): {msg[2]}")
            else:
                st.info("No messages yet with this doctor")
            
            # New message
            st.subheader("Send New Message")
            new_message = st.text_area("Your message")
            if st.button("Send Message"):
                if new_message:
                    add_message(user_id, doctor_id, new_message, False)
                    st.success("Message sent!")
                    st.rerun()
                else:
                    st.warning("Please enter a message")
