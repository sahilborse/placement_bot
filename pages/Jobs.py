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

# Load animation
lottie_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# Page configuration
st.set_page_config(page_title="Job Finder", page_icon="💼", layout="centered")

# Add background animation
if lottie_animation:
    st_lottie(lottie_animation, height=300, key="background", loop=True)

# Page title
st.title("💼 Job Finder")
st.markdown("### Enter your skills and experience to find the best job opportunities!")

# Input fields
skills = st.text_input("Enter your skills (comma-separated):", placeholder="e.g., Python, Data Analysis, Machine Learning")
experience = st.number_input("Enter your years of experience:", min_value=0, max_value=50, step=1)

# Submit button
# if st.button("Find Jobs"):
#     if skills and experience >= 0:
#         # Prepare data for API
#         payload = {
#             "skills": skills,
#             "experience": experience
#         }
#         try:
#             # Call API (replace 'https://api.example.com/jobs' with your actual API endpoint)
#             response = requests.post("http://127.0.0.1:8000/suggest-job-roles", json=payload)
#             if response.status_code == 200:
#                 st.success("Jobs fetched successfully!")
#                 st.json(response.json())  # Display API response
#             else:
#                 st.error(f"Failed to fetch jobs. Status code: {response.status_code}")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#     else:
#         st.warning("Please fill in all the fields.")

if st.button("Find Jobs"):
    if skills and experience >= 0:
        payload = {
            "skills": skills,
            "experience": experience
        }
        try:
            response = requests.post("http://127.0.0.1:8000/suggest-job-roles", json=payload)
            if response.status_code == 200:
                st.success("Jobs fetched successfully!")
                # st.markdown(response.text)
                jobs = response.json()

                st.markdown("## 🧾 Suggested Job Roles")
                for idx, job in enumerate(jobs, 1):
                    st.markdown(f"""
                    <div style="background-color:#1e1e1e; padding:15px; border-radius:10px; margin:10px 0; box-shadow: 0 0 10px rgba(255,255,255,0.1);">
                        <h4 style="color:#00ffaa;">{idx}. {job['Job Title']}</h4>
                        <p style="color:#ffffff;">{job['Description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"Failed to fetch jobs. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please fill in all the fields.")
