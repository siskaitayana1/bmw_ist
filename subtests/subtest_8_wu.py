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

def render_timer(seconds_remaining, email, current_sub=8, next_sub=9):
    safe_email = email.replace("'", "\\'") if email else ""
    target_url = f"?page=result&email={safe_email}"
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
                if (elem) elem.innerHTML = "00:00 (WAKTU HABIS - MENYIMPAN DATA)";
                var url = window.top.location.pathname + "{target_url}";
                try {{ window.top.location.href = url; }} catch(e) {{}}
                try {{ window.parent.location.href = url; }} catch(e) {{}}
                try {{ window.location.href = url; }} catch(e) {{}}
            }} else {{ timeLeft--; }}
        }}
        updateTimer(); setInterval(updateTimer, 1000);
    </script>
    """, height=70)

def render_subtest_8_wu():
    if "step_sub8" not in st.session_state: st.session_state.step_sub8 = "instruction"
    email = st.session_state.get("user_info", {}).get("email", "")

    if st.session_state.step_sub8 == "instruction":
        st.title("📑 Petunjuk Subtes 8 (Rotasi Kubus 3D)")
        st.info("Pelajari gambar petunjuk sebelum memulai.")
        img_p = "subtest_8_petunjuk.png" if os.path.exists("subtest_8_petunjuk.png") else "images/subtest_8_petunjuk.png"
        if os.path.exists(img_p): st.image(img_p, caption="Petunjuk Subtes 8", use_container_width=True)
        st.markdown("---")
        if st.button("Mulai Kerjakan Subtes 8 🚀", type="primary"):
            st.session_state.step_sub8 = "test"
            if "sub8" not in st.session_state.start_times: st.session_state.start_times["sub8"] = time.time()
            save_state_disk(email)
            st.rerun()

    elif st.session_state.step_sub8 == "test":
        st.title("🧠 Subtes 8")
        if "sub8" not in st.session_state.start_times: st.session_state.start_times["sub8"] = time.time()
        elapsed = int(time.time() - st.session_state.start_times["sub8"])
        remaining = max(0, 540 - elapsed) # 9 menit

        if remaining <= 0:
            st.session_state.page = "result"
            st.query_params["page"] = "result"
            save_state_disk(email)
            time.sleep(0.3)
            st.rerun()

        # next_sub=9 otomatis mengarahkan ke page=result
        render_timer(remaining, email, 8, 9)

        img_s = "subtest_8_soal.png" if os.path.exists("subtest_8_soal.png") else "images/subtest_8_soal.png"
        if os.path.exists(img_s): st.image(img_s, caption="Soal Subtes 8 (No. 137 - 156)", use_container_width=True)

        opts = ["a", "b", "c", "d", "e"]
        for q_num in range(137, 157):
            curr_val = st.session_state.answers.get(q_num, None)
            idx = opts.index(curr_val) if curr_val in opts else None
            ans = st.radio(f"Soal No. {q_num}:", options=opts, index=idx, horizontal=True, key=f"q_{q_num}")
            st.session_state.answers[q_num] = ans

        save_state_disk(email)
        st.markdown("---")
        if st.button("Simpan & Selesaikan Ujian 🏁", type="primary"):
            st.session_state.page = "result"
            st.query_params["page"] = "result"
            save_state_disk(email)
            st.rerun()
