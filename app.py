import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="📄",
    layout="wide"
)

# =========================
# API KEY FROM STREAMLIT SECRETS
# =========================

# =========================
# GEMINI API KEY
# =========================

api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# TITLE
# =========================

st.title("📄 AI Resume & Portfolio Builder")

st.markdown("""
Generate professional ATS-friendly resumes,
cover letters, and portfolio summaries using Generative AI.
""")

# =========================
# USER INPUT
# =========================

st.header("Personal Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    email = st.text_input("Email")

with col2:
    phone = st.text_input("Phone Number")
    target_role = st.text_input("Target Job Role")

st.header("Education")

education = st.text_area(
    "Education Details",
    placeholder="B.Tech Computer Science, XYZ University..."
)

st.header("Skills")

skills = st.text_area(
    "Skills",
    placeholder="Python, Java, SQL, Machine Learning..."
)

st.header("Projects")

projects = st.text_area(
    "Projects",
    placeholder="AI Chatbot, Portfolio Website..."
)

st.header("Experience")

experience = st.text_area(
    "Experience",
    placeholder="Internship, Freelance Work..."
)

st.header("Certifications")

certifications = st.text_area(
    "Certifications",
    placeholder="IBM SkillsBuild, AWS..."
)

st.header("Career Objective")

career_objective = st.text_area(
    "Career Objective",
    placeholder="Aspiring Software Engineer..."
)

# =========================
# PDF FUNCTION
# =========================

def create_pdf(content):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=11)

    text = content.encode("latin-1", "replace").decode("latin-1")

    pdf.multi_cell(
        0,
        8,
        text
    )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    pdf.output(temp_file.name)

    return temp_file.name

# =========================
# BUTTONS
# =========================

resume_col, cover_col, portfolio_col = st.columns(3)

# =========================
# RESUME GENERATOR
# =========================

with resume_col:

    if st.button("Generate Resume"):

        prompt = f"""
You are an expert resume writer.

Create a COMPLETE professional ATS-friendly resume.

DO NOT give instructions.
DO NOT explain anything.
DO NOT ask questions.
DO NOT provide a template.

Output ONLY the final resume.

Name: {name}
Email: {email}
Phone: {phone}

Target Job Role:
{target_role}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Certifications:
{certifications}

Career Objective:
{career_objective}

The resume must contain:

1. Header with contact information
2. Professional Summary
3. Education
4. Technical Skills
5. Projects
6. Experience
7. Certifications

Make it professional and job-ready.
"""

        try:

            with st.spinner("Generating Resume..."):

                response = model.generate_content(prompt)

                resume = response.text

                st.session_state["resume"] = resume

                st.subheader("Generated Resume")

                st.text_area(
                    "Resume",
                    value=resume,
                    height=600
                )

        except Exception as e:
            st.error(f"Error: {e}")

if "resume" in st.session_state:

    pdf_file = create_pdf(
        st.session_state["resume"]
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📥 Download Resume PDF",
            data=file,
            file_name="AI_Resume.pdf",
            mime="application/pdf"
        )
# =========================
# COVER LETTER GENERATOR
# =========================

with cover_col:

    if st.button("Generate Cover Letter"):

        prompt = f"""
Write a professional cover letter.

Name:
{name}

Target Job Role:
{target_role}

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Certifications:
{certifications}
"""

        try:

            with st.spinner("Generating Cover Letter..."):

                response = model.generate_content(prompt)

                st.subheader("Generated Cover Letter")

                st.text_area(
                    "Cover Letter",
                    value=response.text,
                    height=500
                )

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# PORTFOLIO SUMMARY GENERATOR
# =========================

with portfolio_col:

    if st.button("Generate Portfolio Summary"):

        prompt = f"""
Create a professional portfolio summary.

Name:
{name}

Education:
{education}

Skills:
{skills}

Projects:
{projects}

Experience:
{experience}

Certifications:
{certifications}

Target Job Role:
{target_role}
"""

        try:

            with st.spinner("Generating Portfolio Summary..."):

                response = model.generate_content(prompt)

                st.subheader("Portfolio Summary")

                st.text_area(
                    "Portfolio Summary",
                    value=response.text,
                    height=500
                )

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "Developed using Streamlit + Google Gemini AI"
)