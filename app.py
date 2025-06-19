import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("model/xgb_model.pkl")

st.set_page_config(page_title="Prediksi Dropout Siswa", page_icon="🎓")
st.title("Prediksi Dropout Siswa - Jaya Jaya Institut")
st.markdown("Isi data siswa di bawah ini untuk memprediksi apakah siswa berisiko *dropout* atau tidak.")

# Input form
course = st.number_input("Kode Program Studi", min_value=0)
prev_grade = st.number_input("Nilai Kualifikasi Sebelumnya", min_value=0.0, max_value=200.0)
admission_grade = st.number_input("Nilai Masuk", min_value=0.0, max_value=200.0)
age = st.number_input("Usia saat mendaftar", min_value=15, max_value=70)
units_approved_1 = st.number_input("Jumlah Mata Kuliah Lulus Semester 1", min_value=0)

# Tombol prediksi
if st.button("Prediksi"):
    
    input_data = np.array([[course, prev_grade, admission_grade, age, units_approved_1]])
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Siswa ini berisiko *Dropout*. Probabilitas: {probability:.2%}")
    else:
        st.success(f"✅ Siswa ini diprediksi **tidak** dropout. Probabilitas dropout: {probability:.2%}")
