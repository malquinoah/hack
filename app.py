from flask import Flask, render_template
import python_avatars as pa
import os

app = Flask(__name__)

@app.route('/')
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

        avatar.render("static/cute_female_avatar.svg")  # Save avatar in static folder
        return render_template('index.html')
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start the server: {e}")

