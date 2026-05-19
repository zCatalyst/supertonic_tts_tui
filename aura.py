from flask import Flask, render_template, request, jsonify
from supertonic import TTS
import tempfile
import base64
import os
import json

app = Flask(__name__)

DEFAULT_VOICES = {
    "F1": {"name": "Aria", "gender": "Female", "desc": "Warm, conversational"},
    "F2": {"name": "Luna", "gender": "Female", "desc": "Soft, gentle"},
    "F3": {"name": "Nova", "gender": "Female", "desc": "Bright, energetic"},
    "F4": {"name": "Sage", "gender": "Female", "desc": "Calm, professional"},
    "F5": {"name": "Iris", "gender": "Female", "desc": "Deep, authoritative"},
    "M1": {"name": "Jarvis", "gender": "Male", "desc": "Classic, sophisticated"},
    "M2": {"name": "Atlas", "gender": "Male", "desc": "Deep, commanding"},
    "M3": {"name": "Orion", "gender": "Male", "desc": "Smooth, friendly"},
    "M4": {"name": "Echo", "gender": "Male", "desc": "Clear, neutral"},
    "M5": {"name": "Titan", "gender": "Male", "desc": "Rich, resonant"},
}

DEFAULT_CONFIG = {
    "name": "AURA",
    "voice": "M1",
    "lang": "en",
    "steps": 8,
    "speed": 1.05,
    "text_speed": 20,
    "theme": "catppuccin",
    "show_glyph": True,
    "voices": DEFAULT_VOICES,
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "aura_config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            saved = json.load(f)
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(saved)
        if "voices" in saved:
            for vid, vdata in saved["voices"].items():
                if vid in cfg["voices"]:
                    cfg["voices"][vid].update(vdata)
        return cfg
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

config = load_config()
voices = config["voices"]

print(f"Initializing {config['name']} TTS system...")
tts = TTS(auto_download=True)
voice_style = tts.get_voice_style(voice_name=config["voice"])
print(f"{config['name']} ready. Voice: {config['voice']} ({voices[config['voice']]['name']})")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/synthesize", methods=["POST"])
def synthesize():
    global voice_style
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Sanitize text: remove box-drawing and other unsupported Unicode
    import re
    text = re.sub(r'[\u2500-\u257F\u2580-\u259F\u2800-\u28FF]', '', text).strip()

    if not text:
        return jsonify({"error": "No valid text after sanitization"}), 400

    try:
        wav, duration = tts.synthesize(
            text=text,
            lang=config["lang"],
            voice_style=voice_style,
            total_steps=config["steps"],
            speed=config["speed"],
        )

        temp_path = tempfile.mktemp(suffix=".wav")
        tts.save_audio(wav, temp_path)

        with open(temp_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        os.remove(temp_path)

        return jsonify({
            "audio": f"data:audio/wav;base64,{audio_base64}",
            "duration": float(duration[0]),
            "text": text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({**config, "voices": voices})

@app.route("/api/config", methods=["POST"])
def update_config():
    global config, voice_style
    data = request.json

    if "name" in data:
        config["name"] = data["name"]

    if "voice" in data:
        voice = data["voice"]
        if voice not in voices:
            return jsonify({"error": f"Unknown voice: {voice}"}), 400
        config["voice"] = voice
        voice_style = tts.get_voice_style(voice_name=voice)

    if "lang" in data:
        config["lang"] = data["lang"]
    if "steps" in data:
        config["steps"] = int(data["steps"])
    if "speed" in data:
        config["speed"] = float(data["speed"])
    if "text_speed" in data:
        config["text_speed"] = int(data["text_speed"])
    if "theme" in data:
        config["theme"] = data["theme"]
    if "show_glyph" in data:
        config["show_glyph"] = bool(data["show_glyph"])

    save_config(config)
    return jsonify({**config, "voices": voices})

@app.route("/api/config/reset", methods=["POST"])
def reset_config():
    global config, voice_style, voices
    voices = {k: dict(v) for k, v in DEFAULT_VOICES.items()}
    config = {
        "name": "AURA",
        "voice": "M1",
        "lang": "en",
        "steps": 8,
        "speed": 1.05,
        "text_speed": 20,
        "theme": "catppuccin",
        "show_glyph": True,
        "voices": voices,
    }
    save_config(config)
    voice_style = tts.get_voice_style(voice_name=config["voice"])
    return jsonify({**config, "voices": voices})

@app.route("/api/voice/<voice_id>/desc", methods=["POST"])
def update_voice_desc(voice_id):
    data = request.json
    if voice_id not in voices:
        return jsonify({"error": f"Unknown voice: {voice_id}"}), 400
    if "desc" in data:
        voices[voice_id]["desc"] = data["desc"]
        config["voices"] = voices
        save_config(config)
    return jsonify({"voices": voices})

if __name__ == "__main__":
    print(f"\n  {config['name']} TTS — http://localhost:2998\n")
    app.run(host="0.0.0.0", port=2998, debug=False)
