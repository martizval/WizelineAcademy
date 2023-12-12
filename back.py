from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
import openai

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Crear el cliente OpenAI
client = openai.Client()

app = Flask(__name__)

def create_workout_and_diet_plan(user_data, model):
    # Realizar la solicitud de autocompletado
    response = client.chat.completions.create(
        model=model,
        messages=[{
                    "role": "assistant",
         "content": "You are an expert in diet and routine exercises."
    },
            {
                "role": "user",
                "content": f"Create an exercise and diet routine for every day of the week, for a user with the following data: {user_data}"
            }
        ],
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Devolver el texto generado
    return response.choices[0].message.content

@app.route("/")
def index():
    return render_template("index.html")

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

    user_data = f"weight: {weight} kg, height: {height} cm, Waist Size: {waist_size} cm, Age: {age} , hereditary diseases: {hereditary_diseases}, personal diseases: {personal_diseases}, Injuries: {injuries}, Country: {country}"

    workout_and_diet_plan = create_workout_and_diet_plan(user_data, "gpt-3.5-turbo-1106")

    # Crear un nombre de archivo único basado en la fecha y hora actuales
    now = datetime.datetime.now()
    file_name = f"{now.strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    # Escribir el resultado en un archivo txt
    with open(file_name, "w") as f:
        f.write(workout_and_diet_plan)

    # Redirigir al usuario a la página principal
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
