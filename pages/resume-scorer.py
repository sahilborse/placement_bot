import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Function to load Lottie animation
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load background animation
lottie_background = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# Configure Streamlit page
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered", initial_sidebar_state="collapsed")

# Background animation
with st.container():
    if lottie_background:
        st_lottie(lottie_background, height=300, key="background", loop=True, speed=1)

# Title and instructions
st.title("📄 Resume Analyzer")
st.markdown("#### Upload your resume and enter a job role to analyze how well it fits.")

# Upload field and job role input
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
job_role = st.text_input("Enter desired job role", placeholder="e.g., Python Developer")

# Submit and call API
if st.button("Analyze Resume"):
    if uploaded_file and job_role:
        try:
            # Prepare files and data
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"job_role": job_role}

            # Send to API
            response = requests.post("http://127.0.0.1:8000/analyze-resume", files=files, data=data)

            # Parse and show result
            if response.status_code == 200:
                result = response.json()
                if "resume_analysis" in result:
                    st.success("✅ Resume analysis completed!")
                    st.markdown("#### 🧠 AI Keyword Analysis")

                    analysis_text = result["resume_analysis"]

                    try:
                        found_keywords = []
                        missing_keywords = []

                        # Split into lines
                        for line in analysis_text.split("\n"):
                            if line.strip().lower().startswith("1.") or "Keywords Found" in line:
                                found_keywords = line.split(":")[1].strip(" []\n").split(", ")
                            elif line.strip().lower().startswith("2.") or "Recommended Keywords" in line:
                                missing_keywords = line.split(":")[1].strip(" []\n").split(", ")

                        st.markdown("### ✅ Keywords Found in Your Resume")
                        for keyword in found_keywords:
                            st.markdown(f"- 🟢 **{keyword}**")

                        st.markdown("---")
                        st.markdown("### 🚀 Recommended Keywords to Add")
                        for keyword in missing_keywords:
                            st.markdown(f"- 🔴 **{keyword}**")

                        st.info("Use the above missing keywords to better align your resume with the job role!")

                    except Exception as parse_err:
                        st.markdown("#### Raw Response")
                        st.code(result["resume_analysis"])
                        st.warning("Could not parse the response into keyword sections. Showing raw text instead.")
                elif "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    st.warning("Unexpected response format.")
            else:
                st.error(f"❌ API returned status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ An error occurred while connecting to the API: {e}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
    else:
        st.warning("Please upload a resume and enter a job role.")
