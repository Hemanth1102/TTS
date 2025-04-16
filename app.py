from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import os
import io
from scipy.io.wavfile import write
import numpy as np

app = Flask(__name__)

# Load TTS model (keep your version)
tts = TTS(
    model_path="models/v1/te/fastpitch/best_model.pth",
    config_path="models/v1/te/fastpitch/config.json",
    vocoder_path="models/v1/te/hifigan/best_model.pth",
    vocoder_config_path="models/v1/te/hifigan/config.json"
)

@app.route("/synthesize", methods=["POST"])
def synthesize():
    try:
        data = request.json
        text = data.get("text", "")
        speaker = data.get("speaker", None)

        # Generate waveform (returns float32 between -1 and 1)
        wav = tts.synthesizer.tts(text, speaker_name=speaker)
        wav = np.array(wav)

        # Convert float32 -> int16 PCM (normalize safely)
        wav = wav / np.max(np.abs(wav))  # Normalize
        wav = (wav * 32767).astype(np.int16)

        # Save to temp.wav
        output_path = "output.wav"
        write(output_path, 22050, wav)  # ✅ Save permanently

        return send_file(
            output_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="output.wav"
        )

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
