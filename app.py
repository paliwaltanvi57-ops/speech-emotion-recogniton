from flask import Flask, render_template, request
import os
import json
import traceback

from collections import Counter
from utils.chunk_audio import split_audio
from utils.predict_emotion import predict_emotion




app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"wav"}

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

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
    file.save(filepath)
    try:
        num_chunks = split_audio(filepath)
        # All the remaining processing code
        # (chunk reading, predictions, Counter,
        # average confidence, JSON saving)
    except Exception as e : 
        print(type(e))
        print(e)
        raise
    
    # Read chunk files
    
    chunk_folder = "chunks"
    chunk_files = os.listdir(chunk_folder)
    chunk_files.sort()
    results = []

    emotion_list = []

    confidence_list = []

    for chunk in chunk_files:
        chunk_path = os.path.join(chunk_folder, chunk)
        emotion, confidence = predict_emotion(chunk_path)

        emotion_list.append(emotion)
        confidence_list.append(confidence)

        print(f"Chunk: {chunk}")
        print(f"Emotion: {emotion}")
        print(f"Confidence: {confidence:.2f}")
        print("-----------------------")
        results.append({
            "chunk": chunk,
            "emotion": emotion,
            "confidence": round(confidence, 2)
        })


    print(results)
    emotion_counter = Counter(emotion_list)
    overall_emotion = emotion_counter.most_common(1)[0][0]

    average_confidence = round(
        sum(confidence_list) / len(confidence_list),
        2
    )
    print(f"Average Confidence: {average_confidence}")
    print("\nEmotion Count:")
    print(emotion_counter)
    print(f"\nOverall Emotion: {overall_emotion}")

    analysis_report = {
        "filename": file.filename,
        "overall_emotion": overall_emotion,
        "total_chunks": num_chunks,
        "average_confidence": average_confidence,
        "emotion_distribution": dict(emotion_counter),
        "chunks": results
    }

    result_file = os.path.join("results", "emotion_analysis.json")
    
    with open(result_file, "w") as json_file:
        json.dump(analysis_report, json_file, indent=4)
    
    overall_emotion = max(
        results,
        key=lambda x: x["confidence"]
    )["emotion"]


    return render_template(
        "result.html",
        filename=file.filename,
        total_chunks=num_chunks,
        overall_emotion=overall_emotion,
        results=results
    )

if __name__ == "__main__":
    app.run(debug=True)