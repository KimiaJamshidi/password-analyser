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

    return render_template("index.html", strength=strength, feedback=feedback, password=password)

if __name__ == "__main__":
    app.run(debug=True)