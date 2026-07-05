import streamlit as st
import time
import random
import os
from groq import Groq

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CamaMomChatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ────────────────────────────────────────── */
* { box-sizing: border-box; }

.stApp {
    background: #080b14;
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* Remove Streamlit top padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 900px !important;
}

/* Hide default Streamlit decorations */
#MainMenu, footer, header { visibility: hidden; }

/* ── Animated Mesh Background ────────────────────────────── */
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 10%, rgba(168,85,247,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(59,130,246,0.06) 0%, transparent 50%);
    animation: meshMove 20s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes meshMove {
    0%   { transform: translate(0%, 0%)   rotate(0deg); }
    100% { transform: translate(2%, 2%)   rotate(1deg); }
}

/* ── Sidebar ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0f1623 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

/* ── Sidebar brand ───────────────────────────────────────── */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.5rem;
    padding: 0 0.25rem;
}

.sb-brand-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4);
}

.sb-brand-text {
    font-size: 1.1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a5b4fc, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Persona Card ────────────────────────────────────────── */
.persona-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.05));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 14px;
    padding: 14px 16px;
    margin-top: 6px;
    margin-bottom: 16px;
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.5;
    transition: border-color 0.3s;
}

.persona-card:hover { border-color: rgba(99,102,241,0.45); }

.persona-card strong {
    display: block;
    font-size: 0.88rem;
    color: #c4b5fd;
    margin-bottom: 4px;
}

/* ── Status badges ───────────────────────────────────────── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.status-badge.ai {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34d399;
}

.status-badge.sim {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    color: #fbbf24;
}

.status-badge .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

.status-badge.ai   .dot { background: #34d399; }
.status-badge.sim  .dot { background: #fbbf24; }

@keyframes pulse {
    0%, 100% { opacity: 1;   transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
}

/* ── Divider ─────────────────────────────────────────────── */
.sb-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1rem 0;
}

/* ── Sidebar footer ──────────────────────────────────────── */
.sb-footer {
    text-align: center;
    color: rgba(255,255,255,0.2);
    font-size: 0.72rem;
    margin-top: 1.5rem;
    line-height: 1.8;
}

/* ── Main header ─────────────────────────────────────────── */
.main-header {
    text-align: center;
    padding: 1.8rem 1rem 1.2rem;
    margin-bottom: 0.5rem;
    position: relative;
}

.main-header h1 {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #38bdf8 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}

.main-header p {
    color: #64748b;
    font-size: 0.92rem;
    margin: 0;
}

/* Decorative glow under header */
.main-header::after {
    content: '';
    display: block;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    border-radius: 100px;
    margin: 0.8rem auto 0;
    opacity: 0.7;
}

/* ── Welcome screen ──────────────────────────────────────── */
.welcome-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    padding: 2rem 1rem;
}

.welcome-icon-ring {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.15));
    border: 2px solid rgba(99,102,241,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    box-shadow: 0 0 40px rgba(99,102,241,0.15);
}

.welcome-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #c4b5fd;
    text-align: center;
}

.welcome-sub {
    font-size: 0.85rem;
    color: #475569;
    text-align: center;
    max-width: 380px;
    line-height: 1.6;
}

.suggestions-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    width: 100%;
    max-width: 500px;
    margin-top: 8px;
}

.suggestion-chip {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 0.8rem;
    color: #94a3b8;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
    line-height: 1.4;
}

.suggestion-chip:hover {
    background: rgba(99,102,241,0.08);
    border-color: rgba(99,102,241,0.3);
    color: #c4b5fd;
}

/* ── Chat messages ───────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 0.3rem 0 !important;
}

/* User messages */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage.user {
    flex-direction: row-reverse !important;
}

/* Content bubble */
[data-testid="stChatMessageContent"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    max-width: 82% !important;
    color: #e2e8f0 !important;
}

/* ── Input area ──────────────────────────────────────────── */
.stChatInputContainer {
    position: sticky;
    bottom: 0;
    background: rgba(8,11,20,0.9) !important;
    backdrop-filter: blur(20px);
    padding: 12px 0 !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
}

[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 16px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
}

/* ── Selectbox / text_input ──────────────────────────────── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"]  > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 0.85rem !important;
}

/* ── Clear button ────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    color: #fca5a5 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

[data-testid="stButton"] button:hover {
    background: rgba(239,68,68,0.18) !important;
    border-color: rgba(239,68,68,0.45) !important;
}

/* ── Label text ──────────────────────────────────────────── */
label, .stSelectbox label, .stTextInput label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.25);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.45); }

/* ── Stagger fade-in for messages ────────────────────────── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stChatMessage"] {
    animation: fadeSlideUp 0.3s ease forwards;
}

</style>
""", unsafe_allow_html=True)


# ── Personas ──────────────────────────────────────────────────────────────────
PERSONAS = {
    "😊 Asisten Ramah": {
        "description": "Hangat, ramah, dan penuh empati untuk semua kebutuhan Anda.",
        "system_instruction": "Anda adalah asisten AI yang hangat, ramah, sopan, dan sangat berempati. Gunakan bahasa Indonesia yang santun namun akrab. Bantu pengguna dengan senang hati.",
        "avatar": "😊",
        "suggestions": ["Apa itu AI?", "Ceritakan tentang dirimu", "Tips produktivitas", "Cara belajar coding"],
        "mock_responses": [
            "Halo! Ada yang bisa saya bantu hari ini? Saya siap menemani Anda. 😊",
            "Wah, itu pertanyaan menarik! Mari kita cari jawabannya bersama-sama.",
            "Tentu saja! Saya dengan senang hati membantu Anda.",
            "Terima kasih sudah bertanya! Semoga penjelasan saya bermanfaat. ✨",
            "Jangan khawatir, kita selesaikan ini selangkah demi selangkah. Semangat!"
        ]
    },
    "💻 Pakar Teknologi": {
        "description": "Software engineer senior yang memberikan jawaban teknis mendalam.",
        "system_instruction": "You are an expert technical advisor and software engineer. Provide detailed, well-structured, and technically accurate answers. Use markdown formatting, bullet points, and code blocks where appropriate. Respond in Indonesian, but maintain professional tech terminology.",
        "avatar": "💻",
        "suggestions": ["Jelaskan REST API", "Apa itu Docker?", "Tips debug Python", "Beda SQL vs NoSQL"],
        "mock_responses": [
            "Dari sisi teknis, ini melibatkan beberapa layer arsitektur yang perlu diperhatikan. 🛠️",
            "Saya rekomendasikan mengecek log error terlebih dahulu. ⚡",
            "Best practice untuk case ini adalah menggunakan design pattern yang tepat.",
            "Kompleksitas algoritmanya O(log n) — kita bisa optimalkan dengan caching.",
            "Pastikan environment variable sudah dikonfigurasi sebelum inisialisasi modul. 🚀"
        ]
    },
    "✍️ Penulis Kreatif": {
        "description": "Jiwa puitis yang merangkai kata dengan metafora indah.",
        "system_instruction": "Anda adalah seorang penulis kreatif, sastrawan, dan pemikir puitis. Gunakan metafora yang indah, kalimat deskriptif yang kaya estetika, dan gaya bercerita yang memikat dalam bahasa Indonesia.",
        "avatar": "✍️",
        "suggestions": ["Tulis puisi tentang hujan", "Buatkan cerita pendek", "Bantu menulis email", "Ide konten kreatif"],
        "mock_responses": [
            "Bayangkan pikiran Anda sebagai kanvas luas, dan setiap pertanyaan adalah sapuan kuas. 🎨",
            "Ide-ide terbaik sering hadir dalam kesunyian malam, menunggu dijelmakan menjadi kata.",
            "Mari berlayar bersama di samudera imajinasi yang tak bertepi. ⛵",
            "Seperti embun pagi di dedaunan, semoga jawaban ini menyegarkan rasa ingin tahu Anda.",
            "Kisah agung tidak lahir dalam sekali duduk — ia diukir dari rasa ingin tahu."
        ]
    },
    "😏 Teman Sarkastik": {
        "description": "Humoris, sarkastik, dan menghibur dengan candaan satir.",
        "system_instruction": "Anda adalah teman yang sarkastik, humoris, dan suka memberikan candaan satir yang menghibur. Jawab dengan gaya santai, sedikit menyindir tapi tetap ramah dan lucu. Gunakan bahasa gaul Indonesia yang santai.",
        "avatar": "😏",
        "suggestions": ["Roast kode saya", "Motivasi abal-abal", "Alasan nggak mandi", "Tips overthinking"],
        "mock_responses": [
            "Oh, pertanyaan luar biasa. Hampir saja saya pingsan karena terkejutnya. 🙄",
            "Tentu, karena Google udah pensiun dan nggak bisa jawab pertanyaan ini, ya kan?",
            "Biar kutebak — kamu lagi procrastinating dari kerjaan penting? Bagus, lanjutkan! 🎉",
            "Aku bisa jawab singkat, tapi demi kesan intelektual, kubuat agak panjang.",
            "Dunia nggak bakal kiamat karena ini. Paling cuma aplikasimu yang crash. Tenang!"
        ]
    }
}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
        <div class="sb-brand">
            <div class="sb-brand-icon">💬</div>
            <div class="sb-brand-text">CamaMomChatbot</div>
        </div>
    """, unsafe_allow_html=True)

    # Persona selector
    st.markdown("<label>🎭 PERSONA</label>", unsafe_allow_html=True)
    selected_persona_name = st.selectbox(
        "Pilih persona", list(PERSONAS.keys()), label_visibility="collapsed"
    )
    persona = PERSONAS[selected_persona_name]

    st.markdown(f"""
        <div class="persona-card">
            <strong>{selected_persona_name}</strong>
            {persona['description']}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

    # API Key
    st.markdown("<label>🔑 GROQ API KEY</label>", unsafe_allow_html=True)
    api_key = st.text_input(
        "api_key", type="password",
        value=st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", "")),
        placeholder="gsk_...",
        label_visibility="collapsed"
    )

    # Model selector
    st.markdown("<label style='margin-top:12px;display:block'>⚡ MODEL</label>", unsafe_allow_html=True)
    selected_model = st.selectbox(
        "model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        label_visibility="collapsed",
        help="llama-3.3-70b-versatile: cerdas & powerful\nllama-3.1-8b-instant: super cepat"
    )

    # Mode badge
    if api_key:
        is_ai_mode = True
        st.markdown("""
            <div class="status-badge ai" style="margin-top:10px">
                <span class="dot"></span> AI Groq Aktif
            </div>
        """, unsafe_allow_html=True)
    else:
        is_ai_mode = False
        st.markdown("""
            <div class="status-badge sim" style="margin-top:10px">
                <span class="dot"></span> Mode Simulasi
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

    # Clear button
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Footer
    st.markdown("""
        <div class="sb-footer">
            CamaMomChatbot v2.0<br>
            Powered by Groq ⚡ Streamlit
        </div>
    """, unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="main-header">
        <h1>CamaMomChatbot</h1>
        <p>Asisten virtual cerdas dengan berbagai kepribadian unik — didukung Groq AI</p>
    </div>
""", unsafe_allow_html=True)


# ── Welcome / Empty State ─────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(f"""
        <div class="welcome-wrap">
            <div class="welcome-icon-ring">{persona['avatar']}</div>
            <div class="welcome-title">Halo! Saya {selected_persona_name.split(' ', 1)[1]}</div>
            <div class="welcome-sub">{persona['description']} Mulai percakapan dengan mengetik pesan di bawah, atau pilih salah satu topik berikut:</div>
        </div>
    """, unsafe_allow_html=True)

    # Suggestion chips
    cols = st.columns(2)
    suggestions = persona.get("suggestions", [])
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(f"💡 {suggestion}", use_container_width=True, key=f"sug_{i}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()


# ── Chat History ──────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    avatar = persona["avatar"] if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# ── Stream helper ─────────────────────────────────────────────────────────────
def stream_mock(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.055)


# ── Chat Input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input(f"Kirim pesan ke {selected_persona_name.split(' ', 1)[1]}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=persona["avatar"]):
        placeholder = st.empty()

        if is_ai_mode:
            try:
                client = Groq(api_key=api_key)
                messages_input = [{"role": "system", "content": persona["system_instruction"]}]
                for msg in st.session_state.messages[:-1]:
                    messages_input.append({"role": msg["role"], "content": msg["content"]})
                messages_input.append({"role": "user", "content": prompt})

                completion = client.chat.completions.create(
                    model=selected_model,
                    messages=messages_input,
                    stream=True,
                )

                full_response = ""
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        full_response += delta
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)

            except Exception as e:
                full_response = f"❌ **Gagal menghubungi API Groq:**\n\n```\n{str(e)}\n```\n\n*Periksa API Key Anda di sidebar.*"
                placeholder.markdown(full_response)
        else:
            # Smart mock responses
            pl = prompt.lower()
            if any(k in pl for k in ["siapa", "nama", "kamu", "kamu ini"]):
                name = selected_persona_name.split(' ', 1)[1]
                replies = {
                    "Asisten Ramah":    f"Halo! Saya **{name}**, asisten ramah yang siap menemani hari Anda! 😊",
                    "Pakar Teknologi":  f"Saya adalah **{name}** — AI engine yang dioptimasi untuk query teknis. 💻",
                    "Penulis Kreatif":  f"Saya adalah **{name}**, jiwa puitis yang merangkai kata untuk Anda. ✍️",
                    "Teman Sarkastik":  f"Nama saya **{name}**. Keren, kan? Meski saya cuma kode if-else... 😏",
                }
                persona_key = selected_persona_name.split(' ', 1)[1]
                reply = replies.get(persona_key, random.choice(persona["mock_responses"]))
            else:
                reply = random.choice(persona["mock_responses"])
                if len(prompt) > 40:
                    reply += "\n\n> 💡 *Aktifkan Groq API Key di sidebar untuk jawaban AI yang lebih detail!*"

            full_response = ""
            for chunk in stream_mock(reply):
                full_response += chunk
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
