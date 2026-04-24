import secrets
import string
import math
import hashlib
import requests
import re

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
    pwned_count = check_pwned(password)
    in_dictionary = check_dictionary(password)
    pattern_warnings = check_patterns(password)
    hashes = get_hashes(password)

    return render_template("index.html", strength=strength, feedback=feedback, password=password, crack_time=crack_time, entropy=entropy, score=score, pwned_count=pwned_count, in_dictionary=in_dictionary, pattern_warnings=pattern_warnings, hashes=hashes)


# Opens and reads the file and returns True if password was found in the file
def check_dictionary(password):
    try:
        with open("rockyou.txt", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip() == password:
                    return True
        return False
    except FileNotFoundError:
        return False


def check_pwned(password):
    # Hash the password using SHA-1
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Split into first 5 chars and the rest
    prefix = sha1[:5]
    suffix = sha1[5:]
    
    # Send only the first 5 chars to the API
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    
    # Check if our suffix appears in the response
    hashes = response.text.splitlines()
    for line in hashes:
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    
    return 0


# Hash viewer to show how password looks when stored in a database
def get_hashes(password):
    md5 = hashlib.md5(password.encode()).hexdigest()
    sha1 = hashlib.sha1(password.encode()).hexdigest()
    sha256 = hashlib.sha256(password.encode()).hexdigest()
    
    return {
        "MD5": md5,
        "SHA-1": sha1,
        "SHA-256": sha256
    }


# Checks for common patterns and warns the user
def check_patterns(password):
    warnings = []
    
    # Keyboard walks
    keyboards = ["qwerty", "asdf", "zxcv", "qazwsx", "123456", "654321"]
    for pattern in keyboards:
        if pattern in password.lower():
            warnings.append("Contains a keyboard pattern")
            break

    # Repeated characters
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            warnings.append("Contains repeated characters")
            break

    # Common leet speak
    leet = ["p@ssw0rd", "h3ll0", "@dmin", "l0gin", "passw0rd"]
    for pattern in leet:
        if pattern in password.lower():
            warnings.append("Contains common leet speak substitution")
            break

    # Year patterns
    if re.search(r'19\d{2}|20\d{2}', password):
        warnings.append("Contains a year — easy to guess")

    return warnings


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
    
    # Assuming GPU can do 10 billion guesses per second (as modern GPUs would)
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


# Generates random password
@app.route("/generate", methods=["POST"])
def generate():
    length = int(request.form["length"])
    
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    
    # Run all the same analysis on the generated password
    entropy = calculate_entropy(password)
    crack_time = calculate_crack_time(password)
    pwned_count = check_pwned(password)
    in_dictionary = check_dictionary(password)
    pattern_warnings = check_patterns(password)
    hashes = get_hashes(password)

    return render_template("index.html", generated=password, crack_time=crack_time, entropy=entropy, pwned_count=pwned_count, in_dictionary=in_dictionary, pattern_warnings=pattern_warnings, hashes=hashes)


if __name__ == "__main__":
    app.run(debug=True)