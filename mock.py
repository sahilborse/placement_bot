from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import ollama
import PyPDF2
from typing import List
import json
import re
from pydantic import BaseModel

app = FastAPI()

# Define request model
class JobRequest(BaseModel):
    skills: str
    experience: int

def ask_question(role: str, prompt: str):
    """Send prompt to Ollama (Gemma model) and return the response."""
    response = ollama.chat(model="gemma", messages=[{"role": role, "content": prompt}])
    return response["message"]["content"] if "message" in response else "No response received."

@app.post("/suggest-job-roles")
async def suggest_job_roles(request: JobRequest):
    """Suggest job roles based on user's skills and experience."""
    prompt = f'''
    You are an AI career assistant.
    
    Given:
    - Skills: {request.skills}
    - Experience: {request.experience}
    
    Suggest **3 job roles** in **valid JSON format only**:
    
    ```json
    [
        {{
            "Job Title": "Software Engineer",
            "Description": "Develop scalable applications using Python and JavaScript."
        }},
        {{
            "Job Title": "Machine Learning Engineer",
            "Description": "Work on AI models and deploy deep learning pipelines."
        }},
        {{
            "Job Title": "Data Scientist",
            "Description": "Analyze large datasets and extract meaningful insights."
        }}
    ]
    ```

    Only return JSON data, nothing else.
    '''
    raw_response = ask_question("user", prompt)

    try:
        json_response = json.loads(raw_response)
        if not isinstance(json_response, list):
            raise ValueError("Expected a list of job roles.")
        return json_response
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON response from the model.")

@app.post("/provide-feedback")
async def provide_feedback(user_input: str = Form(...), ai_question: str = Form(...)):
    """Provide feedback on user's interview answer."""
    prompt = f"Provide brief, actionable feedback on: '{user_input}' for the question: '{ai_question}'."
    feedback = ask_question("user", prompt)
    return {"feedback": feedback}

@app.get("/ai-guidance")
async def ai_guidance(question: str):
    """Provide AI-based pre-placement guidance."""
    prompt = f"You are a placement advisor. Provide a concise answer to: '{question}' in 3 sentences or less."
    response = ask_question("user", prompt)
    return {"guidance": response}

@app.post("/mock-interview")
async def mock_interview(specialization: str = Form(...)):
    """Conduct a mock interview with HR & technical questions."""
    hr_questions = [
        "Tell me about yourself.",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why do you want this job?",
        "Where do you see yourself in 5 years?"
    ]

    tech_question = ask_question('user', f"Ask a technical question related to {specialization}.")
    
    return {
        "HR_questions": hr_questions,
        "Technical_Question": tech_question
    }

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...), job_role: str = Form(...)):
    """Analyze the resume and suggest improvements."""
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        resume_text = "\n".join(
            page.extract_text() for page in pdf_reader.pages if page.extract_text()
        )

        if not resume_text.strip():
            return {"error": "Unable to extract text from PDF. Please check the format."}

        prompt = f"""
        You are a professional resume evaluator.
        
        **Analyze the following resume** for the role of **{job_role}**.
        
        Resume:
        ```
        {resume_text}
        ```

        🔹 **Score the resume out of 100** (based on job relevance, tech stack, skills, and projects).
        🔹 **Highlight 3–5 strengths** of the resume.
        🔹 **Suggest missing keywords** that could improve ATS ranking.
        🔹 **Provide actionable feedback in 3 bullet points**.

        📌 **Return JSON output**:
        ```json
        {{
            "score": 85,
            "strengths": ["Strong project portfolio", "Relevant tech stack", "Good soft skills"],
            "missing_keywords": ["Kubernetes", "CI/CD", "Cloud Computing"],
            "feedback": ["Improve description of achievements", "Add quantifiable results", "Highlight leadership roles"]
        }}
        ```
        """
        response = ask_question("user", prompt)
        return json.loads(response)

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the FastAPI-based Mock Interview System!"}
