import os
import random
import string
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# In-memory database to store URL mappings
url_database = {}

# Function to generate a short key
def generate_short_key(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_key = ''.join(random.choice(characters) for _ in range(length))
        if short_key not in url_database:
            return short_key

# Home page with form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form.get('url')
        if not original_url:
            return render_template('index.html', error="Please provide a valid URL.")

        short_key = generate_short_key()
        url_database[short_key] = original_url
        short_url = request.host_url + short_key
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

# Redirect route
@app.route('/<short_key>')
def redirect_to_original(short_key):
    original_url = url_database.get(short_key)
    if original_url:
        return redirect(original_url)
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)