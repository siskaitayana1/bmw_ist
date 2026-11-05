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
        "current_subtest": 4,
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
        ⏱️ SISA WAKTU SUBTES 4: <span id="timer_display">--:--</span>
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
                var targetUrl = window.top.location.pathname + "?page=test&subtest=5&email={safe_email}";
                setTimeout(function() {{ window.top.location.href = targetUrl; }}, 500);
            }} else {{ timeLeft--; }}
        }}
        updateDisplay(); setInterval(updateDisplay, 1000);
    </script>
    """, height=75)

def render_subtest_4_ge():
    st.title("🧠 Subtes 4 (Sifat Bersama / Kesamaan Kata)")
    st.info("Ketikkan satu kata umum yang mencakup sifat/kategori dari kedua kata tersebut.")
    
    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub4" not in st.session_state.start_times:
        st.session_state.start_times["sub4"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub4"])
    remaining = max(0, 480 - elapsed) # 8 menit

    if remaining <= 0:
        st.session_state.current_subtest = 5
        st.query_params["subtest"] = "5"
        save_state_disk(email)
        time.sleep(0.5)
        st.rerun()

    show_live_timer(remaining, email)

    for q_id in range(61, 77):
        curr_val = st.session_state.answers.get(q_id, "")
        ans = st.text_input(f"**Soal No. {q_id}:** Sebutkan kesamaan kategori kata pada nomor {q_id}:", value=curr_val if curr_val else "", key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans.strip() if ans else None

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 5 ➔", type="primary"):
        st.session_state.current_subtest = 5
        st.query_params["subtest"] = "5"
        save_state_disk(email)
        st.rerun()
