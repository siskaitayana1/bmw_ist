import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

from subtests.subtest_1_se import render_subtest_1_se
from subtests.subtest_2_wa import render_subtest_2_wa
from subtests.subtest_3_an import render_subtest_3_an
from subtests.subtest_4_ge import render_subtest_4_ge
from subtests.subtest_5_ra import render_subtest_5_ra
from subtests.subtest_6_zr import render_subtest_6_zr
from subtests.subtest_7_fa import render_subtest_7_fa
from subtests.subtest_8_wu import render_subtest_8_wu

st.set_page_config(page_title="Portal Psikotes Karyawan", page_icon="🧠", layout="wide")

RESULTS_FILE = "rekap_psikotes_karyawan.csv"

def get_temp_filename(email):
    safe_id = "".join(c for c in email if c.isalnum()) if email else "default"
    return f"temp_state_{safe_id}.json"

def save_app_state(email, user_info, answers, subtest, start_times):
    if not email: return
    filename = get_temp_filename(email)
    data = {
        "user_info": user_info,
        "answers": {str(k): v for k, v in answers.items() if v is not None},
        "current_subtest": subtest,
        "start_times": start_times
    }
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception: pass

def load_app_state(email):
    if not email: return {}, {}, 1, {}
    filename = get_temp_filename(email)
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                answers = {int(k): v for k, v in data.get("answers", {}).items()}
                return (
                    data.get("user_info", {}),
                    answers,
                    data.get("current_subtest", 1),
                    data.get("start_times", {})
                )
        except Exception: pass
    return {}, {}, 1, {}

# Kunci Jawaban Pilihan Ganda (Sesuaikan dengan Kunci Asli Anda)
ANSWER_KEYS_MC = {i: "a" for i in range(1, 157)}

def calculate_scores():
    user_answers = st.session_state.get("answers", {})
    s1 = sum(1 for q in range(1, 21) if user_answers.get(q) == ANSWER_KEYS_MC.get(q))
    s2 = sum(1 for q in range(21, 41) if user_answers.get(q) == ANSWER_KEYS_MC.get(q))
    s3 = sum(1 for q in range(41, 61) if user_answers.get(q) == ANSWER_KEYS_MC.get(q))
    s4 = sum(1 for q in range(61, 77) if user_answers.get(q)) # Subtes GE (Isian)
    s5 = sum(1 for q in range(77, 97) if str(user_answers.get(q, '')).strip() == str(ANSWER_KEYS_MC.get(q)))
    s6 = sum(1 for q in range(97, 117) if str(user_answers.get(q, '')).strip() == str(ANSWER_KEYS_MC.get(q)))
    s7 = sum(1 for q in range(117, 137) if str(user_answers.get(q, '')).strip().lower() == str(ANSWER_KEYS_MC.get(q)))
    s8 = sum(1 for q in range(137, 157) if str(user_answers.get(q, '')).strip().lower() == str(ANSWER_KEYS_MC.get(q)))
    
    total = s1 + s2 + s3 + s4 + s5 + s6 + s7 + s8
    return {
        "Subtes_1": s1, "Subtes_2": s2, "Subtes_3": s3, "Subtes_4": s4,
        "Subtes_5": s5, "Subtes_6": s6, "Subtes_7": s7, "Subtes_8": s8,
        "Total_Skor_Mentah": total
    }

params = st.query_params
param_email = params.get("email", "")

if "page" not in st.session_state: st.session_state.page = params.get("page", "register")
if "current_subtest" not in st.session_state: st.session_state.current_subtest = int(params.get("subtest", "1"))
if "user_info" not in st.session_state: st.session_state.user_info = {}
if "answers" not in st.session_state: st.session_state.answers = {}
if "start_times" not in st.session_state: st.session_state.start_times = {}

if param_email:
    u_info, u_ans, u_sub, u_times = load_app_state(param_email)
    if u_info: st.session_state.user_info.update(u_info)
    if u_ans: st.session_state.answers.update(u_ans)
    if u_times: st.session_state.start_times.update(u_times)
    if "page" in params: st.session_state.page = params["page"]
    if "subtest" in params: st.session_state.current_subtest = int(params["subtest"])

if st.session_state.page == "register":
    st.title("🏛️ Portal Psikotes Karyawan")
    with st.form("form_registrasi"):
        nama = st.text_input("Nama Lengkap:")
        email_in = st.text_input("Alamat Email:")
        posisi = st.text_input("Posisi yang Dilamar:")
        btn_start = st.form_submit_button("Mulai Psikotes 🚀", type="primary")

        if btn_start:
            if not nama or not email_in or not posisi:
                st.error("⚠️ Mohon isi seluruh formulir!")
            else:
                st.session_state.user_info = {
                    "nama": nama, "email": email_in, "posisi": posisi,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.page = "test"
                st.session_state.current_subtest = 1
                st.query_params["page"] = "test"
                st.query_params["subtest"] = "1"
                st.query_params["email"] = email_in
                save_app_state(email_in, st.session_state.user_info, st.session_state.answers, 1, st.session_state.start_times)
                st.rerun()

elif st.session_state.page == "test":
    st.caption(f"👤 Peserta: **{st.session_state.user_info.get('nama', '')}** | 💼 Posisi: **{st.session_state.user_info.get('posisi', '')}**")
    st.markdown("---")

    curr_sub = st.session_state.current_subtest
    if curr_sub == 1: render_subtest_1_se()
    elif curr_sub == 2: render_subtest_2_wa()
    elif curr_sub == 3: render_subtest_3_an()
    elif curr_sub == 4: render_subtest_4_ge()
    elif curr_sub == 5: render_subtest_5_ra()
    elif curr_sub == 6: render_subtest_6_zr()
    elif curr_sub == 7: render_subtest_7_fa()
    elif curr_sub == 8: render_subtest_8_wu()
    elif curr_sub >= 9:
        st.session_state.page = "result"
        st.query_params["page"] = "result"
        st.rerun()

elif st.session_state.page == "result":
    st.title("✅ Psikotes Selesai")
    st.success(f"Terima kasih **{st.session_state.user_info.get('nama', '')}**, seluruh jawaban Anda telah tersimpan.")

    if "saved_to_csv" not in st.session_state:
        scores = calculate_scores()
        record = {**st.session_state.user_info, **scores}
        df_new = pd.DataFrame([record])
        if os.path.exists(RESULTS_FILE):
            df_old = pd.read_csv(RESULTS_FILE, sep=';')
            df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(subset=['email', 'tanggal'], keep='last')
        else:
            df_final = df_new
        df_final.to_csv(RESULTS_FILE, index=False, sep=';', encoding='utf-8-sig')
        st.session_state.saved_to_csv = True

    st.info("Hasil tes tersimpan secara otomatis di sistem.")
    st.markdown("---")
    if st.button("🔄 Kembali ke Halaman Utama", type="primary"):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
