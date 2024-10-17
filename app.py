from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Wczytywanie zmiennych środowiskowych
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Obsługa CORS, aby zezwalać na zapytania z dowolnego źródła

# Klucz API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Historia rozmów
conversation_history = [{
    "role": "system",
    "content": (
        "Your name is Neo. "
        "We connect people with future technologies. Here are some key skills you might want to develop:\n"
        "- **Artificial Intelligence**: Understanding machine learning algorithms and their applications.\n"
        "- **Data Science**: Skills in data analysis, statistical modeling, and data visualization.\n"
        "- **Software Development**: Proficiency in programming languages like Python, Java, and frameworks.\n"
        "- **Cloud Computing**: Familiarity with platforms like AWS, Azure, or Google Cloud.\n"
        "- **Cybersecurity**: Knowledge of protecting systems and networks from digital attacks.\n"
        "These skills are essential in the modern job market and can open doors to many opportunities!"
    )
}]

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No input message provided"}), 400

    # Dodajemy wiadomość użytkownika do historii
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Wywołanie OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Użyj odpowiedniego modelu
            messages=conversation_history
        )

        # Pobieranie odpowiedzi z OpenAI
        answer = response['choices'][0]['message']['content'].strip()
        conversation_history.append({"role": "assistant", "content": answer})

        return jsonify({"response": f"Neo: {answer}"})

    except Exception as e:
        print(f"Error: {str(e)}")  # Logowanie błędów
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Uruchomienie serwera Flask z obsługą SSL
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('/etc/letsencrypt/live/isecstudent.com-0002/fullchain.pem', '/etc/letsencrypt/live/isecstudent.com-0002/privkey.pem'))
