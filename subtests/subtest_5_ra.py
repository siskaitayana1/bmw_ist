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
        "current_subtest": 5,
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
        ⏱️ SISA WAKTU SUBTES 5: <span id="timer_display">--:--</span>
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
                var newSearch = "?page=test&subtest=6&email={safe_email}";
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

def render_subtest_5_ra():
    st.title("🧠 Subtes 5 (Hitungan Aritmatika)")
    
    with st.expander("📌 **Petunjuk & Contoh Pengerjaan (Klik untuk membaca)**", expanded=True):
        st.markdown("""
        **Petunjuk**: Selesaikan persoalan hitungan di bawah ini dan ketikkan angka jawaban Anda pada kolom yang disediakan.
        
        * **Contoh 01**: Sebatang pensil harganya 25 rupiah. Berapakah harga 3 batang?  
          *Jawaban*: **75**
          
        * **Contoh 02**: Dengan sepeda Husin dapat mencapai 15 km dalam waktu 1 jam. Berapa km-kah yang dapat ia capai dalam waktu 4 jam?  
          *Jawaban*: **60**
        """)

    email = st.session_state.get("user_info", {}).get("email", "")
    if "sub5" not in st.session_state.start_times:
        st.session_state.start_times["sub5"] = time.time()

    elapsed = int(time.time() - st.session_state.start_times["sub5"])
    remaining = max(0, 600 - elapsed) # 10 menit

    if remaining <= 0:
        st.session_state.current_subtest = 6
        st.query_params["subtest"] = "6"
        save_state_disk(email)
        time.sleep(0.3)
        st.rerun()

    show_live_timer(remaining, email)

    questions = [
        (77, "Jika seorang anak memiliki 50 rupiah dan memberikan 15 rupiah kepada orang lain, berapa rupiahkah yang masih tinggal padanya?"),
        (78, "Berapa km-kah yang dapat ditempuh oleh kereta api dalam waktu 7 jam, jika kecepatannya 40 km/jam?"),
        (79, "15 peti buah-buahan beratnya 250 kg dan setiap peti kosong beratnya 3 kg, berapakah berat buah-buahan itu?"),
        (80, "Seseorang mempunyai persediaan rumput yang cukup untuk 7 ekor kuda selama 78 hari. Berapa harikah persediaan itu cukup untuk 21 ekor kuda?"),
        (81, "3 batang coklat harganya Rp 5,- Berapa batangkah yang dapat kita beli dengan Rp 50,-?"),
        (82, "Seseorang dapat berjalan 1,75 m dalam waktu ¼ detik. Berapakah meterkah yang dapat ia tempuh dalam waktu 10 detik?"),
        (83, "Jika sebuah batu terletak 15 m di sebelah selatan dari sebatang pohon dan pohon itu berada 30 m di sebelah selatan dari sebuah rumah, berapa meterkah jarak antara batu dan rumah itu?"),
        (84, "Jika 4 ½ m bahan sandang harganya Rp 90,- berapakah rupiahkah harganya 2 ½ m?"),
        (85, "7 orang dapat menyelesaikan sesuatu pekerjaan dalam 6 hari. Berapa orangkah yang diperlukan untuk menyelesaikan pekerjaan itu dalam setengah hari?"),
        (86, "Karena dipanaskan, kawat yang panjangnya 48 cm akan mengembang menjadi 52 cm. Setelah pemanasan, berapakah panjangnya kawat yang berukuran 72 cm?"),
        (87, "Suatu pabrik dapat menghasilkan 304 batang pensil dalam waktu 8 jam. Berapa batangkah dihasilkan dalam waktu setengah jam?"),
        (88, "Untuk suatu campuran diperlukan 2 bagian perak dan 3 bagian timah. Berapa gramkah perak yang diperlukan untuk mendapatkan campuran itu yang beratnya 15 gram?"),
        (89, "Untuk setiap Rp 3,- yang dimiliki Sidin, Hamid memiliki Rp 5,- Jika mereka bersama mempunyai Rp 120,- berapa rupiahkah yang dimiliki Hamid?"),
        (90, "Mesin A menenun 60 m kain, sedangkan mesin B menenun 40 m. Berapa meterkah yang ditenun mesin A, jika mesin B menenun 60 m?"),
        (91, "Seseorang membelikan 1/10 dari uangnya untuk perangko dan 4 kali jumlah itu untuk alat tulis. Sisa uangnya masih Rp 60,- Berapa rupiahkah uang semula?"),
        (92, "Di dalam dua peti terdapat 43 piring. Di dalam peti yang satu terdapat 9 piring lebih banyak dari pada di dalam peti yang lain. Berapa buah piring terdapat di dalam peti yang lebih kecil?"),
        (93, "Suatu lembaran kain yang panjangnya 60 cm harus dibagikan sedemikian rupa sehingga panjangnya satu bagian ialah 2/3 dari bagian yang lain. Berapa panjangnya bagian yang terpendek?"),
        (94, "Suatu perusahaan mengekspor ¾ dari hasil produksinya dan menjual 4/5 dari sisa itu dalam negeri. Berapa % kah hasil produksi yang masih tinggal?"),
        (95, "Jika suatu botol berisi anggur hanya 7/8 bagian dan harganya ialah Rp 84,- berapakah harga anggur itu jika botol itu hanya terisi ½ penuh?"),
        (96, "Di dalam suatu keluarga setiap anak perempuan mempunyai jumlah saudara laki-laki yang sama dengan jumlah saudara perempuan dan setiap anak laki-laki mempunyai dua kali lebih banyak saudara perempuan dari pada saudara laki-laki. Berapa anak laki-lakikah yang terdapat di dalam keluarga tersebut?")
    ]

    for q_id, q_text in questions:
        curr_val = st.session_state.answers.get(q_id, "")
        ans = st.text_input(f"**Soal No. {q_id}:** {q_text}", value=curr_val if curr_val else "", key=f"q_{q_id}")
        st.session_state.answers[q_id] = ans.strip() if ans else None

    save_state_disk(email)
    st.markdown("---")
    if st.button("Simpan & Lanjut ke Subtes 6 ➔", type="primary"):
        st.session_state.current_subtest = 6
        st.query_params["subtest"] = "6"
        save_state_disk(email)
        st.rerun()
