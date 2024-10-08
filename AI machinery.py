from flask import Flask, render_template, request, redirect, url_for, session
import python_avatars as pa
import os

app = Flask(__name__)
app.secret_key = 'shellhacks'  # Set a secret key for session management


questions = {
    "initial": {
        "question": "Which area of technology interests you the most?",
        "options": [
            {"answer": "Software Development", "next": "programming_languages"},
            {"answer": "Data Science", "next": "data_analysis"},
            {"answer": "Cybersecurity", "next": "security_questions"},
        ]
    },
    "programming_languages": {
        "question": "What programming languages are you most interested in learning?",
        "options": [
            {"answer": "Python", "next": "programming_tools"},
            {"answer": "JavaScript", "next": "programming_tools"},
            {"answer": "Java", "next": "programming_tools"},
            {"answer": "C++", "next": "programming_tools"},
        ]
    },
    "data_analysis": {
        "question": "What type of data analysis are you interested in?",
        "options": [
            {"answer": "Statistical Analysis", "next": "data_tools"},
            {"answer": "Machine Learning", "next": "data_tools"},
            {"answer": "Data Visualization", "next": "data_tools"},
        ]
    },
    "security_questions": {
        "question": "What aspect of cybersecurity interests you?",
        "options": [
            {"answer": "Network Security", "next": "security_tools"},
            {"answer": "Application Security", "next": "security_tools"},
            {"answer": "Ethical Hacking", "next": "security_tools"},
        ]
    },
    "programming_tools": {
        "question": "Which programming tools are you most comfortable with?",
        "options": [
            {"answer": "Git", "next": "results"},
            {"answer": "VSCode", "next": "results"},
            {"answer": "IntelliJ", "next": "results"},
        ]
    },
    "data_tools": {
        "question": "Which data analysis tools are you most comfortable with?",
        "options": [
            {"answer": "R", "next": "results"},
            {"answer": "Excel", "next": "results"},
            {"answer": "Tableau", "next": "results"},
        ]
    },
    "security_tools": {
        "question": "Which cybersecurity tools are you most comfortable with?",
        "options": [
            {"answer": "Wireshark", "next": "results"},
            {"answer": "Burp Suite", "next": "results"},
            {"answer": "Metasploit", "next": "results"},
        ]
    },
}

def determine_major(responses):
    if "Software Development" in responses:
        return "Computer Science"
    elif "Data Science" in responses:
        return "Data Science"
    elif "Cybersecurity" in responses:
        return "Cybersecurity"
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Create an avatar
        avatar = pa.Avatar(
            style=pa.AvatarStyle.CIRCLE,
            background_color="#f0f8ff",  # Light blue background
            top=pa.HairType.STRAIGHT_2,
            hair_color=pa.HairColor.BROWN,
            eyebrows=pa.EyebrowType.RAISED_EXCITED,
            eyes=pa.EyeType.HAPPY,
            nose=pa.NoseType.DEFAULT,
            mouth=pa.MouthType.SMILE,
            skin_color=pa.SkinColor.LIGHT,
            accessory=pa.AccessoryType.PRESCRIPTION_2,
            clothing=pa.ClothingType.COLLAR_SWEATER
        )

        # Ensure the static folder exists
        if not os.path.exists('static'):
            os.makedirs('static')

        avatar.render("static/cute_female_avatar.svg")
        return render_template('index.html')
    except Exception as e:
        return f"An error occurred: {e}"



@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    session.clear()  # Clear session on the main page to restart the quiz
    if request.method == 'POST':
        user_response = request.form.get('initial')
        if user_response:
            # Store the user's response in session
            session['responses'] = [user_response]
            next_question = next(
                (opt['next'] for opt in questions['initial']['options'] if opt['answer'] == user_response), None)
            if next_question:
                return redirect(url_for('question', question_name=next_question))

    return render_template('quiz.html', questions=questions['initial'])


@app.route('/question/<question_name>', methods=['GET', 'POST'])
def question(question_name):
    question_data = questions.get(question_name)

    if not question_data:
        return redirect(url_for('results'))  # Safeguard in case of an invalid question

    if request.method == 'POST':
        answer = request.form.get('answer')

        # Retrieve responses from session and update with the new answer
        responses = session.get('responses', [])
        responses.append(answer)
        session['responses'] = responses

        # Determine the next question or redirect to results
        next_question = next(
            (opt['next'] for opt in question_data['options'] if opt['answer'] == answer), "results"
        )

        if next_question in questions:
            return redirect(url_for('question', question_name=next_question))
        else:
            # Redirect to results, passing the recommended major
            recommended_major = determine_major(responses)
            return redirect(url_for('results', tech_interest=recommended_major))

    return render_template('question.html', question=question_data['question'], options=question_data['options'])


@app.route('/results/<tech_interest>')
def results(tech_interest):
    return render_template('results.html', tech_interest=tech_interest)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
