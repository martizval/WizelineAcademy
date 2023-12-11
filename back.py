from flask import Flask, request, render_template
import openai

app = Flask(__name__)

openai.api_key = "YOUR_API_KEY"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    user_data = {
        "weight": request.form["weight"],
        "height": request.form["height"],
        "waist_size": request.form["waist_size"],
        "age": request.form["age"],
        "hereditary_diseases": request.form["hereditary_diseases"].split(","),
        "personal_diseases": request.form["personal_diseases"].split(","),
        "injuries": request.form["injuries"].split(","),
        "country": request.form["country"],
    }

    workout_and_diet_plan = create_workout_and_diet_plan(user_data)
    return render_template("results.html", workout_and_diet_plan=workout_and_diet_plan)

def create_workout_and_diet_plan(user_data):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Crear una rutina de ejercicio y dieta para un usuario con los siguientes datos: {user_data}",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)