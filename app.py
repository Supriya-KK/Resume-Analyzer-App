import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title= "Resume Analyzer", layout="centered", page_icon="📄" )
dark_mode=st.toggle ("🌙 Enable Dark mode")
if dark_mode:
    st.markdown("""
        <style>
        .main {
            background-color: #121212;
            color: #eeeeee
        }
    </style>   

""", unsafe_allow_html=True)


#Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .stFileUploader {
            border: 2px dashed #4a90e2;
            padding: 10px;
            background-color: #ffffff;
        }
        .title-style {
            font-size:40px;
            color: #4a90e2;
            font-weight: bold;
            text-align: center;

        }
        .subheader-style{
            font-size:20px;
            color: #333;
            text-align: center;
        }
     </style>   

""", unsafe_allow_html=True)

st.markdown('<div class="title-style">📄 Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader-style"> Upload your resume to check for essential tech skills! </div>', unsafe_allow_html=True)
st.markdown("---")

keywords = ["Python", "C", "C++", "SQL", "Git", "GitHub", "AWS", "Cloud", "Excel", "Machine Learning", "Linux", "IoT"]

uploaded_file= st.file_uploader("📎 Upload your resume (PDF format only)", type="pdf")

if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        full_text =""
        for page in pdf_reader.pages:
            text = page.extract_text()  # <-- FIXED: add () to extract_text
            if text:
                full_text += text
        with st.expander("Preview Extracted Resume Text"):
            st.text(full_text)
        
        found = [kw for kw in keywords if re.search(rf"\b{kw}\b", full_text, re.IGNORECASE)]
        missing = [kw for kw in keywords if kw not in found]
        score =len(found)/ len(keywords)*100

        col1, col2= st.columns(2)
        col1.metric("📄 Total Pages", len(pdf_reader))
        col2.metric("📈Resume Score", f"{round(score, 2)} / 100")
        st.progress(int(score))

        st.success("Resume analyzed successfully!")
    
        st.markdown("### ✅ Found Skills: ")
        st.write(", ".join(found)if found else "None")
        st.markdown("### Missing Skills: ")
        st.write(", ".join(missing)if missing else "None")
        

        if score <50:
            st.warning("Try adding more relevant skills to your resume.")
        else:
            st.success("Great Job! Your resume covers many important skills.")
         
        
    except Exception as e:
        st.error(f"Something went wrong while reading the file: {e}")


