import secrets
import string
import math

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyse", methods=["POST"])
def analyse():
    password = request.form["password"]
    
    score = 0
    feedback = []

    # Check the length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    # Check for numbers
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number")

    # Check for uppercase
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter")

    # Check for symbols
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(char in symbols for char in password):
        score += 1
    else:
        feedback.append("Add at least one symbol")

    # Choosing the strength level
    if score == 4:
        strength = "Very Strong 💪"
    elif score == 3:
        strength = "Strong 👍"
    elif score == 2:
        strength = "Fair ⚠️"
    else:
        strength = "Weak ❌"

    crack_time = calculate_crack_time(password)
    entropy = calculate_entropy(password)

    return render_template("index.html", strength=strength, feedback=feedback, password=password, crack_time=crack_time, entropy=entropy)


# Function to calculate Entropy score
def calculate_entropy(password):
    pool = 0
    
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        pool += 32

    if pool == 0:
        return 0
        
    entropy = len(password) * math.log2(pool)
    return round(entropy, 1)


# Function to calculate how long it takes for the password to be cracked
def calculate_crack_time(password):
    pool = 0
    
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        pool += 32

    combinations = pool ** len(password)
    
    # Assuming GPU can do 10 billion guesses per second (as modern GPU's would)
    guesses_per_second = 10_000_000_000
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "less than a second ⚡ — extremely vulnerable"
    elif seconds < 60:
        return f"{int(seconds)} seconds 😨"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes 😰"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours 😅"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days 👍"
    elif seconds < 3153600000:
        return f"{int(seconds // 31536000)} years 💪"
    else:
        return "longer than the age of the universe 🔒 — uncrackable"

 #Generates random password 
@app.route("/generate", methods=["POST"])
def generate():
    length = int(request.form["length"])
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    
    return render_template("index.html", generated=password)

if __name__ == "__main__":
    app.run(debug=True)