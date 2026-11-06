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

def render_timer(seconds_remaining, email, current_sub=7, next_sub=8):
    safe_email = email.replace("'", "\\'") if email else ""
    target_url = f"?page=result&email={safe_email}" if next_sub >= 9 else f"?page=test&subtest={next_sub}&email={safe_email}"
    components.html(f"""
    <div style="font-family: Arial; font-size: 18px; font-weight: bold; color: #dc2626; background-color: #fef2f2; padding: 10px; border: 2px solid #dc2626; border-radius: 8px; text-align: center;">
        ⏱️ SISA WAKTU SUBTES {current_sub}: <span id="timer_display">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        var redirected = false;
        function updateTimer() {{
            var m = Math.floor(timeLeft / 60); var s = timeLeft % 60;
            var display = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
            var elem = document.getElementById("timer_display");
            if (elem) elem.innerHTML = display;
            if (timeLeft <= 0 && !redirected) {{
                redirected = true;
                if (elem) elem.innerHTML = "00:00 (WAKTU HABIS)";
                var url = window.top.location.pathname + "{target_url}";
                try {{ window.top.location.href = url; }} catch(e) {{}}
                try {{ window.parent.location.href = url; }} catch(e) {{}}
                try {{ window.location.href = url; }} catch(e) {{}}
            }} else {{ timeLeft--; }}
        }}
        updateTimer(); setInterval(updateTimer, 1000);
    </script>
    """, height=70)

def render_subtest_7_fa():
    if "step_sub7" not in st.session_state: st.session_state.step_sub7 = "instruction"
    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub7 == "instruction":
        st.title("📑 Petunjuk Subtes 7 (Potongan Gambar)")
        st.info("Pelajari gambar petunjuk sebelum memulai.")
        img_p = "subtest_7_petunjuk.png" if os.path.exists("subtest_7_petunjuk.png") else "images/subtest_7_petunjuk.png"
        if os.path.exists(img_p): st.image(img_p, caption="Petunjuk Subtes 7", use_container_width=True)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 7 🚀", type="primary"):
            st.session_state.step_sub7 = "test"
            if "sub7" not in st.session_state.start_times: st.session_state.start_times["sub7"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub7 == "test":
        st.title("🧠 Subtes 7")
        if "sub7" not in st.session_state.start_times: st.session_state.start_times["sub7"] = time.time()
        elapsed = int(time.time() - st.session_state.start_times["sub7"])
        remaining = max(0, 420 - elapsed) # 7 menit

        if remaining <= 0:
            st.session_state.current_subtest = 8
            st.query_params["subtest"] = "8"
            save_state_disk(email)
            time.sleep(0.3)
            st.rerun()

        render_timer(remaining, email, 7, 8)
        img_s = "subtest_7_soal.png" if os.path.exists("subtest_7_soal.png") else "images/subtest_7_soal.png"
        if os.path.exists(img_s): st.image(img_s, caption="Soal Subtes 7 (No. 117 - 136)", use_container_width=True)

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
