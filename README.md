# Introduction

<p>PasswordBiotics is a flask-based password evaluation tool powered by the zxcvbn library made by Dropbox.</p>
<p>zxcvbn is a password strength estimation library.</p>
<p>In addition, PasswordBiotics incorporates blacklist detection using a list of 1000 commonly used passwords and leetspeak normalization to enhance the robustness of the tool.</p>

PasswordBiotics evalautes password strength using zxcvbn, which:
<ul>
  <li>Analyzes passwords based on pattern matching</li>
  <li>Checks against multiple dictionaries</li>
  <li>Estimates cracking time based on different attack scenarios</li>
  <li>Provides recommendations for improving the strength of passwords</li>
</ul>

The tool leverages the power of the zxcvbn library by:
<ul>
  <li>Having a clean UI and severity indicators to allow a user with no technical knowledge to improve their passwords and understand the tool</li>
  <li>Using a custom blacklist</li>
  <li>Implementing leatspeak normalization</li>
</ul>

# Features

- Uses the native zxcvbn scoring (on a scale of 0–4)
- Crack time estimation across multiple attack scenarios:
- Custom password blacklist of 1000 commonly used passwords
- Leetspeak normalization to detect disguised weak passwords
- Crack time severity classification
- Clean UI strength and progress bar

# State of the Project

<p>It has not been deployed yet.</p>
<p>It is still being updated.</p>
<p>The public is free to use, copy, modify and publish any part of the code.</p>

# Running It Locally

1. Clone the repository:

   ```
   git clone https://github.com/kangindustries/PasswordBiotics.git
   ```

2. Create the virtual environment:

   ```
   python -m venv venv
   ```

3. Activate the virtual environment:

   ```
   venv\Scripts\activate
   ```

4. If you encounter issues with PowerShell permissions:

   ```
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

5. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
6. Run the application

   ```
   python app.py
   ```
