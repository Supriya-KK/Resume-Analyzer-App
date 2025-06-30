import streamlit as st
import PyPDF2
import re

# ------------------------ Page Setup ------------------------
st.set_page_config(page_title="Resume Analyzer", layout="centered", page_icon="📄")

# ------------------------ Gradient Background Styling ------------------------
st.markdown("""
    <style>
        body, .main {
            background: linear-gradient(to right, #e0eafc, #cfdef3);
            color: #000000;
        }

        h1, h4, .stMarkdown, .stText, .stTextInput, .stFileUploader label, .stAlert {
            color: #000000 !important;
        }

        .stFileUploader, .stButton>button {
            background-color: #ffffff;
            color: #000000;
            border-radius: 10px;
            border: 1px solid #4a90e2;
        }

        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #4a90e2, #6dd5fa);
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------ Header ------------------------
st.markdown("""
    <div style='text-align: center; margin-top: -20px; margin-bottom: 20px;'>
        <h1 style='font-size: 2.8rem; color: #000000; font-weight: bold;'>📄 Resume Analyzer</h1>
        <h4 style='font-size: 1.3rem; color: #4a4a4a;'>
            🔍 Upload your resume <span style='color:#4a90e2;'>(PDF only)</span> to check for essential tech skills!
        </h4>
    </div>
""", unsafe_allow_html=True)

# ------------------------ Upload Info ------------------------
st.info("💡 Only `.pdf` files are supported. Export your Word file as PDF before uploading.")

# ------------------------ Keywords ------------------------
keywords = [
    "Python", "C", "C++", "SQL", "Git", "GitHub", "AWS", "Cloud", "Excel",
    "Machine Learning", "Linux", "IoT", "Power BI", "Flask", "Django", "Data Science"
]

# ------------------------ File Upload ------------------------
uploaded_file = st.file_uploader("📁 Upload your resume (PDF only)", type=None)

if uploaded_file is not None:
    if uploaded_file.type != "application/pdf":
        st.error("❌ Invalid file type! Please upload a `.pdf` file only.")
    else:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            full_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text

            with st.expander("📝 Preview Extracted Resume Text"):
                st.text(full_text)

            # ------------------------ Skill Match ------------------------
            found = [kw for kw in keywords if re.search(rf"\\b{kw}\\b", full_text, re.IGNORECASE)]
            missing = [kw for kw in keywords if kw not in found]
            score = len(found) / len(keywords) * 100

            # ------------------------ Results Display ------------------------
            st.markdown("""
                <hr style='border: 1px solid #4a90e2;'>
                <h3 style='text-align:center;'>📊 Analysis Summary</h3>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("📄 Total Pages", len(pdf_reader.pages))
            col2.metric("📊 Resume Score", f"{round(score, 2)} / 100")
            st.progress(int(score))

            st.success("✅ Resume analyzed successfully!")

            st.markdown("### ✅ Found Skills:")
            st.write(", ".join(found) if found else "None")

            st.markdown("### ❌ Missing Skills:")
            st.write(", ".join(missing) if missing else "None")

            if score < 50:
                st.warning("⚠️ Try adding more relevant skills to your resume.")
            else:
                st.success("🎉 Great Job! Your resume covers many important skills.")

        except Exception as e:
            st.error(f"⚠️ Something went wrong while reading the file: {e}")
