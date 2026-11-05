import streamlit as st
import streamlit.components.v1 as components
import time, json

def save_state_disk(email):
    if not email: return
    safe_id = "".join(c for c in email if c.isalnum())
    filename = f"temp_state_{safe_id}.json"
    data = {
        "user_info": st.session_state.get("user_info", {}),
        "answers": {str(k): v for k, v in st.session_state.get("answers", {}).items() if v is not None},
        "current_subtest": 2,
        "start_times": st.session_state.get("start_times", {})
    }
    try:
        with open(filename, "w", encoding="utf-8") as f: json.dump(data, f)
    except Exception: pass

def show_live_timer(seconds_remaining, email):
    safe_email = email.replace("'", "\\'") if email else ""
    components.html(f"""
    <div style="font-family: Arial; font-size: 20px; font-weight: bold; color: #dc2626; 
                background-color: #fef2f2; padding: 12px; border: 2px solid #dc2626; border-radius: 8px; text-align: center;">
        ⏱️ SISA WAKTU SUBTES 2: <span id="timer_display">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        function updateDisplay() {{
            var m = Math.floor(timeLeft / 60); var s = timeLeft % 60;
            var displayM = m < 10 ? "0" + m : m; var displayS = s < 10 ? "0" + s : s;
            var elem = document.getElementById("timer_display");
            if (elem) {{ elem.innerHTML = displayM + ":" + displayS; }}
            if (timeLeft <= 0) {{ 
                if (elem) elem.innerHTML = "00:00 (WAKTU HABIS)"; 
                var newSearch = "?page=test&subtest=3&email={safe_email}";
                setTimeout(function() {{
                    try {{ window.top.location.search = newSearch; }} catch(e) {{}}
                    try {{ window.parent.location.search = newSearch; }} catch(e) {{}}
                    try {{ window.location.search = newSearch; }} catch(e) {{}}
                }}, 300);
            }} else {{ timeLeft--; }}
        }}
        updateDisplay(); setInterval(updateDisplay, 1000);
    </script>
    """, height=75)

def render_subtest_2_wa():
    st.title("🧠 Subtes 2 (Mencari Kata Berbeda)")
    
    with st.expander("📌 **Petunjuk & Contoh Pengerjaan (Klik untuk membaca)**", expanded=True):
        st.markdown("""
        **Petunjuk**: Ditentukan 5 kata. Pada 4 dari 5 kata terdapat suatu kesamaan. Carilah kata kelima yang **tidak memiliki kesamaan** dengan keempat kata lainnya.
        
        * **Contoh 01**:  
          a) meja &nbsp;&nbsp; b) kursi &nbsp;&nbsp; c) burung &nbsp;&nbsp; d) lemari &nbsp;&nbsp; e) tempat tidur  
          *Jawaban yang benar*: **c) burung** (karena c bukan perabot rumah)
          
        * **Contoh 02**:  
          a) duduk &nbsp;&nbsp; b) berbaring &nbsp;&nbsp; c) berdiri &nbsp;&nbsp; d) berjalan &nbsp;&nbsp; e) berjongkok  
          *Jawaban yang benar*: **d) berjalan** (karena d berada dalam keadaan bergerak)
        """)

    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub2" not in st.session_state.start_times:
        st.session_state.start_times["sub2"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub2"])
    remaining = max(0, 360 - elapsed) # 6 menit

    if remaining <= 0:
        st.session_state.current_subtest = 3
        st.query_params["subtest"] = "3"
        save_state_disk(email)
        time.sleep(0.3)
        st.rerun()

    show_live_timer(remaining, email)

    questions = [
        (21, ["a) lingkungan", "b) panah", "c) elips", "d) busur", "e) lengkungan"]),
        (22, ["a) mengetuk", "b) memaki", "c) menjahit", "d) menggergaji", "e) memukul"]),
        (23, ["a) lebar", "b) keliling", "c) luas", "d) isi", "e) panjang"]),
        (24, ["a) mengikat", "b) menyatukan", "c) melepaskan", "d) mengaitkan", "e) melekatkan"]),
        (25, ["a) arah", "b) timur", "c) perjalanan", "d) tujuan", "e) selatan"]),
        (26, ["a) jarak", "b) perpisahan", "c) tugas", "d) batas", "e) perceraian"]),
        (27, ["a) saringan", "b) kelambu", "c) payung", "d) tapisan", "e) jala"]),
        (28, ["a) putih", "b) pucat", "c) buram", "d) kasar", "e) berkilauan"]),
        (29, ["a) otobis", "b) pesawat terbang", "c) sepeda motor", "d) sepeda", "e) kapal api"]),
        (30, ["a) biola", "b) seruling", "c) klarinet", "d) terompet", "e) saxophon"]),
        (31, ["a) bergelombang", "b) kasar", "c) berduri", "d) licin", "e) lurus"]),
        (32, ["a) jam", "b) kompas", "c) penunjuk jalan", "d) bintang pari", "e) arah"]),
        (33, ["a) kebijaksanaan", "b) pendidikan", "c) perencanaan", "d) penempatan", "e) pengerahan"]),
        (34, ["a) bermotor", "b) berjalan", "c) berlayar", "d) bersepeda", "e) berkuda"]),
        (35, ["a) gambar", "b) lukisan", "c) potret", "d) patung", "e) ukiran"]),
        (36, ["a) panjang", "b) lonjong", "c) runcing", "d) bulat", "e) bersudut"]),
        (37, ["a) kunci", "b) palang pintu", "c) gerendel", "d) gunting", "e) obeng"]),
        (38, ["a) jembatan", "b) batas", "c) perkawinan", "d) pagar", "e) masyarakat"]),
        (39, ["a) mengetam", "b) menasehati", "c) mengasah", "d) melicinkan", "e) menggosok"]),
        (40, ["a) batu", "b) baja", "c) bulu", "d) karet", "e) kayu"])
    ]

    for q_id, opts in questions:
        curr_val = st.session_state.answers.get(q_id, None)
        idx = opts.index(curr_val) if curr_val in opts else None
        ans = st.radio(f"**{q_id}.**", options=opts, index=idx, key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 3 ➔", type="primary"):
        st.session_state.current_subtest = 3
        st.query_params["subtest"] = "3"
        save_state_disk(email)
        st.rerun()
