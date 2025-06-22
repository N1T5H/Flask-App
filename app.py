from flask import Flask, render_template
import requests
import random

app = Flask(__name__)
quote_cache = []

def refill_cache():
    global quote_cache
    try:
        response = requests.get("https://zenquotes.io/api/quotes")
        if response.status_code == 200:
            quote_cache = [
                f"{q['q']} — {q['a']}"
                for q in response.json()
                if 'q' in q and 'a' in q
            ]
    except Exception as e:
        quote_cache.append(f"Error: {e}")

def get_random_quote():
    if not quote_cache:
        refill_cache()
    return random.choice(quote_cache) if quote_cache else "Could not fetch quote at the moment."


@app.route('/')
def home():
    quote = get_random_quote()
    return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
