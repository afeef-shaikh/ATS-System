from dotenv import load_dotenv

load_dotenv()

from dotenv import load_dotenv
import base64   
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_base64, prompt):
    try:
        # Concatenate all inputs into a single string
        content = f"Job Description: {input_text}\n\nResume Image (Base64): {pdf_base64}\n\nPrompt: {prompt}"
        
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([content])
        return response.text
    except Exception as e:
        st.error(f"Error with Gemini API: {e}")
        return None

def input_pdf_setup(uploaded_file):
    try:
        # Convert the uploaded PDF to image(s)
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        # Take the first page and convert it to bytes
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode to base64
        return base64.b64encode(img_byte_arr).decode()
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("Application Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for actions
submit1 = st.button("Tell me about the resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager with expertise in evaluating candidates for tech roles. 
Your task is to assess the provided resume in the context of the given job description for the specified role.

Please provide a comprehensive and professional evaluation, including:

1. An analysis of how well the candidate's experience, skills, and qualifications align with the job requirements.
2. A detailed list of the candidate’s strengths and how they match the role's demands.
3. An objective assessment of the candidate's weaknesses or areas where they may not fully meet the job criteria.
4. Any specific recommendations for the candidate to improve or gain qualifications that would strengthen their candidacy.

Ensure that your response is detailed, well-structured, and concise, highlighting key aspects of the resume relevant 
to the position. Avoid generic or superficial comments, and provide actionable feedback where applicable.

"""


input_prompt2 = """
You are an advanced ATS (Applicant Tracking System) scanner with an in-depth understanding of how ATS software evaluates resumes. Your task is to assess the provided resume against the job description in a structured and insightful manner.

1. **Match Percentage**: Begin by providing a precise percentage that indicates how closely the resume matches the job description.
2. **Missing Keywords**: Next, identify and list key skills, qualifications, or terms that are present in the job description but are missing from the resume. Be specific about the relevance of these keywords to the role.
3. **Final Assessment**: Conclude with a detailed analysis of the candidate’s suitability for the position. Highlight strengths, weaknesses, and any areas where the resume can be improved for a better match to the job description. Offer suggestions for enhancement if applicable.

Your response should be clear, well-structured, and focused on actionable insights. Ensure the evaluation reflects both technical and qualitative aspects of the resume against the job description.

"""

if submit1 and uploaded_file:
    pdf_base64 = input_pdf_setup(uploaded_file)
    if pdf_base64:
        response = get_gemini_response(input_text, pdf_base64, input_prompt1)
        st.subheader("The response is:")
        st.write(response)

elif submit3 and uploaded_file:
    pdf_base64 = input_pdf_setup(uploaded_file)
    if pdf_base64:
        response = get_gemini_response(input_text, pdf_base64, input_prompt2)
        st.subheader("The response is:")
        st.write(response)

else:
    st.write("Upload a PDF resume and provide a job description to evaluate.")