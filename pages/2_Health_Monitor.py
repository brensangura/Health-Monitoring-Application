import streamlit as st
import random
from database import get_health_data, add_health_data

st.title("Health Monitor")

HEALTH_TIPS = [
    "Drink at least 8 glasses of water daily.",
    "Aim for 7-9 hours of sleep each night.",
    "Take a 5-minute break every hour if you sit for long periods.",
    "Wash your hands regularly to prevent infections.",
    "Include fruits and vegetables in every meal."
]

SYMPTOM_DATABASE = {
    'headache': {
        'possible_causes': ['tension', 'migraine', 'dehydration', 'eye strain'],
        'recommendations': ['drink water', 'rest', 'take pain reliever if needed']
    },
    'fever': {
        'possible_causes': ['infection', 'flu', 'cold'],
        'recommendations': ['rest', 'stay hydrated', 'take fever reducer']
    }
}

tab1, tab2 = st.tabs(["AI Health Assistant", "Symptom Checker"])

with tab1:
    st.subheader("Chat with our AI Health Assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your health assistant. How can I help you today?"}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about symptoms or health tips"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simple AI response logic
        response = ""
        if any(word in prompt.lower() for word in ['symptom', 'pain', 'hurt']):
            response = "I can help check symptoms. Please tell me your main symptom (e.g., headache, fever)."
        elif any(symptom in prompt.lower() for symptom in SYMPTOM_DATABASE.keys()):
            for symptom, info in SYMPTOM_DATABASE.items():
                if symptom in prompt.lower():
                    causes = ', '.join(info['possible_causes'])
                    recs = ', '.join(info['recommendations'])
                    response = f"Possible causes: {causes}. Recommendations: {recs}. If symptoms persist, consult a doctor."
                    break
        elif any(word in prompt.lower() for word in ['tip', 'advice']):
            response = random.choice(HEALTH_TIPS)
        else:
            response = "I'm here to help with health questions. You can ask about symptoms or request a health tip."
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("Symptom Checker")
    symptoms = st.text_area("Describe your symptoms in detail")
    if st.button("Analyze Symptoms"):
        if symptoms:
            # Basic symptom analysis
            found_symptoms = []
            for symptom in SYMPTOM_DATABASE:
                if symptom in symptoms.lower():
                    found_symptoms.append(symptom)
            
            if found_symptoms:
                st.success("Analysis Complete")
                for symptom in found_symptoms:
                    info = SYMPTOM_DATABASE[symptom]
                    st.subheader(symptom.capitalize())
                    st.write("Possible causes:", ", ".join(info['possible_causes']))
                    st.write("Recommendations:", ", ".join(info['recommendations']))
            else:
                st.info("No specific symptoms identified. For general advice: rest, stay hydrated, and monitor your symptoms.")
        else:
            st.warning("Please describe your symptoms")
