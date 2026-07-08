from flask import Flask, render_template, request
import os
from utils.chunk_audio import split_audio

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    if "audio" not in request.files:
        return "No file selected."

    file = request.files["audio"]

    if file.filename == "":
        return "No file selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    
    file.save(filepath)
    
    num_chunks = split_audio(filepath)
    return f"""<h2>Upload Successful ✅</h2>
    <p>File: {file.filename}</p>
    <p>Total Chunks Created: {num_chunks}</p>"""

if __name__ == "__main__":
    app.run(debug=True)