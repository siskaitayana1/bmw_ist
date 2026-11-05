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
        "current_subtest": 1,
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
        ⏱️ SISA WAKTU SUBTES 1: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=2&email={safe_email}";
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

def render_subtest_1_se():
    st.title("🧠 Subtes 1 (Melengkapi Kalimat)")
    
    with st.expander("📌 **Petunjuk & Contoh Pengerjaan (Klik untuk membaca)**", expanded=True):
        st.markdown("""
        **Petunjuk**: Pada setiap kalimat, satu kata hilang. Pilihlah kata pengganti yang paling tepat untuk menyempurnakan kalimat tersebut.
        
        * **Contoh 01**: Seekor kuda mempunyai kesamaan terbanyak dengan seekor .....  
          a) kucing &nbsp;&nbsp; b) bajing &nbsp;&nbsp; c) keledai &nbsp;&nbsp; d) lembu &nbsp;&nbsp; e) anjing  
          *Jawaban yang benar*: **c) keledai**
          
        * **Contoh 02**: Lawannya “harapan” ialah .....  
          a) duka &nbsp;&nbsp; b) putus asa &nbsp;&nbsp; c) sengsara &nbsp;&nbsp; d) cinta &nbsp;&nbsp; e) benci  
          *Jawaban yang benar*: **b) putus asa**
        """)

    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub1" not in st.session_state.start_times:
        st.session_state.start_times["sub1"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub1"])
    remaining = max(0, 360 - elapsed) # 6 menit

    if remaining <= 0:
        st.session_state.current_subtest = 2
        st.query_params["subtest"] = "2"
        save_state_disk(email)
        time.sleep(0.3)
        st.rerun()

    show_live_timer(remaining, email)

    questions = [
        (1, "Pengaruh seseorang terhadap orang lain seharusnya bergantung pada .....", ["a) kekuasaan", "b) bujukan", "c) kekayaan", "d) keberanian", "e) kewibawaan"]),
        (2, "Lawannya “hemat” ialah .....", ["a) murah", "b) kikir", "c) boros", "d) bernilai", "e) kaya"]),
        (3, "..... tidak termasuk cuaca.", ["a) angin puyuh", "b) halilintar", "c) salju", "d) gempa bumi", "e) kabut"]),
        (4, "Lawannya “setia” ialah .....", ["a) cinta", "b) benci", "c) persahabatan", "d) khianat", "e) permusuhan"]),
        (5, "Seekor kuda selalu mempunyai .....", ["a) kandang", "b) ladam", "c) pelana", "d) kuku", "e) surai"]),
        (6, "Seorang paman ..... lebih tua dari kemenakannya.", ["a) jarang", "b) biasanya", "c) selalu", "d) tidak pernah", "e) kadang-kadang"]),
        (7, "Pada jumlah yang sama, nilai kalori yang tertinggi terdapat pada .....", ["a) ikan", "b) daging", "c) lemak", "d) tahu", "e) sayuran"]),
        (8, "Pada suatu pertandingan selalu terdapat .....", ["a) lawan", "b) wasit", "c) penonton", "d) sorak", "e) kemenangan"]),
        (9, "Suatu pernyataan yang belum dipastikan dikatakan sebagai pernyataan yang .....", ["a) paradoks", "b) tergesa-gesa", "c) mempunyai arti rangkap", "d) menyesatkan", "e) hipotesis"]),
        (10, "Pada sepatu selalu terdapat .....", ["a) kulit", "b) sol", "c) tali sepatu", "d) gesper", "e) lidah"]),
        (11, "Suatu ..... tidak menyangkut persoalan pencegahan kecelakaan.", ["a) lampu lalu lintas", "b) kacamata pelindung", "c) kotak PPPK", "d) tanda peringatan", "e) palang kereta api"]),
        (12, "Mata uang logam Rp 50,- tahun 1991, garis tengahnya ialah ..... mm.", ["a) 17", "b) 29", "c) 25", "d) 20", "e) 15"]),
        (13, "Seseorang yang bersikap menyangsikan setiap kemajuan ialah seorang yang .....", ["a) demokratis", "b) radikal", "c) liberal", "d) konservatif", "e) anarkis"]),
        (14, "Lawannya “tidak pernah” ialah .....", ["a) sering", "b) kadang-kadang", "c) jarang", "d) kerap kali", "e) selalu"]),
        (15, "Jarak antara Jakarta – Surabaya kira-kira ..... Km", ["a) 650", "b) 1000", "c) 800", "d) 600", "e) 950"]),
        (16, "Untuk dapat membuat nada yang rendah dan mendalam, kita memerlukan banyak .....", ["a) kekuatan", "b) peranan", "c) ayunan", "d) berat", "e) suara"]),
        (17, "Ayah ..... lebih berpengalaman dari pada anaknya.", ["a) selalu", "b) biasanya", "c) jauh", "d) jarang", "e) pada dasarnya"]),
        (18, "Diantara kota-kota berikut ini, maka kota ..... letaknya paling selatan.", ["a) Jakarta", "b) Bandung", "c) Cirebon", "d) Semarang", "e) Surabaya"]),
        (19, "Jika kita mengetahui jumlah presentase nomor-nomor lotere yang tidak menang, maka kita dapat menghitung .....", ["a) jumlah nomor yang menang", "b) pajak lotere", "c) kemungkinan menang", "d) jumlah pengikut", "e) tinggi keuntungan"]),
        (20, "Seorang anak yang berumur 10 tahun tingginya rata-rata ..... cm", ["a) 150", "b) 130", "c) 110", "d) 105", "e) 115"])
    ]

    for q_id, q_text, opts in questions:
        st.markdown(f"**Soal No. {q_id}:** {q_text}")
        curr_val = st.session_state.answers.get(q_id, None)
        idx = opts.index(curr_val) if curr_val in opts else None
        ans = st.radio(f"Jawaban No. {q_id}:", options=opts, index=idx, key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 2 ➔", type="primary"):
        st.session_state.current_subtest = 2
        st.query_params["subtest"] = "2"
        save_state_disk(email)
        st.rerun()
