import streamlit as st
import os
import io
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import PyPDF2 as pdf



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text


def input_pdf_setup(uploaded_file):
  if uploaded_file is not None:
      pdf_reader = pdf.PdfReader(uploaded_file)
      pdf_text = ""
      for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          pdf_text += page.extract_text()

      return pdf_text
  else:
        raise FileNotFoundError("No file uploaded")


# Streamlit App Configuration
st.set_page_config(page_title="Resume Advisor")

# Navigation Bar with Tabs
navigation = st.sidebar.title("Select Role")
navigation = st.header("RESUME ADVISOR")
selected_tab = st.sidebar.radio("", ["HR", "Applicant"])


## Content based on Selected Role
if selected_tab == "HR":
    st.header("HR - Resume Advisor")
    input_text = st.text_area("Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

    # Function to display success message and buttons for HR
    def display_buttons_hr():
        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")

        submit1 = st.button("Resume Summary")
        submit2 = st.button("Percentage Match")
        return {
            "submit1": submit1,
            "submit2": submit2
        }


    # Function to display response based on button clicked for HR
    def show_response_hr(buttons, input_prompts):
        if buttons["submit1"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Added progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["HR_Summary"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Resume Summary' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)

        elif buttons["submit2"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Added progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["HR_Match"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Percentage Match' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)

        else:
            if uploaded_file is None:
                st.write("Please upload the resume")

    buttons_hr = display_buttons_hr()
    input_prompts = {
        "HR_Summary": """
            You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
            Please share your professional evaluation on whether the candidate's profile aligns with the role. 
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """,
        "HR_Match": """
            You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
            your task is to evaluate the resume against the provided job description. Give me the percentage match if the resume matches
            the job description. First, the output"""
    }
    show_response_hr(buttons_hr, input_prompts)
                 
                 
                 
             #################------------------###############


if selected_tab == "Applicant":
    st.header("Applicant - Resume Advisor")
    input_text = st.text_area("Job Description:", key="input")
    uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

    # Function to display success message and buttons for HR
    def display_buttons_app():
        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")

        submit3 = st.button("How to improve ")
        return {
            "submit3": submit3,
        }


    # Function to display response based on button clicked for HR
    def show_response_app(buttons, input_prompts):
        if buttons["submit3"] and uploaded_file is not None:
            with st.spinner("Generating response..."):  # Added progress bar
                pdf_text = input_pdf_setup(uploaded_file)
                try:
                    response = get_gemini_response(input_prompts["APP_IMP"], pdf_text, input_text)
                except KeyError:
                    st.error("Prompt for 'Improvement' not found. Please check the code.")
                    return
                st.subheader("The Response is")
                st.write(response)

        
        else:
            if uploaded_file is None:
                st.write("Please upload the resume")

    buttons_app = display_buttons_app()
    input_prompts = {
        "APP_IMP": """
            You are an experienced technical human resource manager your task is to review the provided resume(PDF) againts the job desciption and  Tell what points to be improved by compairing the resume with job description only, what skills are missing, what should be the improvement. First mention what are the missing skills,
 and then what skills to be added in the resume, tell how to improve it."""
        
    }
    show_response_app(buttons_app, input_prompts )


