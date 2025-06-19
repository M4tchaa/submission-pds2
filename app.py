import streamlit as st
import numpy as np
import joblib

# Load model
model = joblib.load("model/xgb_model.pkl")

st.set_page_config(page_title="Prediksi Dropout Siswa", page_icon="🎓")
st.title("🎓 Prediksi Dropout Siswa - Jaya Jaya Institut")

st.markdown("Silakan isi data siswa berikut. Sistem akan memprediksi apakah siswa berisiko *dropout* berdasarkan model yang telah dilatih.")

# Mapping kategori
marital_map = {
    'Single': 1,
    'Married': 2,
    'Widowed': 3,
    'Divorced': 4,
    'Facto Union': 5,
    'Legally Separated': 6
}
gender_map = {'Perempuan': 0, 'Laki-laki': 1}
bool_map = {'Tidak': 0, 'Ya': 1}

# Form input
st.subheader("🧑‍🎓 Data Sosial & Administratif")
col1, col2 = st.columns(2)

with col1:
    marital = st.selectbox("Status Pernikahan", list(marital_map.keys()))
    application_mode = st.number_input("Kode Mode Aplikasi", min_value=1, max_value=57, value=17, help="Contoh: 17 untuk mode umum")
    application_order = st.slider("Urutan Pilihan Jurusan", 0, 10, 1)
    nationality = st.number_input("Kode Negara", min_value=1, max_value=109, value=1)
    age = st.slider("Usia saat Mendaftar", 17, 60, 19)

with col2:
    gender = st.radio("Jenis Kelamin", list(gender_map.keys()), horizontal=True)
    scholarship = st.radio("Penerima Beasiswa?", list(bool_map.keys()), horizontal=True)
    displaced = st.radio("Apakah Terdampak Relokasi?", list(bool_map.keys()), horizontal=True)
    special_needs = st.radio("Berkebutuhan Khusus?", list(bool_map.keys()), horizontal=True)
    international = st.radio("Mahasiswa Internasional?", list(bool_map.keys()), horizontal=True)

st.subheader("🏫 Data Akademik")
col3, col4 = st.columns(2)

with col3:
    course = st.number_input("Kode Program Studi", min_value=1, max_value=9999, value=9238)
    admission_grade = st.number_input("Nilai Masuk (0-200)", 0.0, 200.0, 130.0)
    prev_qual = st.number_input("Tingkat Pendidikan Sebelumnya", 1, 50, 1)
    prev_grade = st.number_input("Nilai Pendidikan Sebelumnya", 0.0, 200.0, 130.0)
    daytime = st.radio("Jadwal Belajar", ['Malam (0)', 'Siang (1)'])
    debtor = st.radio("Ada Tunggakan?", list(bool_map.keys()), horizontal=True)
    tuition_ok = st.radio("Pembayaran Lunas?", list(bool_map.keys()), horizontal=True)

with col4:
    mother_qual = st.slider("Pendidikan Ibu (Kode)", 1, 44, 19)
    father_qual = st.slider("Pendidikan Ayah (Kode)", 1, 44, 19)
    mother_job = st.slider("Pekerjaan Ibu (Kode)", 1, 44, 5)
    father_job = st.slider("Pekerjaan Ayah (Kode)", 1, 44, 9)

st.subheader("📚 Data Perkuliahan Semester 1")
cu1_credited = st.number_input("CU Semester 1 Diakui", 0, 20, 0)
cu1_enrolled = st.number_input("CU Semester 1 Diambil", 0, 20, 6)
cu1_eval = st.number_input("CU Semester 1 Dievaluasi", 0, 20, 6)
cu1_approved = st.number_input("CU Semester 1 Lulus", 0, 20, 5)
cu1_grade = st.number_input("Rata-rata Nilai CU Semester 1", 0.0, 20.0, 12.0)
cu1_wo_eval = st.number_input("CU Semester 1 Tidak Dievaluasi", 0, 10, 0)

st.subheader("📚 Data Perkuliahan Semester 2")
cu2_credited = st.number_input("CU Semester 2 Diakui", 0, 20, 0)
cu2_enrolled = st.number_input("CU Semester 2 Diambil", 0, 20, 6)
cu2_eval = st.number_input("CU Semester 2 Dievaluasi", 0, 20, 6)
cu2_approved = st.number_input("CU Semester 2 Lulus", 0, 20, 5)
cu2_grade = st.number_input("Rata-rata Nilai CU Semester 2", 0.0, 20.0, 12.0)
cu2_wo_eval = st.number_input("CU Semester 2 Tidak Dievaluasi", 0, 10, 0)

st.subheader("📈 Data Ekonomi Makro")
unemployment = st.number_input("Tingkat Pengangguran (%)", 0.0, 20.0, 10.0)
inflation = st.number_input("Tingkat Inflasi (%)", -5.0, 10.0, 1.5)
gdp = st.number_input("GDP (%)", -10.0, 10.0, 0.5)

# Tombol prediksi
if st.button("🔍 Prediksi Dropout"):
    input_data = np.array([[
        marital_map[marital], application_mode, application_order, course,
        1 if 'Siang' in daytime else 0, prev_qual, prev_grade, nationality,
        mother_qual, father_qual, mother_job, father_job, admission_grade,
        bool_map[displaced], bool_map[special_needs], bool_map[debtor], bool_map[tuition_ok],
        gender_map[gender], bool_map[scholarship], age, bool_map[international],
        cu1_credited, cu1_enrolled, cu1_eval, cu1_approved, cu1_grade, cu1_wo_eval,
        cu2_credited, cu2_enrolled, cu2_eval, cu2_approved, cu2_grade, cu2_wo_eval,
        unemployment, inflation, gdp
    ]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Siswa ini diprediksi **Dropout**.\nProbabilitas: {probability:.2%}")
    else:
        st.success(f"✅ Siswa ini diprediksi **Tidak Dropout**.\nProbabilitas Dropout: {probability:.2%}")
