from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
import os
import re

# Initialize Flask App
app = Flask(__name__)

# Folder where resumes will be stored
UPLOAD_FOLDER = 'resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to extract text from PDF
def extract_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to generate intelligent questions based on resume content
def generate_questions(text):
    text_lower = text.lower()
    questions = []

    # 🎓 Education-based questions
    if "bachelor" in text_lower or "b.tech" in text_lower or "degree" in text_lower or "graduated" in text_lower:
        questions.append("Where did you complete your graduation?")
        questions.append("What was your major or specialization in college?")
        questions.append("Did you participate in any extracurricular activities during your studies?")

    if "12th" in text_lower or "intermediate" in text_lower or "high school" in text_lower:
        questions.append("Which school did you attend for your 12th grade or high school?")
    
    if "10th" in text_lower:
        questions.append("Which school did you attend for your 10th grade?")

    # 🏆 Achievement-based questions
    if "achievement" in text_lower or "awarded" in text_lower or "won" in text_lower or "certified" in text_lower:
        questions.append("Can you tell me about one of your biggest achievements?")
        questions.append("Have you received any awards or recognitions?")
        questions.append("Do you hold any certifications? How did you earn them?")

    # 💼 Work Experience-related
    if "experience" in text_lower or "worked at" in text_lower:
        questions.append("Can you elaborate on your work experience?")
        matches = re.findall(r"(worked at|experience at|intern at) (.+?)(\.|\n)", text_lower)
        for match in matches:
            company = match[1].strip()
            questions.append(f"What was your role at {company}?")

    # 🧑‍💼 Internship-related
    if "internship" in text_lower or "intern at" in text_lower:
        questions.append("Tell me more about your internship experience.")
        matches = re.findall(r"intern(ship)? at (.+?)(\.|\n)", text_lower)
        for match in matches:
            company = match[1].strip()
            questions.append(f"What were your responsibilities as an intern at {company}?")

    # 🔧 Project-related questions
    if "project" in text_lower:
        questions.append("Can you describe a project that you're proud of?")
        questions.append("What challenges did you face during your projects?")
        questions.append("Which technologies did you use in your projects?")

    # 🛠️ Skills-based questions
    skills = {
        "python": "Can you describe a project where you used Python?",
        "java": "What Java applications have you built?",
        "sql": "How have you used SQL in your work?",
        "machine learning": "Which ML models have you implemented?",
        "data analysis": "How do you approach data analysis tasks?",
        "react": "Have you worked with React on any projects?",
        "c++": "What have you built using C++?",
        "django": "Have you created any web apps using Django?"
    }

    for skill, question in skills.items():
        if skill in text_lower:
            questions.append(question)

    # 🧠 Soft Skills or General Questions
    questions.append("What are your strengths and how do they help in your work?")
    questions.append("Are you comfortable working in a team?")
    questions.append("Where do you see yourself in the next 2 years?")

    # 📌 If no key info found
    if len(questions) < 5:
        questions.append("Can you walk me through your resume?")
        questions.append("What is something you're passionate about?")

    return questions

# Route to render HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and response
@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text(filepath)
    questions = generate_questions(text)
    return jsonify({"questions": questions})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

