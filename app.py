import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from groq import Groq
import httpx 
import requests
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VoiceQL",layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .main .block-container {
        background-color: #CAF0F8;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stApp {
        background-color: #CAF0F8;
    }
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    html { 
        scroll-behavior: smooth; 
    }
    
    h1 {
        background: linear-gradient(135deg, #023E8A 0%, #0077B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 4rem !important;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-weight: 700;
        color: #023E8A;
        letter-spacing: -0.01em;
    }
    
    h3 {
        font-weight: 600;
        color: #023E8A;
    }
    
    body, p, div, span, label {
        color: #023E8A !important;
    }
    
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span,
    .element-container p,
    .element-container div,
    .element-container span {
        color: #023E8A !important;
    }
    
    label,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label {
        color: #023E8A !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        color: #023E8A !important;
    }
    
    .stButton > button {
        color: white !important;
    }
    
    .stInfo,
    .stInfo p,
    .stInfo div {
        color: #023E8A !important;
    }
    
    .stSuccess p,
    .stSuccess div,
    .stError p,
    .stError div,
    .stWarning p,
    .stWarning div {
        color: #023E8A !important;
    }
    
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    h1 .header-anchor,
    h2 .header-anchor,
    h3 .header-anchor,
    h1 a[href^="#"],
    h2 a[href^="#"],
    h3 a[href^="#"],
    h1 a[href*="#"],
    h2 a[href*="#"],
    h3 a[href*="#"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    h1:hover a, h2:hover a, h3:hover a {
        display: none !important;
        visibility: hidden !important;
    }
    
    .nav-btn {
        display: inline-block;
        background: #0077B6;
        color: white !important;
        padding: 14px 32px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        box-shadow: 0 4px 15px rgba(2, 62, 138, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .nav-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(2, 62, 138, 0.4);
        background: #023E8A;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid #90E0EF;
        box-shadow: 0 8px 32px rgba(144, 224, 239, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 119, 182, 0.2);
        border-color: #0077B6;
    }
    
    .feature-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 35px 30px;
        border: 2px solid #90E0EF;
        box-shadow: 0 4px 12px rgba(144, 224, 239, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        margin: 0;
        display: block;
    }
    
    .feature-card h3 {
        margin-top: 0 !important;
        margin-bottom: 15px !important;
        font-size: 1.5rem !important;
        color: #023E8A !important;
    }
    
    .feature-card p {
        margin-bottom: 0 !important;
        color: #023E8A !important;
        line-height: 1.6 !important;
        font-size: 1rem !important;
    }
    
    .feature-card strong {
        color: #0077B6 !important;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 28px rgba(144, 224, 239, 0.5);
        border-color: #0077B6;
        background: #ffffff;
    }
    
    div[data-testid="column"] .feature-card {
        width: 100%;
        box-sizing: border-box;
    }
    
    div[data-testid="column"] > div {
        width: 100%;
    }
    
    .feature-card-container {
        padding: 0;
        margin: 0;
    }
    
    .section-divider {
        margin: 60px 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #90E0EF, transparent);
        border: none;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #90E0EF !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        background-color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0077B6 !important;
        box-shadow: 0 0 0 3px rgba(0, 119, 182, 0.1) !important;
    }
    
    .stButton > button {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        background-color: #0077B6 !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        background-color: #023E8A !important;
        color: white !important;
    }
    
    button[data-baseweb="button"][kind="primary"],
    button[data-baseweb="button"][kind="primary"]:focus,
    button[data-baseweb="button"][kind="primary"]:active {
        background-color: #0077B6 !important;
        color: white !important;
        border: none !important;
    }
    
    button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #023E8A !important;
        color: white !important;
    }
    
    .stForm button[data-baseweb="button"][kind="primary"],
    .stForm button[data-baseweb="button"][kind="primary"]:focus,
    .stForm button[data-baseweb="button"][kind="primary"]:active,
    .stForm [data-testid="stFormSubmitButton"] button,
    .stForm [data-testid="stFormSubmitButton"] button:focus,
    .stForm [data-testid="stFormSubmitButton"] button:active,
    div[data-testid="stForm"] button[data-baseweb="button"][kind="primary"],
    div[data-testid="stForm"] button[data-baseweb="button"][kind="primary"]:focus,
    div[data-testid="stForm"] button[data-baseweb="button"][kind="primary"]:active {
        background-color: #0077B6 !important;
        background: #0077B6 !important;
        color: white !important;
        border: none !important;
        border-color: transparent !important;
    }
    
    .stForm button[data-baseweb="button"][kind="primary"]:hover,
    .stForm [data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stForm"] button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #023E8A !important;
        background: #023E8A !important;
        color: white !important;
    }
    
    button[data-baseweb="button"][kind="primary"],
    button[data-baseweb="button"][kind="primary"]:focus,
    button[data-baseweb="button"][kind="primary"]:active,
    button[data-baseweb="button"][kind="primary"]:visited {
        background-color: #0077B6 !important;
        background: #0077B6 !important;
        color: white !important;
        border: none !important;
    }
    
    button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #023E8A !important;
        background: #023E8A !important;
        color: white !important;
    }
    
    .stForm [data-testid="stFormSubmitButton"] + div small,
    .stForm [data-testid="stFormSubmitButton"] ~ div small,
    div[data-testid="stForm"] [data-testid="stFormSubmitButton"] + div small,
    div[data-testid="stForm"] [data-testid="stFormSubmitButton"] ~ div small {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 0 !important;
        line-height: 0 !important;
    }
    
    .stForm {
        background: #ffffff;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 2px solid #90E0EF;
        box-shadow: 0 8px 32px rgba(144, 224, 239, 0.2);
    }
    
    .stForm p,
    .stForm div,
    .stForm h3,
    .stForm label {
        color: #023E8A !important;
    }
    
    [data-testid="stTooltip"],
    .stTooltip {
        color: #023E8A !important;
    }
    
    .stSuccess {
        border-radius: 12px !important;
        border-left: 4px solid #0077B6 !important;
        background-color: rgba(202, 240, 248, 0.5) !important;
    }
    
    .stError {
        border-radius: 12px !important;
        border-left: 4px solid #023E8A !important;
        background-color: rgba(202, 240, 248, 0.5) !important;
    }
    
    .stWarning {
        border-radius: 12px !important;
        border-left: 4px solid #0077B6 !important;
        background-color: rgba(202, 240, 248, 0.5) !important;
    }
    
    .stInfo {
        border-radius: 12px !important;
        border-left: 4px solid #0077B6 !important;
        background-color: rgba(202, 240, 248, 0.5) !important;
    }
    
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #90E0EF;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        color: #023E8A !important;
        background-color: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0077B6 !important;
        border-bottom: 3px solid #0077B6 !important;
        background-color: rgba(202, 240, 248, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0077B6 !important;
        background-color: rgba(144, 224, 239, 0.1) !important;
    }
    
    .streamlit-expanderHeader {
        border-radius: 12px;
        font-weight: 600;
        color: #023E8A !important;
        background-color: rgba(202, 240, 248, 0.2) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(144, 224, 239, 0.3) !important;
    }
    
    .js-plotly-plot {
        background-color: #ffffff !important;
    }
    
    .stBarChart rect,
    .stBarChart [class*="bar"] {
        fill: #0077B6 !important;
    }
    
    .stBarChart rect:hover {
        fill: #023E8A !important;
    }
    
    .stAudioInput {
        border-radius: 16px;
        overflow: hidden;
    }
    
    .locked-workspace {
        text-align: center;
        color: #023E8A;
        padding: 60px 40px;
        background: #ffffff;
        border-radius: 20px;
        border: 2px dashed #90E0EF;
        box-shadow: 0 4px 16px rgba(144, 224, 239, 0.2);
        margin: 0 auto;
        max-width: 800px;
    }
    
    .locked-workspace h3 {
        color: #023E8A;
        margin-bottom: 1rem;
    }
    
    .unlocked-workspace {
        margin: 0 auto;
        max-width: 800px;
        padding: 0 20px;
    }
    
    .hero-text {
        line-height: 1.6;
        color: #023E8A;
        font-size: 1.125rem;
    }
    
    .stSpinner > div {
        border-top-color: #0077B6;
    }
    
    code {
        background: rgba(144, 224, 239, 0.2);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Fira Code', 'Courier New', monospace;
        color: #023E8A;
    }
    
    .stCodeBlock,
    .stCodeBlock > div,
    .stCodeBlock pre,
    .stCodeBlock code,
    div[data-testid="stCodeBlock"],
    div[data-testid="stCodeBlock"] > div,
    div[data-testid="stCodeBlock"] pre,
    div[data-testid="stCodeBlock"] code,
    pre,
    pre code,
    code[class*="language"],
    pre[class*="language"] {
        background-color: rgba(202, 240, 248, 0.5) !important;
        background: rgba(202, 240, 248, 0.5) !important;
        color: #023E8A !important;
        border: 1px solid #90E0EF !important;
        border-radius: 8px !important;
    }
    
    .stCodeBlock pre,
    div[data-testid="stCodeBlock"] pre,
    pre {
        background-color: rgba(202, 240, 248, 0.5) !important;
        background: rgba(202, 240, 248, 0.5) !important;
        color: #023E8A !important;
        padding: 15px !important;
    }
    
    .stCodeBlock code,
    div[data-testid="stCodeBlock"] code,
    pre code,
    code {
        background-color: transparent !important;
        background: transparent !important;
        color: #023E8A !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }
    
    *[style*="background"] code,
    *[style*="background-color"] code,
    pre[style*="background"],
    code[style*="background"] {
        background-color: rgba(202, 240, 248, 0.5) !important;
        background: rgba(202, 240, 248, 0.5) !important;
    }
    
    .stCodeBlock .token.keyword,
    div[data-testid="stCodeBlock"] .token.keyword {
        color: #0077B6 !important;
        font-weight: 600 !important;
    }
    
    .stCodeBlock .token.string,
    div[data-testid="stCodeBlock"] .token.string {
        color: #023E8A !important;
    }
    
    .stCodeBlock .token.function,
    div[data-testid="stCodeBlock"] .token.function {
        color: #0077B6 !important;
    }
    
    .stCodeBlock .token.comment,
    div[data-testid="stCodeBlock"] .token.comment {
        color: #90E0EF !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #CAF0F8;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #023E8A 0%, #0077B6 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0077B6 0%, #023E8A 100%);
    }
    
    [data-testid="stMetricValue"] {
        font-weight: 700;
        color: #023E8A;
    }
    
    a {
        color: #023E8A !important;
    }
    
    a:hover {
        color: #0077B6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {}
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False

# Helper functions
def load_lottieurl(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

def clean_db_url(url):
    if not url: return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}sslmode=require"
    return url

def seed_database(db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS transactions;"))
            conn.execute(text("""
                CREATE TABLE transactions (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    category VARCHAR(50),
                    amount DECIMAL(10, 2),
                    merchant VARCHAR(100),
                    type VARCHAR(10)
                );
            """))
            conn.execute(text("""
                INSERT INTO transactions (date, category, amount, merchant, type) VALUES 
                ('2024-01-15', 'Food', 15.50, 'Burger King', 'expense'),
                ('2024-01-16', 'Transport', 45.00, 'Uber', 'expense'),
                ('2024-02-01', 'Salary', 5000.00, 'Tech Corp', 'income'),
                ('2024-02-10', 'Utilities', 120.00, 'Electric Co', 'expense'),
                ('2024-02-15', 'Food', 85.00, 'Fancy Steakhouse', 'expense'),
                ('2024-03-05', 'Shopping', 200.00, 'Nike', 'expense'),
                ('2024-03-10', 'Investments', 1000.00, 'Vanguard', 'expense');
            """))
            conn.commit()
        return True, "Database connected and seeded successfully!"
    except Exception as e:
        return False, str(e)

def transcribe_audio(audio_file, api_key):
    try:
        url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&language=en-US"
        headers = {"Authorization": f"Token {api_key}", "Content-Type": "audio/*"}
        response = httpx.post(url, headers=headers, content=audio_file.getvalue(), timeout=30.0)
        
        if response.status_code != 200:
            error_data = response.text
            try:
                error_json = response.json()
                error_data = error_json.get("err_msg", str(error_json))
            except:
                pass
            error_msg = f"Deepgram API Error (Status {response.status_code}): {error_data}"
            print(f"[ERROR] {error_msg}")
            st.error(error_msg)
            return None
        
        data = response.json()
        if "results" not in data:
            error_msg = f"Unexpected API response format: {data}"
            print(f"[ERROR] {error_msg}")
            st.error(error_msg)
            return None
        
        if "channels" not in data["results"] or len(data["results"]["channels"]) == 0:
            error_msg = "No transcription channels found in API response"
            print(f"[ERROR] {error_msg}")
            st.error(error_msg)
            return None
        
        transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(f"[SUCCESS] Transcription: {transcript}")
        return transcript
    except KeyError as e:
        error_msg = f"Transcription Error: Missing key in API response - {e}"
        response_data = "N/A"
        if 'response' in locals():
            try:
                response_data = response.json()
            except:
                response_data = response.text
        full_error = f"{error_msg}. Response: {response_data}"
        print(f"[ERROR] {full_error}")
        st.error(full_error)
        return None
    except Exception as e:
        import traceback
        error_msg = f"Transcription Error: {str(e)}"
        traceback_str = traceback.format_exc()
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Traceback:\n{traceback_str}")
        st.error(f"{error_msg}. Check console for full details.")
        return None

def text_to_sql(query_text, api_key):
    try:
        client = Groq(api_key=api_key)
        system_prompt = """
        You are a SQL expert. Table: 'transactions'. 
        Cols: date, category, amount, merchant, type.
        Return ONLY the SQL query. Example: SELECT * FROM transactions;
        """
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query_text}],
            model="llama-3.3-70b-versatile", temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"LLM Error: {e}")
        return None

def execute_sql(sql_query, db_url):
    try:
        engine = create_engine(clean_db_url(db_url))
        with engine.connect() as conn:
            return pd.read_sql(text(sql_query), conn)
    except Exception as e:
        return f"Database Error: {str(e)}"

# Load animations
lottie_voice = load_lottieurl("https://lottie.host/64299b9b-9864-448c-9418-508b4618779c/g2DkU4yQyv.json")
lottie_data = load_lottieurl("https://lottie.host/90822361-26c7-432d-8860-262846876c27/1X2f3M3i2g.json")
lottie_robot = load_lottieurl("https://lottie.host/5a0248c8-38c8-4721-827c-3f9f4a01c40f/P2Vj8s7q8t.json")


# Hero section
st.markdown("<div style='padding: 40px 0 20px 0;'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown("<h1 style='margin-bottom: 0.5rem;'>VoiceQL</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0;'>The AI Financial Analyst that listens.</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p class='hero-text'>Stop wrestling with spreadsheets. Just speak to your data and get instant answers, charts, and insights powered by cutting-edge AI.</p>", 
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<a href="#setup-section" class="nav-btn"> Let\'s talk to your data</a>', unsafe_allow_html=True)
        
with col2:
    if lottie_voice:
        st_lottie(lottie_voice, height=450, key="voice")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Features section
st.markdown("<h2 style='text-align: center; margin-bottom: 50px;'>Why VoiceQL?</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="feature-card">
        <h3>Natural Voice</h3>
        <p>Powered by <strong style="color: #0077B6;">Deepgram Nova-2</strong>. It understands complex queries even with background noise.</p>
    </div>
    """, unsafe_allow_html=True)
    
with c2:
    st.markdown("""
    <div class="feature-card">
        <h3>Real-Time SQL</h3>
        <p>Powered by <strong style="color: #0077B6;">Groq Llama-3</strong>. It translates English to perfect PostgreSQL in milliseconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
with c3:
    st.markdown("""
    <div class="feature-card">
        <h3>Instant Viz</h3>
        <p>Automatically visualizes your data trends. No drag-and-drop required.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Setup section
st.markdown("<div id='setup-section'></div>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>How it works ?</h2>", unsafe_allow_html=True)

c_side, c_center, c_side2 = st.columns([1, 2.5, 1], gap="medium")
with c_center:
    st.markdown("""
    <div style="margin-bottom: 40px;">
        <h3 style="color: #023E8A; margin-bottom: 15px;">
            <strong style="color: #0077B6;">1. Connect</strong> your secure database
        </h3>
        <p style="color: #023E8A; margin-bottom: 20px;">
            Add your database connection and API keys below. 
            </br>
            Need help creating these keys? 
            <a href="https://neon.tech/docs/connect/connect-from-any-app" target="_blank" style="color: #0077B6; text-decoration: underline;">Neon Database Guide</a> | 
            <a href="https://console.groq.com/keys" target="_blank" style="color: #0077B6; text-decoration: underline;">Groq API Keys</a> | 
            <a href="https://console.deepgram.com/signup" target="_blank" style="color: #0077B6; text-decoration: underline;">Deepgram API Keys</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Your keys are processed locally. Connect to activate the workspace below.")
    st.markdown("<br>", unsafe_allow_html=True)

    try:
        default_neon = st.secrets.get("NEON_DB_URL", "")
        default_groq = st.secrets.get("GROQ_API_KEY", "")
        default_deepgram = st.secrets.get("DEEPGRAM_API_KEY", "")
    except Exception:
        default_neon, default_groq, default_deepgram = "", "", ""

    with st.form("setup_form", clear_on_submit=False):
        st.markdown("### Database & API Configuration")
        
        st.markdown("""
        <div style="margin-bottom: 15px; padding: 15px; background: rgba(144, 224, 239, 0.1); border-radius: 8px; border-left: 3px solid #0077B6;">
            <p style="margin: 0; color: #023E8A; font-size: 0.9rem;">
                <strong>Quick Setup:</strong> Create a free account and get your API keys from the links above. 
                For Neon, create a new project and copy the connection string.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        neon_input = st.text_input(
            "Neon Database URL", 
            value=default_neon, 
            type="password",
            help="Get your connection string from Neon dashboard after creating a project"
        )
        groq_input = st.text_input(
            "Groq API Key", 
            value=default_groq, 
            type="password",
            help="Create a free API key at console.groq.com"
        )
        deepgram_input = st.text_input(
            "Deepgram API Key", 
            value=default_deepgram, 
            type="password",
            help="Sign up at console.deepgram.com to get your API key"
        )
        
        submitted = st.form_submit_button(
            "Connect & Initialize", 
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if neon_input and groq_input and deepgram_input:
                st.session_state.api_keys = {
                    "neon": clean_db_url(neon_input),
                    "groq": groq_input,
                    "deepgram": deepgram_input
                }
                with st.spinner("Seeding secure database environment..."):
                    success, message = seed_database(st.session_state.api_keys["neon"])
                if success:
                    st.success(message)
                    st.session_state.db_connected = True
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<a href="#workspace-section" class="nav-btn">Go to Workspace</a>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {message}")
            else:
                st.warning("All keys are required to proceed.")
    
    st.markdown("""
    <div style="margin-top: 50px; margin-bottom: 20px;">
        <h3 style="color: #023E8A; margin-bottom: 15px;">
            <strong style="color: #0077B6;">2. Ask</strong> a question
        </h3>
        <p style="color: #023E8A; margin-bottom: 20px;">
            Once connected, use the workspace below to ask questions like <em>'What were my top expenses last month?'</em> or <em>'Show me all transactions over $100'</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div id='workspace-section'></div>", unsafe_allow_html=True)

    if st.session_state.db_connected:
        st.markdown("<div class='unlocked-workspace'>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #023E8A; margin-bottom: 20px;'>Press record to query the <strong>Transactions</strong> database using natural language.</p>", 
            unsafe_allow_html=True
        )
        
        col_input, col_status = st.columns([3, 1], gap="medium")
        with col_input:
            audio_value = st.audio_input("Record Voice Command", label_visibility="visible")
        with col_status:
            if lottie_robot:
                st_lottie(lottie_robot, height=120, key="robot")
        
        st.markdown("""
        <div style="margin-top: 50px; margin-bottom: 20px;">
            <h3 style="color: #023E8A; margin-bottom: 15px;">
                <strong style="color: #0077B6;">3. Watch</strong> as VoiceQL works its magic
            </h3>
            <p style="color: #023E8A; margin-bottom: 20px;">
                VoiceQL will transcribe your voice, generate the SQL query, execute it on your database, and automatically visualize the results.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if audio_value and st.session_state.db_connected:
            with st.spinner("Transcribing your voice..."):
                transcript = transcribe_audio(audio_value, st.session_state.api_keys["deepgram"])
            
            if transcript:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(0, 119, 182, 0.08) 0%, rgba(144, 224, 239, 0.15) 100%); 
                            padding: 20px; border-radius: 12px; border-left: 4px solid #0077B6; 
                            margin: 20px 0;'>
                    <strong style='color: #0077B6;'>You asked:</strong> 
                    <span style='color: #023E8A; font-size: 1.05rem;'>"{transcript}"</span>
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("Generating SQL query with AI..."):
                    sql = text_to_sql(transcript, st.session_state.api_keys["groq"])
                    
                if sql:
                    cleaned_sql = sql.replace("```sql", "").replace("```", "").strip()
                    
                    st.markdown("### Generated SQL Query")
                    with st.expander("View Generated SQL Query", expanded=True):
                        st.code(cleaned_sql, language="sql")
                    
                    with st.spinner("Querying database..."):
                        result = execute_sql(cleaned_sql, st.session_state.api_keys["neon"])
                    
                    if isinstance(result, str):
                        st.markdown("### Database Output")
                        st.error(f"{result}")
                    elif result.empty:
                        st.markdown("### Database Output")
                        st.warning("Query executed successfully but returned no results.")
                    else:
                        st.markdown("### Database Output")
                        st.success("Query successful! Results displayed below.")
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        st.markdown("### Visualization")
                        tab1, tab2 = st.tabs(["Chart View", "Raw Data"])
                        with tab1:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if len(result.columns) >= 2:
                                try:
                                    df_chart = result.set_index(result.columns[0])
                                    if len(df_chart.columns) == 1:
                                        fig = px.bar(
                                            df_chart.reset_index(),
                                            x=df_chart.index.name if df_chart.index.name else 'Index',
                                            y=df_chart.columns[0],
                                            color_discrete_sequence=['#0077B6'],
                                            labels={df_chart.columns[0]: 'Value'}
                                        )
                                    else:
                                        fig = px.bar(
                                            df_chart.reset_index(),
                                            x=df_chart.index.name if df_chart.index.name else 'Index',
                                            y=df_chart.columns.tolist(),
                                            color_discrete_sequence=['#0077B6', '#023E8A', '#90E0EF', '#CAF0F8'],
                                            labels={df_chart.index.name if df_chart.index.name else 'Index': 'Category'}
                                        )
                                    
                                    fig.update_layout(
                                        plot_bgcolor='#ffffff',
                                        paper_bgcolor='#ffffff',
                                        font=dict(color='#023E8A'),
                                        xaxis=dict(gridcolor='#90E0EF'),
                                        yaxis=dict(gridcolor='#90E0EF'),
                                        showlegend=True,
                                        legend=dict(font=dict(color='#023E8A'))
                                    )
                                    fig.update_traces(marker_line_color='#023E8A', marker_line_width=1)
                                    st.plotly_chart(fig, use_container_width=True)
                                except Exception as e:
                                    st.bar_chart(result.set_index(result.columns[0]), use_container_width=True)
                            else:
                                st.metric(label="Result", value=str(result.iloc[0,0]))
                        with tab2:
                            st.markdown("<br>", unsafe_allow_html=True)
                            st.dataframe(result, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)