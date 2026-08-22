# AI Recruiter Fit Analyzer

An AI-powered resume-to-JD evaluation tool built with **Python, Streamlit, and Gemini**.

Instead of traditional ATS keyword matching, the app evaluates a candidate like an experienced technical recruiter by considering:

* **Actual demonstrated capabilities**
* **Transferable skills**
* **Project experience**, especially for freshers
* **Professional vs internship vs project experience**
* **Experience and seniority gaps**
* **What the candidate can likely do immediately**
* **What would require additional training**
* **Overall likelihood of being shortlisted**

### How it works

1. Paste a candidate's **resume**.
2. Paste the **Job Description**.
3. Adjust Gemini's **Temperature** and **Max Output Tokens** if desired.
4. Click **Analyze Candidate**.
5. Gemini provides a recruiter-style assessment and shortlist recommendation.

### Key idea

The system does **not** ask:

> "How many keywords from the JD appear in the resume?"

Instead, it asks:

> **"Based on the evidence in this resume, could this candidate realistically succeed in this particular role?"**

### Tech Stack

* Python
* Streamlit
* Google Gemini API
* JSON-based structured AI output

### Run locally

```bash
pip install streamlit google-generativeai
streamlit run ai_recruiter_fit.py
```

Replace `your-api-key-here` in the Python file with your Gemini API key.
