from flask import Flask, render_template, request
import socket
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    score = 0
    ip_address = None

    if request.method == "POST":
        website = request.form["website"].strip().lower()

        # Add http if missing
        if not website.startswith("http"):
            website = "http://" + website

        # Extract domain name
        domain = website.replace("http://", "").replace("https://", "").split("/")[0]
        
# Simple Risk Logic

# 1️⃣ Check if domain uses suspicious keywords
suspicious_words = ["free", "login", "verify", "update", "secure", "bank"]

for word in suspicious_words:
    if word in domain:
        score += 20

# 2️⃣ Check if domain length is very long
if len(domain) > 20:
    score += 15

# 3️⃣ Check if domain contains numbers
if any(char.isdigit() for char in domain):
    score += 15

# Decide risk level
if score >= 40:
    result = "High Risk"
elif score >= 20:
    result = "Medium Risk"
else:
    result = "Low Risk"
        # Try getting IP address
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unable to fetch IP"
            score += 30

        # HTTPS check
        if website.startswith("https://"):
            score += 20
        else:
            score += 70

        # Suspicious keywords check (improved)
suspicious_words = ["login", "verify", "secure", "update", "bank"]

for word in suspicious_words:
    if word in website.lower():
        score += 5

if "@" in website:
    score += 20

if domain.count('-') > 1:
    score += 5

if website.count('.') > 3:
    score += 10

        # Final risk level
        if score < 40:
            result = "🟢 LOW RISK"
        elif score < 80:
            result = "🟡 MEDIUM RISK"
        else:
            result = "🔴 HIGH RISK"

    return render_template("index.html", result=result, score=score, ip=ip_address)

if __name__ == "__main__":
    app.run(debug=True)
