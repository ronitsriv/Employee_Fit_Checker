import streamlit as st
import google.generativeai as genai
import json
import re

# --------------------------------------------------
# Gemini Configuration
# --------------------------------------------------

API_KEY = "your-api-key-here"
genai.configure(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

st.set_page_config(
    page_title="AI Recruiter Fit Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Recruiter Fit Analyzer")

st.write(
    "Evaluate a candidate against a Job Description like an experienced "
    "recruiter — using reasoning rather than keyword matching."
)

# --------------------------------------------------
# Preloaded Demo Data
# --------------------------------------------------

sample_resume = """
RONIT SRIVASTAVA

Software Engineer | Java Backend Developer

EDUCATION
B.Tech in Computer Science and Engineering

EXPERIENCE

LTIMindtree — Quality Engineer
2025 - Present
- Training and hands-on work involving Python, Selenium and Playwright.
- Backend development exposure using Java, Spring Boot, REST APIs and
  Microservices.
- Worked with relational databases and Docker.

Candescent — Software Engineer Intern
2025
- Worked with Salesforce Apex and platform development.

Subex — AI Intern
2024
- Processed and validated contract and invoice datasets using Python.

PROJECTS

Expense Manager
- Built a full-stack expense management application using Spring Boot,
  React and MySQL.
- Implemented JWT authentication.
- Developed REST APIs.
- Added pagination, filtering and sorting.
- Worked with Docker and AWS deployment.
- Explored Redis caching and Kafka-based notifications.

Job Finder
- Developed a JavaFX application with MongoDB backend.
- Implemented job search and persistence functionality.

SKILLS
Java, Python, Spring Boot, REST APIs, Microservices, SQL, MySQL,
MongoDB, React, Docker, AWS, Redis, Kafka, Git
"""

sample_jd = """
Software Engineer I — Backend

We are looking for a Software Engineer to join our backend engineering
team.

Responsibilities:
- Design and develop RESTful backend services.
- Build and maintain applications using Java and Spring Boot.
- Work with relational databases and SQL.
- Develop reliable and maintainable backend components.
- Participate in debugging, testing and code reviews.
- Work with distributed systems and messaging technologies.
- Collaborate with frontend and other engineering teams.

Requirements:
- 1+ years of software development experience.
- Strong programming fundamentals.
- Experience with Java and Spring Boot.
- Experience developing REST APIs.
- Knowledge of SQL and relational databases.
- Understanding of microservices.
- Exposure to Kafka or another messaging platform is preferred.

Preferred:
- Docker and cloud deployment experience.
- Redis or another caching technology.
- Experience building production-quality applications.
"""

# --------------------------------------------------
# AI Controls
# --------------------------------------------------

st.subheader("⚙️ AI Model Settings")

col1, col2 = st.columns(2)

with col1:
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1
    )

    st.caption(
        "Controls how varied the AI's reasoning is. Lower values make "
        "the evaluation more consistent and focused; higher values can "
        "make the response more exploratory. For recruiter evaluation, "
        "a low value is usually preferable."
    )

with col2:
    max_tokens = st.slider(
        "Max Output Tokens",
        min_value=512,
        max_value=4096,
        value=2048,
        step=256
    )

    st.caption(
        "Controls the maximum amount of text Gemini can generate. "
        "Higher values allow a more detailed recruiter analysis, but "
        "do not make the AI itself more intelligent."
    )

# --------------------------------------------------
# Resume + JD
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Candidate Resume")

    resume = st.text_area(
        "Resume",
        value=sample_resume,
        height=500
    )

with col2:
    st.subheader("💼 Job Description")

    jd = st.text_area(
        "Job Description",
        value=sample_jd,
        height=500
    )

# --------------------------------------------------
# Recruiter Prompt
# --------------------------------------------------

def build_prompt(resume, jd):

    return f"""
You are an experienced technical recruiter and hiring manager.

Evaluate the candidate below for the specific Job Description.

IMPORTANT:

Do NOT behave like an ATS.

Do NOT perform keyword matching.
Do NOT count matching technologies.
Do NOT calculate a score from keyword overlap.

Instead, understand what the company actually needs and reason about
whether this candidate has demonstrated the underlying ability to do
the work.

Think like a recruiter who has spent 20-30 minutes carefully reviewing
the resume and JD.

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Evaluate the following:

1. Understand the actual responsibilities of the role.
2. Determine what engineering capabilities are genuinely required.
3. Determine what the candidate has actually demonstrated.
4. Assess direct experience.
5. Assess transferable skills.

A missing technology does NOT automatically mean the candidate cannot
perform the work.

For example, if the JD asks for Kafka and the candidate has meaningful
RabbitMQ experience, determine whether their understanding of messaging,
producers, consumers and asynchronous systems is transferable.

Do not automatically treat similar technologies as equivalent either.
Explain the reasoning.

6. Carefully evaluate projects.

For early-career candidates, strong projects can provide meaningful
evidence of engineering capability.

However, NEVER falsely convert project experience into professional
experience.

For example:

JD: "1+ years professional backend experience."

Candidate: "Built a substantial Spring Boot backend project."

Correct interpretation:
The formal experience requirement is not met, but the project may
provide strong evidence of relevant practical capability.

7. Distinguish between:

- Professional experience
- Internship experience
- Project experience
- Coursework

8. Identify whether gaps are:

- Fundamental capability gaps
- Technology gaps
- Experience gaps
- Depth gaps
- Domain gaps
- Minor gaps

9. Determine what the candidate could probably do TODAY.

10. Determine what they would probably need training for.

11. Compare the candidate's actual engineering maturity with the
seniority of the role.

12. Decide whether you would actually shortlist this person.

Do not invent experience.

Do not assume knowledge merely because technologies are related.

Do not reject a fresher simply because they lack every technology in
the JD.

The goal is NOT:

"How many things in the resume match the JD?"

The goal is:

"Based on the evidence, how confident would I be that this person could
succeed in this particular role?"

Return ONLY valid JSON:

{{
    "score": 0,
    "decision": "YES/MAYBE/NO",
    "classification": "Strong Match/Good Match/Possible Stretch/Weak Match",

    "summary": "",

    "strongest_reasons": [],

    "transferable_skills": [
        {{
            "jd_requirement": "",
            "candidate_experience": "",
            "assessment": ""
        }}
    ],

    "experience_assessment": "",

    "project_assessment": "",

    "important_gaps": [
        {{
            "gap": "",
            "severity": "Critical/Moderate/Minor",
            "reason": ""
        }}
    ],

    "can_do_now": [],

    "would_need_training": [],

    "recruiter_reasoning": ""
}}
"""

# --------------------------------------------------
# Analyze
# --------------------------------------------------

if st.button("🔍 Analyze Candidate", type="primary"):

    if not resume.strip() or not jd.strip():
        st.warning("Please provide both a resume and Job Description.")
        st.stop()

    model = genai.GenerativeModel(MODEL)

    with st.spinner("Deeply evaluating candidate against the role..."):

        response = model.generate_content(
            build_prompt(resume, jd),
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens
            }
        )

    try:

        text = response.text.strip()

        text = re.sub(
            r"^```json\s*|\s*```$",
            "",
            text,
            flags=re.IGNORECASE
        )

        result = json.loads(text)

        # --------------------------------------------------
        # Overall Result
        # --------------------------------------------------

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Overall Fit",
            f"{result['score']}/100"
        )

        col2.metric(
            "Assessment",
            result["classification"]
        )

        col3.metric(
            "Shortlist?",
            result["decision"]
        )

        # --------------------------------------------------
        # Recruiter Summary
        # --------------------------------------------------

        st.subheader("🧠 Recruiter Summary")

        st.write(result["summary"])

        # --------------------------------------------------
        # Strongest Reasons
        # --------------------------------------------------

        st.subheader("💪 Strongest Reasons")

        for reason in result["strongest_reasons"]:
            st.write("• " + reason)

        # --------------------------------------------------
        # Transferable Skills
        # --------------------------------------------------

        st.subheader("🔄 Transferable Skills")

        for item in result["transferable_skills"]:

            with st.expander(item["jd_requirement"]):

                st.write(
                    "**Candidate experience:**",
                    item["candidate_experience"]
                )

                st.write(
                    "**Recruiter assessment:**",
                    item["assessment"]
                )

        # --------------------------------------------------
        # Experience
        # --------------------------------------------------

        st.subheader("👨‍💻 Experience Assessment")

        st.write(result["experience_assessment"])

        # --------------------------------------------------
        # Projects
        # --------------------------------------------------

        st.subheader("🛠️ Project Assessment")

        st.write(result["project_assessment"])

        # --------------------------------------------------
        # Gaps
        # --------------------------------------------------

        st.subheader("⚠️ Important Gaps")

        for gap in result["important_gaps"]:

            st.write(
                f"**{gap['severity']} — {gap['gap']}**  \n"
                f"{gap['reason']}"
            )

        # --------------------------------------------------
        # Immediate Capability
        # --------------------------------------------------

        st.subheader("✅ What the Candidate Can Probably Do Now")

        for item in result["can_do_now"]:
            st.write("• " + item)

        # --------------------------------------------------
        # Training
        # --------------------------------------------------

        st.subheader("📚 What Would Require Training")

        for item in result["would_need_training"]:
            st.write("• " + item)

        # --------------------------------------------------
        # Final Decision
        # --------------------------------------------------

        st.subheader("🎯 Final Recruiter Reasoning")

        st.write(result["recruiter_reasoning"])

    except Exception as e:

        st.error("Gemini returned an unexpected response.")

        st.write(response.text)

        st.caption(f"Parsing error: {e}")
