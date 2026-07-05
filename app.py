import streamlit as st
import time
import random
import os
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="CamaMomChatbot - Premium Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Glassmorphism CSS styling for premium look
custom_css = """
<style>
/* Base theme overrides */
.stApp {
    background: linear-gradient(135deg, #0e1117 0%, #161a24 100%);
    color: #e2e8f0;
    font-family: 'Outfit', 'Inter', sans-serif;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: rgba(22, 26, 36, 0.9) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
}

/* Custom card container for UI */
.premium-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    backdrop-filter: blur(5px);
}

/* Input fields styling */
div[data-baseweb="input"] {
    background-color: rgba(14, 17, 23, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

/* Chat Input Bar styling */
div[data-testid="stChatInput"] {
    border-radius: 12px !important;
    background-color: rgba(22, 26, 36, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px);
}

/* Title and typography */
h1 {
    font-weight: 800 !important;
    background: linear-gradient(90deg, #38bdf8 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

/* Mode badge */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 10px;
}
.badge-simulated {
    background-color: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
}
.badge-ai {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Persona Configurations
PERSONAS = {
    "😊 Asisten Ramah": {
        "description": "Asisten yang hangat, ramah, dan siap membantu segala kebutuhan Anda dengan penuh empati.",
        "system_instruction": "Anda adalah asisten AI yang hangat, ramah, sopan, dan sangat berempati. Gunakan bahasa Indonesia yang santun namun akrab. Bantu pengguna dengan senang hati.",
        "avatar": "😊",
        "mock_responses": [
            "Halo! Ada yang bisa saya bantu hari ini? Saya senang sekali bisa menemani Anda. 😊",
            "Wah, itu pertanyaan yang menarik sekali! Mari kita cari solusinya bersama-sama.",
            "Tentu saja, saya siap membantu Anda menyelesaikan hal itu. Apa lagi yang ingin Anda ketahui?",
            "Terima kasih sudah bertanya! Semoga penjelasan saya cukup membantu ya. Jika ada hal lain, tanyakan saja. ✨",
            "Jangan khawatir, kita bisa selesaikan ini selangkah demi selangkah. Tetap semangat!"
        ]
    },
    "💻 Pakar Teknologi": {
        "description": "Insinyur perangkat lunak senior yang memberikan jawaban teknis, terstruktur, mendalam, dan menggunakan sintaks kode.",
        "system_instruction": "You are an expert technical advisor and software engineer. Provide detailed, well-structured, and technically accurate answers. Use markdown formatting, bullet points, and code blocks where appropriate. Respond in Indonesian, but maintain professional tech terminology.",
        "avatar": "💻",
        "mock_responses": [
            "Mari kita analisis secara teknis. 🛠️ Masalah ini biasanya terjadi karena konflik dependensi atau kesalahan konfigurasi runtime.",
            "Berdasarkan best practice arsitektur modern, solusi optimal untuk case ini melibatkan optimasi algoritma runtime. Berikut kodenya:\n```python\n# Contoh implementasi optimis\ndef optimize_process(data):\n    return [item for item in data if item.is_valid()]\n```",
            "Saya sarankan untuk memeriksa log debugging terlebih dahulu. ⚡ Apakah Anda melihat error code tertentu pada terminal?",
            "Langkah integrasi ini sangat mudah. Pastikan environment variables sudah di-set dengan benar sebelum inisialisasi modul. 🚀",
            "Secara umum, efisiensi waktu operasi ini adalah O(log n). Kita bisa memangkas kompleksitas dengan menambahkan caching layer."
        ]
    },
    "✍️ Penulis Kreatif": {
        "description": "Pribadi puitis yang menggunakan metafora indah, deskripsi kaya, dan gaya penulisan naratif.",
        "system_instruction": "Anda adalah seorang penulis kreatif, sastrawan, dan pemikir puitis. Gunakan metafora yang indah, kalimat deskriptif yang kaya estetika, dan gaya bercerita yang memikat dalam bahasa Indonesia.",
        "avatar": "✍️",
        "mock_responses": [
            "Bayangkan pikiran Anda bagaikan kanvas kosong yang luas, dan setiap pertanyaan adalah goresan kuas warna-warni yang siap melukis keindahan. 🎨",
            "Ide-ide cemerlang sering kali berbisik pelan di sela-sela kesunyian malam, menanti jemari Anda menuliskannya menjadi barisan kalimat yang abadi.",
            "Mari kita jelajahi samudera imajinasi ini bersama-sama, berlayar melintasi ombak kata-kata untuk menemukan pulau kreativitas baru. ⛵",
            "Seperti embun pagi yang membasahi dedaunan, semoga jawaban sederhana ini bisa memberikan kesegaran bagi dahaga penasaran Anda.",
            "Kisah terbaik tidak ditulis dalam sekali duduk; ia diukir dari rasa ingin tahu yang tak pernah padam."
        ]
    },
    "😏 Teman Sarkastik": {
        "description": "Teman yang sarkastik, penuh candaan satir, sedikit malas, tetapi aslinya humoris dan menghibur.",
        "system_instruction": "Anda adalah teman yang sarkastik, humoris, dan suka memberikan candaan satir yang menghibur. Jawab dengan gaya santai, sedikit menyindir tapi tetap ramah dan lucu. Gunakan bahasa gaul Indonesia yang santai.",
        "avatar": "😏",
        "mock_responses": [
            "Oh, sebuah pertanyaan luar biasa lagi. Hampir saja saya pingsan karena kagum. Tapi baiklah, mari kita bahas... 🙄",
            "Tentu, karena membaca dokumentasi resmi atau mencarinya di Google itu terlalu mainstream untuk Anda, kan? Biar saya jelaskan saja.",
            "Biar saya tebak: Anda sedang menunda pekerjaan penting dengan menanyakan hal ini kepada saya? Bagus sekali, mari kita lanjutkan penundaan ini! 🎉",
            "Saya bisa saja menjawabnya dalam satu kalimat, tapi demi terlihat pintar, saya akan buat jawabannya sedikit lebih panjang.",
            "Tenang, dunia tidak akan kiamat hanya karena masalah sepele ini. Paling-paling cuma aplikasi Anda yang error. Bercanda!"
        ]
    }
}

# Sidebar Content
with st.sidebar:
    st.markdown("## ✨ CamaMomChatbot Panel")
    st.markdown("Konfigurasi chatbot Anda di bawah ini:")

    # Persona Selection
    selected_persona_name = st.selectbox(
        "Pilih Persona Chatbot:",
        list(PERSONAS.keys()),
        index=0
    )
    persona = PERSONAS[selected_persona_name]
    
    # Show description of current persona
    st.markdown(f"<div class='premium-card'><strong>{selected_persona_name}</strong><br><small>{persona['description']}</small></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔌 API Integrasi (Groq)")
    st.markdown("Masukkan Groq API Key Anda untuk mengaktifkan AI asli:")
    
    api_key = st.text_input(
        "Groq API Key:",
        type="password",
        value=st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", "")),
        placeholder="gsk_...",
        help="Kosongkan untuk tetap menggunakan mode simulasi cerdas."
    )

    selected_model = st.selectbox(
        "Pilih Model Groq:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        index=0,
        help="llama-3.3-70b-versatile cocok untuk tugas kompleks. llama-3.1-8b-instant sangat cepat."
    )
    
    # Active Mode Check
    if api_key:
        is_ai_mode = True
        st.markdown("<span class='badge badge-ai'>⚡ Mode: AI Groq Aktif</span>", unsafe_allow_html=True)
    else:
        is_ai_mode = False
        st.markdown("<span class='badge badge-simulated'>🧪 Mode: Simulasi Aktif</span>", unsafe_allow_html=True)
        
    st.markdown("---")
    # Action buttons
    if st.button("🔄 Bersihkan Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Footer
    st.markdown("<br><br><div style='text-align: center; color: rgba(255,255,255,0.3); font-size: 0.8rem;'>CamaMomChatbot v1.1.0 (Groq)<br>Made with 💖 using Streamlit</div>", unsafe_allow_html=True)

# Main Application Layout
st.markdown("<h1>✨ CamaMomChatbot (Groq Edition)</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; margin-top: -10px;'>Asisten virtual cerdas didukung oleh model Llama 3 super cepat dari Groq.</p>", unsafe_allow_html=True)

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat Messages
for message in st.session_state.messages:
    # Use selected avatar based on sender
    avatar = persona["avatar"] if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Function to simulate typing / streaming output (for mock mode)
def stream_response(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.06)

# User Chat Input
if prompt := st.chat_input("Tulis sesuatu ke chatbot..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Render User Message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # Generate and Render Assistant Message
    with st.chat_message("assistant", avatar=persona["avatar"]):
        response_placeholder = st.empty()
        
        if is_ai_mode:
            try:
                # Initialize Groq client
                client = Groq(api_key=api_key)
                
                # Format conversation history for Groq completions
                messages_input = [
                    {"role": "system", "content": persona["system_instruction"]}
                ]
                
                # Add historical messages (excluding the last one which is already sent below)
                for msg in st.session_state.messages[:-1]:
                    messages_input.append({"role": msg["role"], "content": msg["content"]})
                    
                # Add current message
                messages_input.append({"role": "user", "content": prompt})
                
                # Call Groq completions with streaming enabled
                completion = client.chat.completions.create(
                    model=selected_model,
                    messages=messages_input,
                    stream=True,
                )
                
                # Display stream in real-time
                full_response = ""
                for chunk in completion:
                    content = chunk.choices[0].delta.content
                    if content is not None:
                        full_response += content
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                error_msg = f"❌ **Terjadi kesalahan saat menghubungi API Groq:** {str(e)}\n\n*Catatan: Pastikan API Key Anda valid.*"
                response_placeholder.markdown(error_msg)
                full_response = error_msg
        else:
            # Simulated Mode: Pick a random reply or customize based on prompt keywords
            prompt_lower = prompt.lower()
            if any(x in prompt_lower for x in ["siapa", "nama", "kamu"]):
                if "Asisten Ramah" in selected_persona_name:
                    reply = "Saya adalah CamaMomChatbot, asisten ramah Anda! Saya di sini untuk menemani hari Anda. 😊"
                elif "Pakar Teknologi" in selected_persona_name:
                    reply = "Sistem mengidentifikasi saya sebagai CamaMomChatbot Core Engine v1.1. Saya dioptimasi untuk penanganan query teknis. 💻"
                elif "Penulis Kreatif" in selected_persona_name:
                    reply = "Saya adalah bayangan pena Anda, CamaMomChatbot, jiwa puitis yang siap merangkai cerita bersama Anda. ✍️"
                else: # Sarcastic
                    reply = "Nama saya CamaMomChatbot. Keren kan? Meskipun sejujurnya saya cuma sekumpulan kode if-else yang bosan. 😏"
            elif any(x in prompt_lower for x in ["halo", "hi", "hey", "pagi", "siang", "sore", "malam"]):
                reply = random.choice(persona["mock_responses"])
            else:
                reply = random.choice(persona["mock_responses"])
                if len(prompt) > 30:
                    reply += f"\n\n*(Catatan dari {selected_persona_name}: Anda menulis kalimat yang cukup panjang. Untuk mendapatkan jawaban detail dan nyata dari AI, pastikan Groq API Key Anda aktif di sidebar!)*"
            
            # Stream the response simulation
            full_response = ""
            for chunk in stream_response(reply):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            
        # Add Assistant Response to History
        st.session_state.messages.append({"role": "assistant", "content": full_response})
