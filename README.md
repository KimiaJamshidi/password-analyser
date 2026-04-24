# 🔒 SafeCheck — Password Security Analyser

A full-stack cybersecurity web application built with Python and Flask that analyses password strength, detects data breaches, and generates cryptographically secure passwords.

---

## Features

- **Live Strength Indicator** — password strength updates in real time as you type, implemented in vanilla JavaScript
- **Strength Analyser** — scores passwords against real security criteria including length, complexity, and character diversity
- **Entropy Calculator** — computes Shannon entropy in bits, the formal cryptographic measure of password strength used by security professionals
- **Brute Force Time Estimator** — calculates how long a modern GPU (10 billion guesses/second) would take to crack the password
- **Have I Been Pwned Integration** — checks passwords against a database of over 600 million breached passwords using the HIBP API with k-anonymity, ensuring the full password is never transmitted
- **Dictionary Attack Checker** — checks passwords against the rockyou.txt wordlist, a real-world leaked password dataset used by security researchers
- **Common Pattern Detector** — warns users about keyboard walks, repeated characters, leet speak substitutions, and year patterns
- **Hash Viewer** — displays MD5, SHA-1, and SHA-256 hashes to show how passwords are stored in databases
- **Secure Password Generator** — generates cryptographically secure passwords using Python's `secrets` module

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, JavaScript |
| Templating | Jinja2 |
| Security APIs | Have I Been Pwned |
| Version Control | Git, GitHub |

---

## Project Structure

```
password-analyser/
├── app.py                  # Flask app — all routing and security logic
├── static/
│   ├── style.css           # Stylesheet
│   └── script.js           # Live strength indicator
└── templates/
    ├── home.html           # Landing page
    ├── analyser.html       # Password analyser page
    └── generator.html      # Password generator page
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KimiaJamshidi/password-analyser.git
cd password-analyser
```

2. Install dependencies:
```bash
pip3 install flask requests
```

3. Download the rockyou.txt wordlist and place it in the root directory:
   - Download from: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
   - The file is ~133MB and is excluded from this repo via `.gitignore`

4. Run the app:
```bash
python3 app.py
```

5. Open your browser and go to:
```
http://127.0.0.1:5000
```

---

## Security Concepts Demonstrated

**k-Anonymity** — The Have I Been Pwned integration never sends the full password or hash to the API. Only the first 5 characters of the SHA-1 hash are transmitted, and the result is checked locally. This is a real privacy-preserving pattern used in production security tools.

**Cryptographically Secure Randomness** — The password generator uses Python's `secrets` module rather than `random`, as `secrets` uses the operating system's secure random source and is designed specifically for security-sensitive applications.

**Shannon Entropy** — Entropy is calculated using the formula `length × log₂(pool)`, where pool is the size of the character set used. This gives a formal cryptographic measurement in bits rather than a simple rule-based score.

**Hashing Algorithms** — The hash viewer demonstrates MD5, SHA-1, and SHA-256, illustrating why modern systems should use SHA-256 over the deprecated MD5 and SHA-1 algorithms.

---

## Notes

- This tool is built for **educational purposes**. No passwords are stored or logged.
- Run in `debug=True` mode for local development only. Always set `debug=False` for any production deployment.
- rockyou.txt is not included in this repository due to its file size (133MB). See installation instructions above.

---

## Built With

- [Flask](https://flask.palletsprojects.com/)
- [Have I Been Pwned API](https://haveibeenpwned.com/API/v3)
- [rockyou.txt](https://github.com/brannondorsey/naive-hashcat)