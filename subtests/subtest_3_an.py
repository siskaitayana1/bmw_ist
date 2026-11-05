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
        "current_subtest": 3,
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
        ⏱️ SISA WAKTU SUBTES 3: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=4&email={safe_email}";
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

def render_subtest_3_an():
    st.title("🧠 Subtes 3 (Persamaan Kata / Analogi)")
    
    with st.expander("📌 **Petunjuk & Contoh Pengerjaan (Klik untuk membaca)**", expanded=True):
        st.markdown("""
        **Petunjuk**: Antara kata pertama dan kedua terdapat hubungan tertentu. Antara kata ketiga dan salah satu kata pilihan harus memiliki hubungan setara.
        
        * **Contoh 01**: Hutan : pohon = tembok : ?  
          a) batu bata &nbsp;&nbsp; b) rumah &nbsp;&nbsp; c) semen &nbsp;&nbsp; d) putih &nbsp;&nbsp; e) dinding  
          *Jawaban yang benar*: **a) batu bata** (karena hutan terdiri atas pohon-pohon, dan tembok terdiri atas batu bata)
          
        * **Contoh 02**: Gelap : terang = basah : ?  
          a) hujan &nbsp;&nbsp; b) hari &nbsp;&nbsp; c) lembab &nbsp;&nbsp; d) angin &nbsp;&nbsp; e) kering  
          *Jawaban yang benar*: **e) kering** (karena gelap lawan dari terang, dan basah lawan dari kering)
        """)

    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub3" not in st.session_state.start_times:
        st.session_state.start_times["sub3"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub3"])
    remaining = max(0, 420 - elapsed) # 7 menit

    if remaining <= 0:
        st.session_state.current_subtest = 4
        st.query_params["subtest"] = "4"
        save_state_disk(email)
        time.sleep(0.3)
        st.rerun()

    show_live_timer(remaining, email)

    questions = [
        (41, "Menemukan : menghilangkan = Mengingat : ?", ["a) menghapal", "b) mengenai", "c) melupakan", "d) berpikir", "e) memimpikan"]),
        (42, "Bunga : jambangan = Burung : ?", ["a) sarang", "b) langit", "c) pagar", "d) pohon", "e) sangkar"]),
        (43, "Kereta api : rel = Otobis : ?", ["a) roda", "b) poros", "c) ban", "d) jalan raya", "e) kecepatan"]),
        (44, "Perak : emas = Cincin : ?", ["a) arloji", "b) berlian", "c) permata", "d) gelang", "e) platin"]),
        (45, "Lingkaran : bola = Bujur sangkar : ?", ["a) bentuk", "b) gambar", "c) segi empat", "d) kubus", "e) piramid"]),
        (46, "Saran : kepustakaan = Merundingkan : ?", ["a) menawarkan", "b) menentukan", "c) menilai", "d) menimbang", "e) merenungkan"]),
        (47, "Lidah : asam = Hidung : ?", ["a) mencium", "b) bernapas", "c) mengecap", "d) tengik", "e) asin"]),
        (48, "Darah : pembuluh = Air : ?", ["a) pintu air", "b) sungai", "c) talang", "d) hujan", "e) ember"]),
        (49, "Saraf : penyalur = Pupil : ?", ["a) penyinaran", "b) mata", "c) melihat", "d) cahaya", "e) pelindung"]),
        (50, "Pengantar surat : pengantar telegram = Pandai besi : ?", ["a) palu godam", "b) pedagang besi", "c) api", "d) tukang emas", "e) besi tempa"]),
        (51, "Buta : warna = Tuli : ?", ["a) pendengaran", "b) mendengar", "c) nada", "d) kata", "e) telinga"]),
        (52, "Makanan : bumbu = Ceramah : ?", ["a) penghinaan", "b) pidato", "c) kelakar", "d) kesan", "e) ayat"]),
        (53, "Marah : emosi = Duka cita : ?", ["a) suka cita", "b) sakit hati", "c) suasana hati", "d) sedih", "e) rindu"]),
        (54, "Mantel : jubah = wool : ?", ["a) bahan sandang", "b) domba", "c) sutra", "d) jas", "e) tekstil"]),
        (55, "Ketinggian puncak : tekanan udara = ketinggian nada : ?", ["a) garpu tala", "b) sopran", "c) nyanyian", "d) panjang senar", "e) suara"]),
        (56, "Negara : revolusi = Hidup : ?", ["a) biologi", "b) keturunan", "c) mutasi", "d) seleksi", "e) ilmu hewan"]),
        (57, "Kekurangan : penemuan = Panas : ?", ["a) haus", "b) khatulistiwa", "c) es", "d) matahari", "e) dingin"]),
        (58, "Kayu : diketam = Besi : ?", ["a) dipalu", "b) digergaji", "c) dituang", "d) dikikir", "e) ditempa"]),
        (59, "Olahragawan : lembing = Cendekiawan : ?", ["a) perpustakaan", "b) penelitian", "c) karya", "d) studi", "e) mikroskop"]),
        (60, "Keledai : kuda pacuan = Pembakaran : ?", ["a) pemadam api", "b) obor", "c) letupan", "d) korek api", "e) lautan api"])
    ]

    for q_id, q_text, opts in questions:
        st.markdown(f"**Soal No. {q_id}:** {q_text}")
        curr_val = st.session_state.answers.get(q_id, None)
        idx = opts.index(curr_val) if curr_val in opts else None
        ans = st.radio(f"Jawaban No. {q_id}:", options=opts, index=idx, key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 4 ➔", type="primary"):
        st.session_state.current_subtest = 4
        st.query_params["subtest"] = "4"
        save_state_disk(email)
        st.rerun()
