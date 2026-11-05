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
        "current_subtest": 8,
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
        ⏱️ SISA WAKTU SUBTES 8: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=9&email={safe_email}";
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

def render_subtest_8_wu():
    if "step_sub8" not in st.session_state:
        st.session_state.step_sub8 = "instruction"

    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub8 == "instruction":
        st.title("📑 Petunjuk Subtes 8")
        st.info("💡 Bacalah petunjuk dan pelajari contoh pengerjaan pada gambar di bawah sebelum memulai tes.")

        img_p = "subtest_8_petunjuk.png" if os.path.exists("subtest_8_petunjuk.png") else "images/subtest_8_petunjuk.png"
        if os.path.exists(img_p):
            st.image(img_p, caption="Petunjuk & Contoh Subtes 8", use_container_width=True)

        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 8 🚀", type="primary"):
            st.session_state.step_sub8 = "test"
            if "sub8" not in st.session_state.start_times:
                st.session_state.start_times["sub8"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub8 == "test":
        st.title("🧠 Subtes 8 (Rotasi Kubus 3D)")

        if "sub8" not in st.session_state.start_times:
            st.session_state.start_times["sub8"] = time.time()

        elapsed = int(time.time() - st.session_state.start_times["sub8"])
        remaining = max(0, 540 - elapsed) # 9 menit

        if remaining <= 0:
            st.session_state.current_subtest = 9
            st.query_params["subtest"] = "9"
            save_state_disk(email)
            time.sleep(0.3)
            st.rerun()

        show_live_timer(remaining, email)

        img_s = "subtest_8_soal.png" if os.path.exists("subtest_8_soal.png") else "images/subtest_8_soal.png"
        if os.path.exists(img_s):
            st.image(img_s, caption="Lembar Soal Subtes 8 (No. 137 - 156)", use_container_width=True)

        opts = ["a", "b", "c", "d", "e"]
        for q_num in range(137, 157):
            curr_val = st.session_state.answers.get(q_num, None)
            idx = opts.index(curr_val) if curr_val in opts else None
            ans = st.radio(f"Soal No. {q_num}:", options=opts, index=idx, horizontal=True, key=f"q_{q_num}")
            st.session_state.answers[q_num] = ans

        save_state_disk(email)
        st.markdown("---")
        if st.button("Simpan & Selesaikan Ujian 🏁", type="primary"):
            st.session_state.current_subtest = 9
            st.query_params["subtest"] = "9"
            save_state_disk(email)
            st.rerun()
