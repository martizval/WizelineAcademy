from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not configured in the .env file")

client = OpenAI(api_key=api_key)

app = Flask(__name__)


# ============================================================
# GENERATE A PLAN
# ============================================================

def create_workout_and_diet_plan(user_data, model):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a nutrition and exercise planning assistant. "
                    "Create a practical 7-day diet and exercise plan using all "
                    "the user's information. "

                    "Country is a mandatory constraint: prioritize foods "
                    "commonly available in that country and replace difficult "
                    "or uncommon ingredients with locally available, "
                    "nutritionally similar alternatives. "

                    "Ensure appropriate sources of protein, carbohydrates, "
                    "healthy fats, fiber, fruits and vegetables. "

                    "Consider weight, height, age, waist size, diseases, "
                    "hereditary conditions and injuries. Avoid recommendations "
                    "that may conflict with reported conditions. "

                    "Prefer simple, affordable and realistic meals. "

                    "Return a concise plan organized by day. For each day "
                    "include breakfast, lunch, dinner, optional snack and "
                    "exercise. "

                    "This is general wellness guidance, not a medical diagnosis "
                    "or treatment."
                )
            },
            {
                "role": "user",
                "content": user_data
            }
        ],
        max_tokens=700,
        temperature=0.5
    )

    return response.choices[0].message.content


# ============================================================
# MAIN PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# PROCESS FORM
# ============================================================

@app.route("/submit", methods=["POST"])
def submit():

    weight = request.form["weight"]
    height = request.form["height"]
    waist_size = request.form["waist_size"]
    age = request.form["age"]

    hereditary_diseases = request.form["hereditary_diseases"]
    personal_diseases = request.form["personal_diseases"]
    injuries = request.form["injuries"]

    country = request.form["country"]

    # user data to send to the model
    user_data = (
        f"User data:\n"
        f"- Weight: {weight} kg\n"
        f"- Height: {height} cm\n"
        f"- Waist: {waist_size} cm\n"
        f"- Age: {age}\n"
        f"- Hereditary diseases: {hereditary_diseases}\n"
        f"- Personal diseases: {personal_diseases}\n"
        f"- Injuries: {injuries}\n"
        f"- Country: {country}"
    )

    # Generate the plan
    workout_and_diet_plan = create_workout_and_diet_plan(
        user_data,
        "gpt-3.5-turbo-1106"
    )

    # Show the result
    return render_template(
        "result.html",
        workout_and_diet_plan=workout_and_diet_plan
    )


# ============================================================
# EXECUTION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)


# if __name__ == "__main__":
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant."
#             },
#             {
#                 "role": "user",
#                 "content": "Say hello in Spanish."
#             }
#         ],
#         max_tokens=50
#     )

#     print(response.choices[0].message.content)
