from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la API key de forma segura
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY no está configurada")

# Crear cliente OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__)


def create_workout_and_diet_plan(user_data, model):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in diet and routine exercises."
            },
            {
                "role": "user",
                "content": (
                    "Create an exercise and diet routine for every day "
                    f"of the week, for a user with the following data: {user_data}"
                )
            }
        ],
        max_tokens=800,
        n=1,
        temperature=0.7
    )

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

    user_data = (
        f"weight: {weight} kg, "
        f"height: {height} cm, "
        f"waist size: {waist_size} cm, "
        f"age: {age}, "
        f"hereditary diseases: {hereditary_diseases}, "
        f"personal diseases: {personal_diseases}, "
        f"injuries: {injuries}, "
        f"country: {country}"
    )

    # Generar el plan usando el modelo que ya tenías
    workout_and_diet_plan = create_workout_and_diet_plan(
        user_data,
        "gpt-3.5-turbo-1106"
    )

    # Mostrar el resultado directamente en HTML
    return render_template(
        "result.html",
        workout_and_diet_plan=workout_and_diet_plan
    )


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
