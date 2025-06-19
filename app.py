import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("model/xgb_model.pkl")

st.set_page_config(page_title="Prediksi Dropout Siswa", page_icon="🎓")
st.title("Prediksi Dropout Siswa - Jaya Jaya Institut")

st.markdown("Silakan isi data siswa berikut untuk melakukan prediksi risiko dropout. Semua field wajib diisi.")

# Buat helper untuk form
def binary_input(label, default=0):
    return st.radio(label, ['Tidak', 'Ya'], index=default, horizontal=True) == 'Ya'

def numeric_input(label, min_val=0, max_val=9999, default=0, step=1, help=None):
    return st.number_input(label, min_value=min_val, max_value=max_val, value=default, step=step, help=help)

# Bagi menjadi 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    marital_status = numeric_input("Marital Status", 1, 6, 1)
    application_mode = numeric_input("Application Mode", 1, 57, 17)
    application_order = numeric_input("Application Order", 0, 10, 1)
    course = numeric_input("Kode Program Studi", 0, 9999, 9238)
    daytime_evening = numeric_input("Jadwal (1=Siang, 0=Malam)", 0, 1, 1)
    previous_qualification = numeric_input("Tingkat Pendidikan Sebelumnya", 1, 50, 1)
    previous_grade = st.number_input("Nilai Kualifikasi Sebelumnya", 0.0, 200.0, 130.0)
    nationality = numeric_input("Kode Negara", 1, 110, 1)
    mother_qual = numeric_input("Pendidikan Ibu", 1, 50, 19)
    father_qual = numeric_input("Pendidikan Ayah", 1, 50, 19)

with col2:
    mother_job = numeric_input("Pekerjaan Ibu", 1, 50, 5)
    father_job = numeric_input("Pekerjaan Ayah", 1, 50, 9)
    admission_grade = st.number_input("Nilai Masuk", 0.0, 200.0, 130.0)
    displaced = binary_input("Siswa Terdampak Relokasi?")
    special_needs = binary_input("Berkebutuhan Khusus?")
    debtor = binary_input("Memiliki Tunggakan?")
    tuition_up_to_date = binary_input("Pembayaran Lunas?")
    gender = numeric_input("Gender (0=F, 1=M)", 0, 1, 1)
    scholarship = binary_input("Penerima Beasiswa?")
    age_enroll = numeric_input("Usia Saat Mendaftar", 15, 70, 19)

with col3:
    international = binary_input("Mahasiswa Internasional?")
    cu1_credited = numeric_input("CU 1st Sem Credited", 0, 20, 0)
    cu1_enrolled = numeric_input("CU 1st Sem Enrolled", 0, 20, 6)
    cu1_eval = numeric_input("CU 1st Sem Evaluated", 0, 20, 6)
    cu1_approved = numeric_input("CU 1st Sem Lulus", 0, 20, 5)
    cu1_grade = st.number_input("CU 1st Sem Rata-rata Nilai", 0.0, 20.0, 12.0)
    cu1_wo_eval = numeric_input("CU 1st Sem Tanpa Evaluasi", 0, 10, 0)
    cu2_credited = numeric_input("CU 2nd Sem Credited", 0, 20, 0)
    cu2_enrolled = numeric_input("CU 2nd Sem Enrolled", 0, 20, 6)
    cu2_eval = numeric_input("CU 2nd Sem Evaluated", 0, 20, 6)
    cu2_approved = numeric_input("CU 2nd Sem Lulus", 0, 20, 5)
    cu2_grade = st.number_input("CU 2nd Sem Rata-rata Nilai", 0.0, 20.0, 12.0)
    cu2_wo_eval = numeric_input("CU 2nd Sem Tanpa Evaluasi", 0, 10, 0)
    unemployment = st.number_input("Tingkat Pengangguran Nasional (%)", 0.0, 20.0, 10.0)
    inflation = st.number_input("Tingkat Inflasi (%)", -5.0, 10.0, 1.5)
    gdp = st.number_input("GDP (%)", -10.0, 10.0, 0.5)

# Tombol Prediksi
if st.button("🔍 Prediksi Dropout"):
    input_array = np.array([[
        marital_status, application_mode, application_order, course, daytime_evening,
        previous_qualification, previous_grade, nationality, mother_qual, father_qual,
        mother_job, father_job, admission_grade, int(displaced), int(special_needs),
        int(debtor), int(tuition_up_to_date), gender, int(scholarship), age_enroll,
        int(international), cu1_credited, cu1_enrolled, cu1_eval, cu1_approved, cu1_grade,
        cu1_wo_eval, cu2_credited, cu2_enrolled, cu2_eval, cu2_approved, cu2_grade,
        cu2_wo_eval, unemployment, inflation, gdp
    ]])

    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Siswa ini diprediksi **Dropout**. Probabilitas: {probability:.2%}")
    else:
        st.success(f"✅ Siswa ini diprediksi **Tidak Dropout**. Probabilitas Dropout: {probability:.2%}")
