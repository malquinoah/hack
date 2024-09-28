from flask import Flask, render_template, request, redirect, url_for
import python_avatars as pa
import os

app = Flask(__name__)

questions = [
    {
        "question": "Which area of technology interests you the most?",
        "options": [
            "Software Development",
            "Data Science",
            "Cybersecurity",
            "Network Engineering",
            "User Experience (UX) Design"
        ]
    },
    {
        "question": "What programming languages are you most interested in learning?",
        "options": [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "None"
        ]
    },
    {
        "question": "What type of projects do you enjoy working on?",
        "options": [
            "Web Development",
            "Mobile App Development",
            "Data Analysis",
            "System Security",
            "Designing User Interfaces"
        ]
    },
    {
        "question": "How do you prefer to work?",
        "options": [
            "Team",
            "Independently"
        ]
    },
    {
        "question": "What motivates you to pursue a career in tech?",
        "options": [
            "Solving complex problems",
            "Creating innovative solutions",
            "Analyzing data",
            "Designing user-friendly applications"
        ]
    }
]

common_opportunities = {
    ("The Women In Tech Conference (WITCON)",
     "https://wicsfiu.github.io/witcon2024/"): "A conference focused on empowering women in technology through networking and skill-building workshops.",
    ("Shellhacks",
     "https://shellhacks2024.devpost.com"): "A hackathon that brings together students to create innovative solutions.",
    ("Break Through Tech Sprinternship",
     "https://miami.breakthroughtech.org/programs/sprinternships/"): "A program providing women and non-binary students with internship opportunities.",
    ("Build INIT", ""): "An initiative at FIU designed to empower students through tech-focused workshops."
}

fiu_opportunities = {
    "Computer Science": {
        "Clubs": [
            ("Women in Computer Science (WICS)", "https://wics.cs.fiu.edu"),
            ("Society of Women Engineers (SWE)", "https://swe.org/"),
            ("Code Crunch", "https://codecrunch.org/"),
            ("INIT", "https://init.fiu.edu/")
        ],
        "Opportunities": common_opportunities
    },
    "Data Science": {
        "Clubs": [
            ("Women in Computer Science (WICS)", "https://wics.cs.fiu.edu"),
            ("Break Through Tech", "https://breakthroughtech.org/")
        ],
        "Opportunities": common_opportunities
    },
    "Cybersecurity": {
        "Clubs": [
            ("Women in CyberSecurity (WICyS)", "https://wics.cs.fiu.edu")
        ],
        "Opportunities": common_opportunities
    },
    "Computer Engineering": {
        "Clubs": [
            ("Society of Women Engineers (SWE)", "https://swe.org/"),
            ("IEEE", "https://www.ieee.org/")
        ],
        "Opportunities": common_opportunities
    },
    "Information Technology": {
        "Clubs": [
            ("Women in Computer Science (WICS)", "https://wics.cs.fiu.edu"),
            ("Women in CyberSecurity (WICyS)", "https://www.wicys.org/")
        ],
        "Opportunities": common_opportunities
    }
}


def determine_major(responses):
    # Logic to determine the major based on user responses
    if "Software Development" in responses:
        return "Computer Science"
    elif "Data Analysis" in responses:
        return "Data Science"
    elif "System Security" in responses:
        return "Cybersecurity"
    elif "Network Engineering" in responses:
        return "Computer Engineering"
    elif "User Experience (UX) Design" in responses:
        return "Information Technology"
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
    if request.method == 'POST':
        user_responses = []
        for i in range(1, len(questions) + 1):
            response = request.form.get(str(i))
            user_responses.append(response)

        tech_interest = determine_major(user_responses)
        print(f"Tech Interest: {tech_interest}")  # Debugging line

        if tech_interest:
            return redirect(url_for('results', tech_interest=tech_interest))
        else:
            return "Error: No valid tech interest found."

    return render_template('quiz.html', questions=questions)


@app.route('/results/<tech_interest>')
def results(tech_interest):
    opportunities = fiu_opportunities.get(tech_interest, {})
    return render_template('results.html', tech_interest=tech_interest, opportunities=opportunities)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
