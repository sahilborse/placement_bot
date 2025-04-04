import streamlit as st
import time
import requests

# Set page config
st.set_page_config(page_title="Mock Interview", layout="centered")

# CSS for dark theme, animated background, and custom UI
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(-45deg, #5500ff, #ff0055, #00ffaa, #ff5500);
            background-size: 300% 300%;
            animation: animateBg 15s infinite alternate ease-in-out;
            z-index: -1;
        }
        @keyframes animateBg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .interview-box {
            background-color: #1e1e1e;
            padding: 0;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
            margin-top: 30px;
        }
    </style>
    <div class='background'></div>
""", unsafe_allow_html=True)

# Initialize session state
if "specialization" not in st.session_state:
    st.session_state.specialization = ""
if "questions" not in st.session_state:
    st.session_state.questions = []
if "question_index" not in st.session_state:
    st.session_state.question_index = -1
if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Get specialization from user
if st.session_state.specialization == "":
    st.title("🎤 Mock Interview")
    specialization = st.text_input("Enter your specialization (e.g., Software Engineering):")
    
    if st.button("Start Interview"):
        if specialization:
            st.session_state.specialization = specialization
            
            # Fetch initial questions from the mock interview API (POST request)
            response = requests.post("/mock-interview", json={"specialization": specialization})
            
            if response.status_code == 200:
                st.session_state.questions = response.json().get("questions", [])
                if st.session_state.questions:
                    st.session_state.question_index = 0
                else:
                    st.error("No questions found for this specialization.")
            else:
                st.error("Failed to fetch questions. Please try again.")
        else:
            st.error("Please enter a specialization.")

# Proceed with the interview if questions are available
if st.session_state.question_index >= 0 and st.session_state.questions:
    total_questions = len(st.session_state.questions)
    current_question = st.session_state.question_index + 1
    st.title(f"🎤 Mock Interview - Question {current_question} of {total_questions}")

    # Display current question
    question = st.session_state.questions[st.session_state.question_index]
    st.markdown(f"<div class='interview-box'><b>Question:</b><br>{question}</div>", unsafe_allow_html=True)

    # Answer input field
    user_answer = st.text_area("Your Answer:", height=200)

    # Submit answer
    if st.button("Submit Answer"):
        with st.spinner("Analyzing your response..."):
            time.sleep(2)  # Simulate processing delay

            # Provide feedback using the feedback API (POST request)
            feedback_response = requests.post("/provide-feedback", json={"answer": user_answer})
            
            if feedback_response.status_code == 200:
                feedback = feedback_response.json().get("feedback", "Feedback not available.")
            else:
                feedback = "Error retrieving feedback."

            # Store the feedback history
            st.session_state.feedback_history.append((question, user_answer, feedback))
            st.session_state.submitted = True

    # Next button appears only after submission
    if st.session_state.submitted:
        if st.session_state.question_index < total_questions - 1:
            if st.button("Next Question"):
                st.session_state.question_index += 1
                st.session_state.submitted = False
        else:
            st.success("🎉 You’ve completed all the initial interview questions!")
            
            # Fetch additional questions based on specialization
            with st.spinner("Fetching additional questions..."):
                additional_response = requests.post("/mock-interview", json={"specialization": st.session_state.specialization})
                
                if additional_response.status_code == 200:
                    additional_questions = additional_response.json().get("questions", [])
                    if additional_questions:
                        st.success("Additional questions fetched successfully!")
                        st.session_state.questions.extend(additional_questions)
                        st.session_state.question_index += 1
                        st.session_state.submitted = False
                    else:
                        st.info("No additional questions available.")
                else:
                    st.error("Failed to fetch additional questions.")

# Display feedback history
if st.session_state.feedback_history:
    st.markdown("## 🧠 Feedback Summary")
    for i, (q, a, f) in enumerate(st.session_state.feedback_history, 1):
        st.markdown(f"""
        <div class='interview-box'>
            <b>Q{i}: {q}</b><br>
            <b>Your Answer:</b> {a}<br>
            <b>Feedback:</b> {f}
        </div>
        """, unsafe_allow_html=True)

# Hide Streamlit branding
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)
