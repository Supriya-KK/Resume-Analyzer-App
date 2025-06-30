# Resume-Analyzer-App (Streamlit App)
This ia a simple Python + Streamlit web app that analyzes your resume(PDF)
and highlights the skills present and missing based on trending Computer Science keywords.

# Features 
- Upload your resume (PDF)
- Automatically detects CS-related keywords like Python, SQL, AWS, etc,.
- Shows total pages, found & missing skills
- Give a score out of 100
- Begineer-friendly and easy to use!

# How to run this project
1. Clone the REpository
    '''bash
    git clone https://github.com/Supriya-KK/resume-analyzer.git (copy this from code->local->HTTPS and copy it)
    cd resume-analyzer(project folder name)

2. install required libraries
    Make sure Python is installed. Then run:
        (in bash terminal)
            pip install -r requirements.txt

    if requirements.txt is missing, you can install manually:
        pip install streamlit PyPDF2
    
3. Run the app
    '''bash
        stramlit run app.py
                OR
        python -m steamlit run app.py
    This will open the app in your browser: http://localhost:8501

