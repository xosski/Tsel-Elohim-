from pathlib import Path
import zipfile

# Define the base directory and zip file name
base_dir = Path("C:\Users\edking\Downloads")
base_dir.mkdir(exist_ok=True)
zip_filename = "C:\Users\edking\Downloads"

# Define the files to include in the PoC bundle
files = {
    "app.py": """
\"\"\"
GHOST.WALLET.OVERRIDE — Bitcoin Wallet Identity Exploit
Simulates a biometric + browser spoof-based wallet unlock process.
This is a PoC demonstration. No actual keys are retrieved.
\"\"\"

from flask import Flask, request, render_template_string
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "<h1>GhostCore Wallet Recovery Portal</h1><p>Navigate to /bypass or /wallet</p>"

@app.route('/bypass')
def bypass():
    return render_template_string(open("bypass_ui.html").read())

@app.route('/wallet', methods=['GET', 'POST'])
def wallet():
    if request.method == 'POST':
        fake_key = "L1aW4aubDFB7yfras2S1mMEb5BzZK1F1tQ9x4UePbksJQxoyX4Rz"
        logging.info(f"[WALLET] Fake private key served: {fake_key}")
        return f"<h3>Wallet Unlocked</h3><p>Private Key: <code>{fake_key}</code></p>"
    return render_template_string(open("wallet_ui.html").read())

if __name__ == '__main__':
    print("== GHOST.WALLET.OVERRIDE running on http://localhost:5000 ==")
    app.run(host='0.0.0.0', port=5000)
""",
    "bypass_ui.html": """
<!doctype html>
<html>
<head>
  <title>Facial Verification</title>
  <script>
    function spoofVerify() {
        document.getElementById('status').innerText = "✅ Facial ID Verified";
        document.getElementById('next').style.display = 'block';
    }
    window.onload = () => setTimeout(spoofVerify, 1000);
  </script>
</head>
<body>
  <h2>Identity Verification</h2>
  <video autoplay style="width:320px; background:#000;"></video>
  <p id="status">🔍 Scanning...</p>
  <a href="/wallet" id="next" style="display:none;"><button>Proceed to Wallet</button></a>
</body>
</html>
""",
    "wallet_ui.html": """
<!doctype html>
<html>
<head><title>Wallet Recovery</title></head>
<body>
  <h2>Wallet Recovery</h2>
  <form method="post">
    <label>Enter your username or ID:</label><br>
    <input name="user" required><br><br>
    <input type="submit" value="Recover Wallet">
  </form>
</body>
</html>
"""
}

# Write each file to the bundle directory
for filename, content in files.items():
    (base_dir / filename).write_text(content.strip())

# Create the zip archive
with zipfile.ZipFile(zip_filename, "w") as zipf:
    for file in files:
        zipf.write(base_dir / file, arcname=file)

zip_filename  # Return the zip file path for download confirmation
