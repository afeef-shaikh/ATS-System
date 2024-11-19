import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)  # Reads the PDF file
    text = ""
    for page_index in range(len(reader.pages)):  # Handles multiple pages
        page = reader.pages[page_index]
        text += str(page.extract_text())
    return text

# Create a circular progress bar for percentage match
def create_progress_icon(percentage):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.pie(
        [percentage, 100 - percentage],
        startangle=90,
        colors=['#00cc44', '#e6e6e6'],
        wedgeprops=dict(width=0.3, edgecolor='w'),
    )
    plt.gcf().gca().add_artist(plt.Circle((0, 0), 0.7, color='black'))
    plt.text(0, 0, f"{percentage}%", ha='center', va='center', fontsize=14, color='white')
    plt.axis('equal')
    st.pyplot(fig)

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide 
best assistance for improving resumes. Assign the percentage Matching based 
on the JD and
list the important missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":"", "Suggestions":""}}
"""

# Streamlit App
st.title("📋 Smart ATS: Optimize Your Resume for Success")
st.markdown(
    """
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stTextArea textarea {
            border-radius: 10px;
            font-family: 'Arial', sans-serif;
        }
        .stFileUploader div {
            border-radius: 10px;
        }
        
        
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.text("🤖 Improve Your Resume for ATS Compatibility")
jd = st.text_area("📄 Paste the Job Description", height=150, help="Enter the job description here.")
uploaded_file = st.file_uploader(
    "📁 Upload Your Resume (PDF Format)",
    type="pdf",
    help="Please upload your resume in PDF format.",
)

submit = st.button("✨ Analyze My Resume")

st.markdown("</div>", unsafe_allow_html=True)

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)  # Extract text from the uploaded PDF
        
        if not jd:
            st.error("Please paste the job description.")
        else:
            # Format the prompt with the resume text and job description
            formatted_prompt = input_prompt.format(text=text, jd=jd)
            
            try:
                # Call the API with the formatted prompt
                response = get_gemini_response(formatted_prompt)
                
                # Parse the JSON response
                response_data = eval(response)  # Ensure the response is in JSON format
                match_percentage = int(response_data["JD Match"].strip('%'))
                missing_keywords = response_data["MissingKeywords"]
                profile_summary = response_data["Profile Summary"]
                suggestions = response_data.get("Suggestions", "No suggestions provided.")
                
                # Display the results
                st.subheader("Analysis Result")
                
                # Job Match Percentage
                st.markdown("### Job Match Percentage")
                create_progress_icon(match_percentage)
                
                # Missing Keywords
                st.markdown("### Missing Keywords")
                if missing_keywords:
                    st.write(", ".join(missing_keywords))
                else:
                    st.write("No missing keywords found!")
                
                # Profile Summary
                st.markdown("### Profile Summary")
                st.write(profile_summary)

                # Suggestions
                st.markdown("### Suggestions for Improvement")
                st.write(suggestions)
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please upload a PDF resume.")
