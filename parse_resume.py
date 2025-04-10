import os
import json
import pdfplumber
import docx
import re

UPLOAD_DIR = "C:\\xampp\\htdocs\\file_upload_download\\uploads"

# Skill Set
SKILL_SET = {
    "python", "java", "c++", "sql", "django", "machine learning", "ai",
    "javascript", "react", "node.js", "html", "css", "typescript",
    "flutter", "swift", "kotlin", "c#", ".net", "angular",
    "tensorflow", "pytorch", "data science", "nlp", "cloud computing",
    "aws", "azure", "google cloud", "docker", "kubernetes",
    "git", "linux", "bash", "cybersecurity", "networking", "uiux"
}

# Common Languages
LANGUAGE_SET = {
    "english", "tamil", "french", "german", "chinese", "mandarin",
    "hindi", "bengali", "portuguese", "russian", "japanese", "korean",
    "arabic", "italian", "dutch", "telugu", "vietnamese"
}

# Education Keywords
EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "associate", "diploma", "degree",
    "university", "college", "b.tech", "senior secondary", "secondary"
]

def get_latest_file(directory):
    """Fetch the latest uploaded resume file."""
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return max(files, key=os.path.getctime) if files else None
    except Exception as e:
        print(f"❌ Error accessing directory: {e}")
        return None

def extract_text(file_path):
    """Extract text from a PDF or DOCX file."""
    try:
        if file_path.endswith(".pdf"):
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs).strip()
        else:
            print("❌ Unsupported file format.")
            return None
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        return None

def extract_name(text):
    """Extract the candidate's name from the resume text."""
    lines = text.split("\n")
    for line in lines:
        words = line.split()
        if len(words) >= 2 and not any(keyword in line.lower() for keyword in ["email", "phone", "resume", "cv"]):
            return line
    return "Not found"

def extract_skills(text):
    """Extract technical skills from the resume."""
    words = set(re.findall(r'\b[a-zA-Z0-9+#.]+\b', text.lower()))  
    return sorted({skill for skill in SKILL_SET if skill.lower() in words}) or ["Not found"]

def extract_languages(text):
    """Extract spoken languages from the resume."""
    words = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))  
    return sorted({lang for lang in LANGUAGE_SET if lang.lower() in words}) or ["Not found"]

def extract_certifications(text):
    """Extract certifications from the resume."""
    certs = re.findall(r'(?i)(Certified\s+\w+|AWS\s+Certified\s+\w+|Microsoft\s+Certified\s+\w+|Google\s+Cloud\s+Certified\s+\w+|Cisco\s+Certified\s+\w+|PMP|Scrum\s+Master|Six\s+Sigma)', text)
    return sorted(set(certs)) or ["Not found"]

def extract_education(text):
    """Extract education details and CGPA/GPA if available."""
    education_matches = re.findall(r'(?i)(bachelor|master|phd|diploma|associate)\s+of\s+\w+|university\s+of\s+\w+|college\s+of\s+\w+', text)
    cgpa_matches = re.findall(r'(?i)CGPA[:\s]*([\d.]+)|GPA[:\s]*([\d.]+)', text)

    cgpa_values = [float(cgpa) for match in cgpa_matches for cgpa in match if cgpa]
    avg_cgpa = sum(cgpa_values) / len(cgpa_values) if cgpa_values else None

    return {
        "degrees": sorted(set(education_matches)) or ["Not found"],
        "cgpa": avg_cgpa if avg_cgpa else "Not found"
    }

def extract_experience(text):
    """Extract experience roles from the resume."""
    return re.findall(r'(?i)(\w+ Engineer|Developer|Manager|Intern)[^\n]*', text) or ["Not found"]

def extract_projects(text):
    """Extract projects from the resume."""
    return re.findall(r'(?i)Project[^\n]*', text) or ["Not found"]

def calculate_score(skills, experience, certifications, education_data):
    """Calculate a score based on extracted resume details."""
    score = 0

    score += min(len(skills) * 5, 30)  # Max 30 points
    score += min(len(experience) * 10, 30)  # Max 30 points
    score += min(len(certifications) * 5, 20)  # Max 20 points

    if education_data["cgpa"] != "Not found":
        cgpa = education_data["cgpa"]
        if cgpa >= 9:
            score += 20  # Max 20 points
        elif cgpa >= 8:
            score += 15
        elif cgpa >= 7:
            score += 10
        elif cgpa >= 6:
            score += 5

    return min(score, 100)  # Cap at 100

def parse_resume(file_path):
    """Parse the resume and extract relevant details."""
    text = extract_text(file_path)
    if not text:
        print("❌ No text extracted.")
        return None

    resume_data = {
        "name": extract_name(text),
        "email": next(iter(re.findall(r'[\w\.-]+@[\w\.-]+', text)), "Not found"),
        "phone": next(iter(re.findall(r'\+?\d[\d\s\-\(\)]{8,15}\d', text)), "Not found"),
        "skills": extract_skills(text),
        "languages": extract_languages(text),
        "certifications": extract_certifications(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "score": calculate_score(extract_skills(text), extract_experience(text), extract_certifications(text), extract_education(text))
    }
    
    return resume_data

def main():
    """Main function to process the latest resume."""
    file_path = get_latest_file(UPLOAD_DIR)
    
    if not file_path:
        print("❌ No resume file found.")
        return
    
    print(f"📂 Parsing Resume: {file_path}")
    
    resume_data = parse_resume(file_path)

    if resume_data:
        print("✅ Extracted Resume Data:")
        print(json.dumps(resume_data, indent=4))
        output_file = "resume_data.json"
        with open(output_file, "w") as file:
            json.dump(resume_data, file, indent=4)
        print(f"📡 Resume data saved to {output_file}!")

if __name__ == "__main__":
    main()
