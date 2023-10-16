from flask import Flask, render_template, request, redirect, send_file
import mysql.connector
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL Configuration
db = mysql.connector.connect(
    host="sql11.freesqldatabase.com",
    user="sql11653855",
    password="x2lIMdfC7C",
    database="sql11653855",
    port=3306
)

cursor = db.cursor()

# Create a table to store messages
cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, sender VARCHAR(255), message TEXT)")

# Create a table to store files
cursor.execute("CREATE TABLE IF NOT EXISTS files (id INT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255))")

@app.route('/')
def index():
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()

    cursor.execute("SELECT * FROM files")
    files = cursor.fetchall()

    return render_template('index.html', messages=messages, files=files)

@app.route('/send', methods=['POST'])
def send():
    sender = request.form['sender']
    message = request.form['message']

    cursor.execute("INSERT INTO messages (sender, message) VALUES (%s, %s)", (sender, message))
    db.commit()

    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("INSERT INTO files (filename) VALUES (%s)", (filename,))
        db.commit()

    return redirect('/')

@app.route('/uploads/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
