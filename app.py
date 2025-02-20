from flask import Flask, Response
import os
import subprocess
from datetime import datetime
import pytz

app = Flask(__name__)

FULL_NAME = "Namandeep Singh"

@app.route('/htop')
def htop():
    # Get system username; fallback if os.getlogin() fails
    try:
        username = os.getlogin()
    except Exception:
        username = os.environ.get("USER", "unknown")
    
    # Get server time in IST (Indian Standard Time)
    ist_tz = pytz.timezone("Asia/Kolkata")
    server_time = datetime.now(ist_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Run the top command in batch mode
    try:
        top_output = subprocess.check_output(["top", "-b", "-n", "1"], universal_newlines=True)
    except Exception as e:
        top_output = f"Error running top command: {e}"
    
    # Create HTML response
    html = f"""
    <html>
      <head>
        <title>HTOP Endpoint</title>
      </head>
      <body>
        <h1>HTOP Endpoint</h1>
        <p><strong>Name:</strong> {FULL_NAME}</p>
        <p><strong>Username:</strong> {username}</p>
        <p><strong>Server Time in IST:</strong> {server_time}</p>
        <h2>Top Output:</h2>
        <pre>{top_output}</pre>
      </body>
    </html>
    """
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    # Make the server externally accessible by binding to 0.0.0.0 on port 5000
    app.run(host='0.0.0.0', port=5000)
