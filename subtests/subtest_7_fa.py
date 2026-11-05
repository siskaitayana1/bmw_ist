import streamlit as st
import streamlit.components.v1 as components
import time, json, os

def save_state_disk(email):
    if not email: return
    safe_id = "".join(c for c in email if c.isalnum())
    filename = f"temp_state_{safe_id}.json"
    data = {
        "user_info": st.session_state.get("user_info", {}),
        "answers": {str(k): v for k, v in st.session_state.get("answers", {}).items() if v is not None},
        "current_subtest": 7,
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
        ⏱️ SISA WAKTU SUBTES 7: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=8&email={safe_email}";
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

def render_subtest_7_fa():
    if "step_sub7" not in st.session_state:
        st.session_state.step_sub7 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub7 == "instruction":
        st.title("📑 Petunjuk Subtes 7")
        st.info("💡 Bacalah petunjuk dan pelajari contoh pengerjaan pada gambar di bawah sebelum memulai tes.")

        img_p = "subtest_7_petunjuk.png" if os.path.exists("subtest_7_petunjuk.png") else "images/subtest_7_petunjuk.png"
        if os.path.exists(img_p):
            st.image(img_p, caption="Petunjuk & Contoh Subtes 7", use_container_width=True)

        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 7 🚀", type="primary"):
            st.session_state.step_sub7 = "test"
            if "sub7" not in st.session_state.start_times:
                st.session_state.start_times["sub7"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub7 == "test":
        st.title("🧠 Subtes 7 (Potongan Gambar)")

        if "sub7" not in st.session_state.start_times:
            st.session_state.start_times["sub7"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub7"])
        remaining = max(0, 420 - elapsed) # 7 menit

        if remaining <= 0:
            st.session_state.current_subtest = 8
            st.query_params["subtest"] = "8"
            save_state_disk(email)
            time.sleep(0.3)
            st.rerun()

        show_live_timer(remaining, email)

        img_s = "subtest_7_soal.png" if os.path.exists("subtest_7_soal.png") else "images/subtest_7_soal.png"
        if os.path.exists(img_s):
            st.image(img_s, caption="Lembar Soal Subtes 7 (No. 117 - 136)", use_container_width=True)

        opts = ["a", "b", "c", "d", "e"]
        for q_num in range(117, 137):
            curr_val = st.session_state.answers.get(q_num, None)
            idx = opts.index(curr_val) if curr_val in opts else None
            ans = st.radio(f"Soal No. {q_num}:", options=opts, index=idx, horizontal=True, key=f"q_{q_num}")
            st.session_state.answers[q_num] = ans

        save_state_disk(email)
        st.markdown("---")
        if st.button("Simpan & Lanjut ke Subtes 8 ➔", type="primary"):
            st.session_state.current_subtest = 8
            st.query_params["subtest"] = "8"
            save_state_disk(email)
            st.rerun()
