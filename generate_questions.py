import json
from random import choice

def generate_questions(resume_data):
    """Generate a concise list of interview questions based on resume details."""
    questions = []
    
    # Greeting the user
    user_name = resume_data.get("name", "Candidate")
    print(f"\n👋 Hello {user_name}, welcome to your interview!\n")
    print("Let's start the interview. Here are your questions:\n")

    # Experience-Based Questions
    if resume_data["experience"] and resume_data["experience"][0] != "Not found":
        questions.append(f"Can you describe your role at {resume_data['experience'][0]}?")
    
    # Project-Based Questions
    if resume_data["projects"] and resume_data["projects"][0] != "Not found":
        questions.append(f"What challenges did you face while working on {resume_data['projects'][0]}?")
    
    # Skill-Based Questions (Limit to 2)
    skill_questions = {
        "python": ["How do you handle exceptions in Python?"],
        "java": ["Can you explain multithreading in Java?"],
        "c++": ["What are smart pointers in C++?"],
        "sql": ["How would you optimize a slow SQL query?"],
        "machine learning": ["How do you evaluate the performance of an ML model?"],
        "django": ["What is Django ORM?"]
    }

    skill_count = 0
    for skill in resume_data["skills"]:
        normalized_skill = skill.lower()
        if normalized_skill in skill_questions:
            questions.append(choice(skill_questions[normalized_skill]))
            skill_count += 1
            if skill_count >= 2:
                break

    # Certification-Based Question (Limit to 1)
    if resume_data["certifications"] and resume_data["certifications"][0] != "Not found":
        questions.append(f"What key insights did you gain from your {resume_data['certifications'][0]} certification?")
    
    # Behavioral Questions (Limit to 2)
    questions.append("Describe a major challenge you faced and how you overcame it.")
    questions.append("Tell me about a time you had to meet a tight deadline. How did you manage it?")
    
    return questions

def save_questions(questions):
    """Save questions to a JSON file for further use."""
    with open("interview_questions.json", "w") as file:
        json.dump(questions, file, indent=4)

def main():
    """Load resume data and generate interview questions dynamically."""
    try:
        with open("resume_data.json", "r") as file:
            resume_data = json.load(file)
    except FileNotFoundError:
        print("❌ Error: resume_data.json not found!")
        return
    
    questions = generate_questions(resume_data)
    save_questions(questions)

    # Display questions
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")

if __name__ == "__main__":
    main()