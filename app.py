from flask import Flask, render_template, request, redirect, flash
from plyer import notification
import time
import threading
import secrets  # Import the secrets module to generate a strong secret key

app = Flask(__name__)

# Generate a secure random secret key
app.secret_key = secrets.token_hex(16)  # 16-byte secure random key

def send_notification(title, message, t):
    time.sleep(t)  # Sleep for the specified time
    notification.notify(
        title=title,
        message=message,
        timeout=10,
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_notification():
    title = request.form['title']
    message = request.form['message']
    delay = int(request.form['time'])  # Get time in seconds

    # Start a new thread for the notification, so it doesn't block the main app
    threading.Thread(target=send_notification, args=(title, message, delay)).start()

    # Flash a success message and redirect back to the home page
    flash(f'Your notification is created! You will be notified in {delay} seconds.')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
