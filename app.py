import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title= "Resume Analyzer", layout="centered")

st.title("Resume Analyzer")
st.subheader("Upload your resume to check for essential tech skills!")

keywords = ["Python", "C", "C++", "SQL", "Git", "GitHub", "AWS", "Cloud", "Excel", "Machine Learning", "Linux", "IoT"]

uploaded_file= st.file_uploader("Upload your resume (PDF format only)", type="pdf")

if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        full_text =""
        for page in pdf_reader.pages:
            text = page.extract_text()  # <-- FIXED: add () to extract_text
            if text:
                full_text += text
        found = [kw for kw in keywords if re.search(rf"\b{kw}\b", full_text, re.IGNORECASE)]
        missing = [kw for kw in keywords if kw not in found]
        score =len(found)/ len(keywords)*100

        st.success("Resume analyzed successfully!")
        st.write(f"** Total Pages:**{len(pdf_reader.pages)}")
        st.write(f"** Found Skills:**{', '.join(found)if found else 'None'}")
        st.write(f"** Missing Skills:**{', '.join(missing)if missing else 'None'}")
        st.write(f"** Resume Score:**{round(score, 2)}/100")

        if score <50:
            st.warning("Try adding more relevant skills to your resume.")
        else:
            st.success("Great Job! Your resume covers many important skills.")
         
        
    except Exception as e:
        st.error(f"Something went wrong while reading the file: {e}")
