from flask import Flask, render_template, request
from zxcvbn import zxcvbn
import unicodedata
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def load_blacklist(path="blacklist.txt"):
    bad_passwords = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                pw = line.strip().lower()
                if pw:
                    bad_passwords.add(pw)
    except FileNotFoundError:
        logging.warning(f"Blacklist file not found at {path}.")
    return bad_passwords

BLACKLIST = load_blacklist()

LEETSPEAK = str.maketrans({
    "@": "a", "4": "a",
    "3": "e",
    "1": "i", "!": "i",
    "0": "o",
    "5": "s", "$": "s",
    "7": "t", "+": "t",
    "8": "b",
    "6": "g", "9": "g",
})

def normalize(password: str) -> str:
    nfd = unicodedata.normalize("NFD", password)
    no_marks = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return no_marks.lower().translate(LEETSPEAK)

def _crack_severity(seconds: float) -> str:
    if seconds < 60:
        return "instant"
    if seconds < 86_400:
        return "fast"
    if seconds < 86_400 * 365:
        return "moderate"
    return "slow"

def _crack_times_from_zxcvbn(z: dict) -> list[dict]:
    ctd = z.get("crack_times_display", {}) or {}
    cts = z.get("crack_times_seconds", {}) or {}
    mapping = [
        ("Online (throttled)",   "online_throttling_100_per_hour"),
        ("Online (no-throttling)", "online_no_throttling_10_per_second"),
        ("Offline – slow hashing (10k/s)", "offline_slow_hashing_1e4_per_second"),
        ("Offline – fast hashing (10B/s)", "offline_fast_hashing_1e10_per_second"),
    ]
    results = []
    for scenario, key in mapping:
        display = ctd.get(key)
        seconds = cts.get(key)
        if display is None:
            continue
        sev = _crack_severity(float(seconds)) if seconds is not None else "moderate"
        results.append({"scenario": scenario, "time": display, "severity": sev})
    return results

def evaluate_password_zxcvbn(password: str):
    if not password:
        return 0, "Weak", ["Password cannot be empty."], []
    if len(password) < 6:
        return 0, "Weak", ["Password is too short — use at least 6 characters."], []
    if password.lower() in BLACKLIST or normalize(password) in BLACKLIST:
        z = zxcvbn(password)
        crack_times = _crack_times_from_zxcvbn(z)
        return 0, "Weak", ["This is a very commonly used password. Choose something else."], crack_times
    z = zxcvbn(password)
    zx_score = int(z.get("score", 0))
    if zx_score <= 1:
        category = "Weak"
    elif zx_score == 2:
        category = "Okay"
    else:
        category = "Strong"
    feedback = []
    fb = z.get("feedback", {}) or {}
    warning = fb.get("warning")
    suggestions = fb.get("suggestions", []) or []
    if warning:
        feedback.append(warning)
    feedback.extend(suggestions)
    crack_times = _crack_times_from_zxcvbn(z)
    return zx_score, category, feedback, crack_times

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    category = None
    feedback = []
    crack_times = []
    if request.method == "POST":
        password = request.form.get("password", "")
        score, category, feedback, crack_times = evaluate_password_zxcvbn(password)
    return render_template(
        "index.html",
        score=score,
        category=category,
        feedback=feedback,
        crack_times=crack_times,
    )

if __name__ == "__main__":
    app.run(debug=False)