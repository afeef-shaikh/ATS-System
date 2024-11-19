# ATS Resume Analyzer

The **ATS Resume Analyzer** is an intuitive tool designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By uploading a resume and providing a job description, this application analyzes how well the resume matches the job criteria and gives suggestions for improvement.

## Features
- Upload a resume (in PDF format) and input a job description.
- Automatically analyze the content of your resume against the job description.
- Receive detailed feedback with suggestions for improving your resume to match ATS requirements.
- Easy-to-use interface built with Streamlit and Python.

## Requirements

To run the application, make sure you have the following installed:
- Python 3.10
- Required Python libraries (listed in `requirements.txt`)

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/afeef-shaikh/ATS-System.git

2. **Navigate into the project directory**:
  cd ATS-System

3. **Install the required dependencies**:
  pip install -r requirements.txt

4. **Create a .env file in the project’s root directory and add your API keys**:
  API_KEY=your-api-key-here

5. **Run the application**:
  streamlit run app.py


## How It Works

1. **Upload Your Resume**  
   Select your resume in PDF format by clicking the "Upload Resume" button.

2. **Enter the Job Description**  
   Paste the job description into the provided text area.

3. **Analyze the Resume**  
   Click the "Tell me about the Resume" button to start the analysis. The application will process both the resume and job description and generate an analysis report.

4. **Review Insights**  
   The report will suggest ways to improve your resume based on ATS compatibility and how well it matches the job description.

---

## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Python**: For backend processing and logic implementation.
- **Generative AI API**: To process the resume and job description, providing detailed insights.


## Contact:
For questions or feedback, feel free to reach out to me at achiever.afeef04@gmail.com.

Feel free to customize it further depending on specific needs or changes in your project.


