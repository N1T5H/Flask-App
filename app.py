from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            return data[0]['q'] + " — " + data[0]['a']
        else:
            return "Could not fetch quote at the moment."
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    quote = get_random_quote()
    return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
