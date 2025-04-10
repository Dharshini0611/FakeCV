from flask import Flask, request, jsonify
import subprocess
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to call generate_questions.py and get questions
def get_generated_questions():
    result = subprocess.run(["python", "generate_questions.py"], capture_output=True, text=True)
    return json.loads(result.stdout)["questions"]

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req["queryResult"]["intent"]["displayName"]
    session_id = req["session"]

    if intent == "Start_Interview":
        questions = get_generated_questions()  # Get generated questions
        response_text = f"Let's start the interview! Here's your first question: {questions[0]}"
        
        return jsonify({
            "fulfillmentText": response_text,
            "outputContexts": [
                {
                    "name": f"{session_id}/contexts/interview",
                    "lifespanCount": 5,
                    "parameters": {"questions": questions, "current_question_index": 0}
                }
            ]
        })

    elif intent == "Next_Question":
        context = req["queryResult"].get("outputContexts", [{}])[0]
        questions = context.get("parameters", {}).get("questions", [])
        current_question_index = context.get("parameters", {}).get("current_question_index", 0)

        next_question_index = current_question_index + 1
        if next_question_index < len(questions):
            response_text = questions[next_question_index]
            return jsonify({
                "fulfillmentText": response_text,
                "outputContexts": [
                    {
                        "name": f"{session_id}/contexts/interview",
                        "lifespanCount": 5,
                        "parameters": {"questions": questions, "current_question_index": next_question_index}
                    }
                ]
            })
        else:
            return jsonify({"fulfillmentText": "That concludes our interview. Thank you for your time!"})

    return jsonify({"fulfillmentText": "I'm not sure how to respond to that."})

if __name__ == '__main__':
    app.run(port=80, debug=True)
