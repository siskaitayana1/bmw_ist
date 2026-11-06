import streamlit.components.v1 as components

def show_live_timer(seconds_remaining, email, current_subtest, next_subtest):
    safe_email = email.replace("'", "\\'") if email else ""
    target_param = f"?page=result&email={safe_email}" if next_subtest >= 9 else f"?page=test&subtest={next_subtest}&email={safe_email}"
    
    components.html(f"""
    <div style="font-family: Arial; font-size: 18px; font-weight: bold; color: #dc2626; 
                background-color: #fef2f2; padding: 10px; border: 2px solid #dc2626; border-radius: 8px; text-align: center;">
        ⏱️ SISA WAKTU SUBTES {current_subtest}: <span id="timer_display">--:--</span>
    </div>
    <script>
        var timeLeft = {seconds_remaining};
        var targetParam = "{target_param}";
        var redirected = false;

        function doRedirect() {{
            if (redirected) return;
            redirected = true;
            var path = window.top.location.pathname;
            try {{ window.top.location.href = path + targetParam; }} catch(e) {{}}
            try {{ window.parent.location.href = path + targetParam; }} catch(e) {{}}
            try {{ window.location.href = path + targetParam; }} catch(e) {{}}
        }}

        function updateTimer() {{
            var m = Math.floor(timeLeft / 60);
            var s = timeLeft % 60;
            var display = (m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s);
            var elem = document.getElementById("timer_display");
            if (elem) {{ elem.innerHTML = display; }}
            if (timeLeft <= 0) {{
                if (elem) elem.innerHTML = "00:00 (WAKTU HABIS)";
                doRedirect();
            }} else {{
                timeLeft--;
            }}
        }}
        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
    """, height=70)
