import streamlit as st
import joblib
import numpy as np

# Load saved models and scaler
@st.cache_resource
def load_artifacts():
    scaler = joblib.load("scaler.pkl")
    svc_model = joblib.load("classifier.pkl")
    logistic_model = joblib.load("model_2.pkl")
    return scaler, {"SVC Model": svc_model, "Logistic Regression": logistic_model}

scaler, models = load_artifacts()

st.title("Diabetes Prediction Web App")
st.write("Enter the required patient health metrics to evaluate diabetes risk.")

# Choose model
selected_model = st.selectbox("Select Model", list(models.keys()))
active_model = models[selected_model]

st.subheader("Patient Health Metrics")

# 2-column layout for neat UI
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
    glucose = st.number_input("Glucose Level", min_value=0.0, value=120.0)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0.0, value=70.0)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0, value=20.0)

with col2:
    insulin = st.number_input("Insulin Level (mu U/ml)", min_value=0.0, value=79.0)
    bmi = st.number_input("BMI", min_value=0.0, value=25.0)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, value=0.47, format="%.3f")
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=33, step=1)

if st.button("Predict Diabetes Risk"):
    # Pass all 8 features in the exact training sequence
    raw_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    
    # Scale raw data using loaded scaler
    scaled_data = scaler.transform(raw_data)
    
    # Run prediction
    prediction = active_model.predict(scaled_data)[0]
    
    if prediction == 1:
        st.error(f"**Result ({selected_model}):** High Risk of Diabetes")
    else:
        st.success(f"**Result ({selected_model}):** Low Risk / Negative")