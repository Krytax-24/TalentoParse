from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher
import re

from resume_parser import (
    extract_text_from_pdf,
    extract_contact_number_from_resume,
    extract_email_from_resume,
    extract_skills_from_resume,
    extract_education_from_resume,
    extract_name
)

app = Flask(__name__)

@app.route('/extract_resume_info', methods=['POST'])
def extract_resume_info():
    # Get the uploaded resume file
    resume_file = request.files['resume']

    # Save the file to a temporary location
    temp_path = 'temp_resume.pdf'
    resume_file.save(temp_path)

    # Extract text from the resume
    resume_text = extract_text_from_pdf(temp_path)

    # Extract information from the resume text
    skill_pattern = "jz_skill_patterns.jsonl"
    name = extract_name(resume_text)
    contact_number = extract_contact_number_from_resume(resume_text)
    email = extract_email_from_resume(resume_text)
    extracted_skills = extract_skills_from_resume(resume_text, skill_pattern)
    education = extract_education_from_resume(resume_text)

    # Prepare the response
    response = {
        'name': name,
        'contact_number': contact_number,
        'email': email,
        'skills': extracted_skills,
        # 'education': education
    }

    # Return the response as JSON
    return jsonify(response)

if __name__ == '__main__':
    app.run()
