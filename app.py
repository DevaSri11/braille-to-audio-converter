import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
from model_utils import load_model_and_labels, predict_single, predict_images_batch
from gtts import gTTS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
AUDIO_FOLDER = os.path.join(BASE_DIR, "audio")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "../templates"),
    static_folder=os.path.join(BASE_DIR, "../static"),
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER
ALLOWED_EXT = {"png", "jpg", "jpeg"}

model, CLASSES = load_model_and_labels()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    saved_paths = []
    for f in files:
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            uid = str(uuid.uuid4())[:8]
            out_name = f"{uid}_{fname}"
            path = os.path.join(app.config["UPLOAD_FOLDER"], out_name)
            f.save(path)
            saved_paths.append(path)

    preds = (
        [predict_single(saved_paths[0], model, CLASSES)]
        if len(saved_paths) == 1
        else predict_images_batch(saved_paths, model, CLASSES)
    )

    letters = [p["letter"] for p in preds]
    full_text = "".join(letters)

    corrected_text = full_text
    if OPENAI_API_KEY and full_text.strip():
        try:
            response = client.responses.create(
                model="gpt-5-nano",
                input=(
                    f"These letters were detected from Braille: {full_text}. "
                    "Reorder or correct them to form a meaningful English word or sentence. "
                    "Return only the corrected text, no explanations."
                ),
            )
            corrected_text = response.output_text.strip()
        except Exception as e:
            print(f"[OpenAI Error]: {e}")

    try:
        tts = gTTS(text=corrected_text or "No prediction", lang="en")
        audio_uid = str(uuid.uuid4())[:8]
        audio_filename = f"tts_{audio_uid}.mp3"
        audio_path = os.path.join(app.config["AUDIO_FOLDER"], audio_filename)
        tts.save(audio_path)
        audio_url = url_for("serve_audio", filename=audio_filename)
    except Exception as e:
        print(f"[TTS Error]: {e}")
        audio_url = None

    return jsonify({
        "predictions": preds,
        "text": full_text,
        "corrected_text": corrected_text,
        "audio_url": audio_url,
    })

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(app.config["AUDIO_FOLDER"], filename)

@app.route("/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
