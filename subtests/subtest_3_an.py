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

def render_timer(seconds_remaining, email, current_sub=3, next_sub=4):
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

def render_subtest_3_an():
    if "step_sub3" not in st.session_state: st.session_state.step_sub3 = "instruction"
    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub3 == "instruction":
        st.title("📑 Petunjuk Subtes 3 (Persamaan Kata / Analogi)")
        st.info("Pilihlah kata yang memiliki hubungan analogi paling sesuai.")
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 3 🚀", type="primary"):
            st.session_state.step_sub3 = "test"
            if "sub3" not in st.session_state.start_times: st.session_state.start_times["sub3"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub3 == "test":
        st.title("🧠 Subtes 3")
        if "sub3" not in st.session_state.start_times: st.session_state.start_times["sub3"] = time.time()
        elapsed = int(time.time() - st.session_state.start_times["sub3"])
        remaining = max(0, 420 - elapsed) # 7 menit

        if remaining <= 0:
            st.session_state.current_subtest = 4
            st.query_params["subtest"] = "4"
            save_state_disk(email)
            time.sleep(0.3)
            st.rerun()

        render_timer(remaining, email, 3, 4)

        opts_default = ["a", "b", "c", "d", "e"]
        for q_id in range(41, 61):
            curr_val = st.session_state.answers.get(q_id, None)
            idx = opts_default.index(curr_val) if curr_val in opts_default else None
            ans = st.radio(f"**Soal No. {q_id}:** [Analogi Soal No. {q_id}]", options=opts_default, index=idx, key=f"q_{q_id}")
            st.session_state.answers[q_id] = ans

        save_state_disk(email)
        st.markdown("---")
        if st.button("Simpan & Lanjut ke Subtes 4 ➔", type="primary"):
            st.session_state.current_subtest = 4
            st.query_params["subtest"] = "4"
            save_state_disk(email)
            st.rerun()
