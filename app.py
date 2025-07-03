import streamlit as st
import PyPDF2
import re
import base64


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_img_as_base64("images.jpg")


st.set_page_config(page_title="Resume Analyzer", layout="centered", page_icon="📄")


st.markdown(f"""
    <style>
        body, .main {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            color: #000000;
        }}

        .stApp {{
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 10px;
        }}

        h1, h4, .stMarkdown, .stText, .stTextInput, .stFileUploader label, .stAlert {{
            color: #000000 !important;
        }}

        .stFileUploader, .stButton>button {{
            background-color: #ffffff;
            color: #000000;
            border-radius: 10px;
            border: 1px solid #4a90e2;
        }}

        .stProgress > div > div > div > div {{
            background-image: linear-gradient(to right, #4a90e2, #6dd5fa);
        }}

        .tip-box {{
            background-color: #f1faff;
            border-left: 5px solid #4a90e2;
            padding: 1rem;
            margin-top: 1.5rem;
            border-radius: 8px;
        }}
        .stSelectbox > div[data-baseweb="select"] {{
            border-style: solid !important; border-width: 2px !important; border-color: #4a90e2 !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            padding: 5px !important;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
        }}
</style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center; margin-top: -20px; margin-bottom: 20px;'>
        <h1 style='font-size: 2.8rem; color: #000000; font-weight: bold;'>Resume Analyzer</h1>
        <h4 style='font-size: 1.3rem; color: #4a4a4a;'>
            Upload your resume <span style='color:#4a90e2;'>(PDF only)</span> to check for essential tech skills.
        </h4>
    </div>
""", unsafe_allow_html=True)


st.info("Only `.pdf` files are supported. Export your Word file as PDF before uploading.")


st.markdown("""
    ## About Resume Analyzer
    Resume Analyzer is a smart web tool designed to:
    - Extract text from your resume (PDF only)
    - Identify key tech skills
    - Score your resume based on job market demand
    - Ensure your resume stays private on your device

    **How it works:**
    1. Upload your resume
    2. The tool scans for tech skills
    3. You get a score and suggestions!

    > ⚠️ **Privacy First**: This app does not store or share your resume. All processing is done locally.
""")


field = st.selectbox(
    "Select your career field:",
    [
        "Computer Science / IT",
        "Mechanical Engineering",
        "Electrical Engineering",
        "Civil Engineering",
        "Finance",
        "Marketing",
        "HR",
        "Design",
        "Medical",
        "Other"
    ],
    index=0,
    help="This selection tailors the skill analysis based on your chosen field."
)

field_keywords = {
    "Computer Science / IT": ["Python", "C", "C++", "SQL", "Git", "GitHub", "AWS", "Cloud", "Excel", "Machine Learning", "Linux", "IoT", "Power BI", "Flask", "Django", "Data Science"],
    "Mechanical Engineering": ["AutoCAD", "SolidWorks", "MATLAB", "ANSYS", "Thermodynamics"],
    "Electrical Engineering": ["MATLAB", "Simulink", "Embedded Systems", "Power Systems", "Circuit Analysis"],
    "Civil Engineering": ["AutoCAD", "Revit", "Staad Pro", "Surveying", "Concrete Design"],
    "Finance": ["Excel", "Accounting", "Tally", "SAP", "Financial Modeling"],
    "Marketing": ["SEO", "Content Writing", "Digital Marketing", "Google Ads", "Social Media"],
    "HR": ["Recruitment", "Employee Engagement", "Payroll", "HRMS", "Interviewing"],
    "Design": ["Photoshop", "Illustrator", "Figma", "Canva", "UI/UX"],
    "Medical": ["EMR", "Patient Care", "Clinical Procedures", "Pharmacology"],
    "Other": ["Communication", "Leadership", "Teamwork", "Problem Solving"]
}

keywords = field_keywords.get(field, [])


uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                full_text += text

        with st.expander("Preview Extracted Resume Text"):
            st.text(full_text)

        
        found = [kw for kw in keywords if re.search(rf"\b{kw}\b", full_text, re.IGNORECASE)]
        missing = [kw for kw in keywords if kw not in found]
        score = len(found) / len(keywords) * 100 if keywords else 0

        st.markdown("""
            <hr style='border: 1px solid #4a90e2;'>
            <h3 style='text-align:center;'>Analysis Summary</h3>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col1.metric("Total Pages", len(pdf_reader.pages))
        col2.metric("Resume Score", f"{round(score, 2)} / 100")
        st.progress(int(score))

        st.success("Resume analyzed successfully!")

        st.markdown("### Found Skills:")
        st.write(", ".join(found) if found else "None")

        st.markdown("### Missing Skills:")
        st.write(", ".join(missing) if missing else "None")

        
        st.markdown("""
            <div class='tip-box'>
                <h4>📌 Resume Improvement Tips</h4>
                <ul>
                    <li><b>Customize</b> your resume for each job application.</li>
                    <li><b>Highlight</b> your key technical skills with examples.</li>
                    <li><b>Quantify</b> results (e.g., "Improved process efficiency by 20%").</li>
                    <li><b>Use clean formatting</b> with clear section headers.</li>
                    <li><b>Keep it honest</b> and professional—avoid buzzwords without substance.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Something went wrong while reading the file: {e}")
