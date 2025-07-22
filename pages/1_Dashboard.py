import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_health_data

st.title("Health Dashboard")

if 'current_user' in st.session_state:
    user_id = st.session_state.current_user['id']
    health_data = get_health_data(user_id)
    
    if health_data:
        df = pd.DataFrame(health_data, columns=['date', 'weight', 'blood_pressure', 'heart_rate'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Weight Trend")
            fig = px.line(df, x='date', y='weight', title='Weight Over Time')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Heart Rate Trend")
            fig = px.line(df, x='date', y='heart_rate', title='Heart Rate Over Time')
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Recent Measurements")
        st.dataframe(df.sort_values('date', ascending=False).head(5))
    else:
        st.info("No health data available. Please add some measurements.")
        
    with st.expander("Add New Measurement"):
        with st.form("health_form"):
            date = st.date_input("Date")
            weight = st.number_input("Weight (kg)", min_value=0.0)
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0)
            symptoms = st.text_area("Symptoms")
            medications = st.text_input("Medications")
            
            submitted = st.form_submit_button("Save")
            if submitted:
                # Save to database
                st.success("Measurement saved!")
else:
    st.warning("Please login to view your dashboard")
