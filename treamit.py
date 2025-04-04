import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="Placement Guidance", layout="wide")

# Background and CSS
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(-45deg, #ff4b2b, #ff416c, #1e90ff, #00ffaa);
            background-size: 400% 400%;
            animation: gradientShift 10s ease infinite;
            z-index: -1;
        }
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 95vh;
            color: white;
        }
        .title {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 1.5rem;
            font-weight: 300;
            max-width: 800px;
            text-align: center;
            margin-bottom: 50px;
        }
        .btn-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .custom-btn {
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: linear-gradient(145deg, #1e1e1e, #292929);
            border: none;
            border-radius: 12px;
            box-shadow: 5px 5px 15px #0a0a0a, -5px -5px 15px #262626;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .custom-btn:hover {
            transform: scale(1.08);
            background: linear-gradient(145deg, #292929, #1e1e1e);
        }
    </style>

    <div class="background"></div>
    <div class="main-container">
        <div class="title">🚀 Placement Guidance</div>
        <div class="subtitle">
            Your all-in-one AI-powered assistant to get you placement-ready.<br>
            From resume reviews to mock interviews and keyword optimization – we've got you covered!
        </div>
        <div class="btn-grid">
            <button class="custom-btn" onclick='window.location.href="/resume-analyzer.py"'>📄 Resume Analyzer</button>
            <button class="custom-btn" onclick='window.location.href="/mock-interview.py"'>🧠 Mock Interview</button>
            <button class="custom-btn" onclick='window.location.href="/Jobs.py"'>🔍 Keyword Optimizer</button>
            <button class="custom-btn" onclick='window.location.href="/chatbot.py"'>📊 Job Fit Score</button>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hide Streamlit branding
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
