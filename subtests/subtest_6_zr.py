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
        "current_subtest": 6,
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
        ⏱️ SISA WAKTU SUBTES 6: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=7&email={safe_email}";
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

def render_subtest_6_zr():
    st.title("🧠 Subtes 6 (Deret Angka)")
    
    with st.expander("📌 **Petunjuk & Contoh Pengerjaan (Klik untuk membaca)**", expanded=True):
        st.markdown("""
        **Petunjuk**: Pada deret angka berikut, tentukan angka berikutnya berdasarkan pola aturan tertentu.
        
        * **Contoh 01**: 2 &nbsp; 4 &nbsp; 6 &nbsp; 8 &nbsp; 10 &nbsp; 12 &nbsp; 14 &nbsp; ?  
          *Jawaban*: **16** (pola: ditambah 2)
          
        * **Contoh 02**: 9 &nbsp; 7 &nbsp; 10 &nbsp; 8 &nbsp; 11 &nbsp; 9 &nbsp; 12 &nbsp; ?  
          *Jawaban*: **10** (pola: berganti-ganti dikurangi 2 lalu ditambah 3)
        """)

    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub6" not in st.session_state.start_times:
        st.session_state.start_times["sub6"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub6"])
    remaining = max(0, 600 - elapsed) # 10 menit

    if remaining <= 0:
        st.session_state.current_subtest = 7
        st.query_params["subtest"] = "7"
        save_state_disk(email)
        time.sleep(0.3)
        st.rerun()

    show_live_timer(remaining, email)

    questions = [
        (97, "6 &nbsp; 9 &nbsp; 12 &nbsp; 15 &nbsp; 18 &nbsp; 21 &nbsp; 24 &nbsp; ?"),
        (98, "15 &nbsp; 16 &nbsp; 18 &nbsp; 19 &nbsp; 21 &nbsp; 22 &nbsp; 24 &nbsp; ?"),
        (99, "19 &nbsp; 18 &nbsp; 22 &nbsp; 21 &nbsp; 25 &nbsp; 24 &nbsp; 28 &nbsp; ?"),
        (100, "16 &nbsp; 12 &nbsp; 17 &nbsp; 13 &nbsp; 18 &nbsp; 14 &nbsp; 19 &nbsp; ?"),
        (101, "2 &nbsp; 4 &nbsp; 8 &nbsp; 10 &nbsp; 20 &nbsp; 22 &nbsp; 44 &nbsp; ?"),
        (102, "15 &nbsp; 13 &nbsp; 16 &nbsp; 12 &nbsp; 17 &nbsp; 11 &nbsp; 18 &nbsp; ?"),
        (103, "25 &nbsp; 22 &nbsp; 11 &nbsp; 33 &nbsp; 30 &nbsp; 15 &nbsp; 45 &nbsp; ?"),
        (104, "49 &nbsp; 51 &nbsp; 54 &nbsp; 27 &nbsp; 9 &nbsp; 11 &nbsp; 14 &nbsp; ?"),
        (105, "2 &nbsp; 3 &nbsp; 1 &nbsp; 3 &nbsp; 4 &nbsp; 2 &nbsp; 4 &nbsp; ?"),
        (106, "19 &nbsp; 17 &nbsp; 20 &nbsp; 16 &nbsp; 21 &nbsp; 15 &nbsp; 22 &nbsp; ?"),
        (107, "94 &nbsp; 92 &nbsp; 46 &nbsp; 44 &nbsp; 22 &nbsp; 20 &nbsp; 10 &nbsp; ?"),
        (108, "5 &nbsp; 8 &nbsp; 9 &nbsp; 8 &nbsp; 11 &nbsp; 12 &nbsp; 11 &nbsp; ?"),
        (109, "12 &nbsp; 15 &nbsp; 19 &nbsp; 23 &nbsp; 28 &nbsp; 33 &nbsp; 39 &nbsp; ?"),
        (110, "7 &nbsp; 5 &nbsp; 10 &nbsp; 7 &nbsp; 21 &nbsp; 17 &nbsp; 68 &nbsp; ?"),
        (111, "11 &nbsp; 15 &nbsp; 18 &nbsp; 9 &nbsp; 13 &nbsp; 16 &nbsp; 8 &nbsp; ?"),
        (112, "3 &nbsp; 8 &nbsp; 15 &nbsp; 24 &nbsp; 35 &nbsp; 48 &nbsp; 63 &nbsp; ?"),
        (113, "4 &nbsp; 5 &nbsp; 7 &nbsp; 4 &nbsp; 8 &nbsp; 13 &nbsp; 7 &nbsp; ?"),
        (114, "8 &nbsp; 5 &nbsp; 15 &nbsp; 18 &nbsp; 6 &nbsp; 3 &nbsp; 9 &nbsp; ?"),
        (115, "15 &nbsp; 6 &nbsp; 18 &nbsp; 10 &nbsp; 30 &nbsp; 23 &nbsp; 69 &nbsp; ?"),
        (116, "5 &nbsp; 35 &nbsp; 28 &nbsp; 4 &nbsp; 11 &nbsp; 77 &nbsp; 70 &nbsp; ?")
    ]

    for q_id, q_text in questions:
        curr_val = st.session_state.answers.get(q_id, "")
        ans = st.text_input(f"**Soal No. {q_id}:** {q_text}", value=curr_val if curr_val else "", key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans.strip() if ans else None

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 7 ➔", type="primary"):
        st.session_state.current_subtest = 7
        st.query_params["subtest"] = "7"
        save_state_disk(email)
        st.rerun()
