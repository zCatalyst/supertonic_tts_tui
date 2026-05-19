from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from supertonic import TTS
import tempfile
import base64
import os
import json
import uuid
import time
import requests as req_lib

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
    "openrouter_api_key": "",
    "openrouter_model": "anthropic/claude-sonnet-4-20250514",
    "openrouter_system_prompt": "You are a helpful AI assistant.",
    "openrouter_temperature": 0.7,
    "openrouter_max_tokens": 4096,
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "aura_config.json")
SESSIONS_PATH = os.path.join(os.path.dirname(__file__), "aura_sessions.json")

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

def load_sessions():
    if os.path.exists(SESSIONS_PATH):
        with open(SESSIONS_PATH) as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSIONS_PATH, "w") as f:
        json.dump(sessions, f, indent=2)

config = load_config()
voices = config["voices"]
sessions = load_sessions()
active_session_id = None

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
    if "openrouter_api_key" in data:
        config["openrouter_api_key"] = data["openrouter_api_key"]
    if "openrouter_model" in data:
        config["openrouter_model"] = data["openrouter_model"]
    if "openrouter_system_prompt" in data:
        config["openrouter_system_prompt"] = data["openrouter_system_prompt"]
    if "openrouter_temperature" in data:
        config["openrouter_temperature"] = float(data["openrouter_temperature"])
    if "openrouter_max_tokens" in data:
        config["openrouter_max_tokens"] = int(data["openrouter_max_tokens"])

    save_config(config)
    return jsonify({**config, "voices": voices})

@app.route("/api/config/reset", methods=["POST"])
def reset_config():
    global config, voice_style, voices
    voices = {k: dict(v) for k, v in DEFAULT_VOICES.items()}
    api_key = config.get("openrouter_api_key", "")
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
        "openrouter_api_key": api_key,
        "openrouter_model": "anthropic/claude-sonnet-4-20250514",
        "openrouter_system_prompt": "You are a helpful AI assistant.",
        "openrouter_temperature": 0.7,
        "openrouter_max_tokens": 4096,
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

@app.route("/api/chat", methods=["POST"])
def chat():
    global active_session_id
    data = request.json
    message = data.get("message", "").strip()
    session_id = data.get("session_id")

    if not config.get("openrouter_api_key"):
        return jsonify({"error": "OpenRouter API key not configured"}), 400

    if not message:
        return jsonify({"error": "No message provided"}), 400

    if session_id and session_id in sessions:
        active_session_id = session_id
    elif not active_session_id or active_session_id not in sessions:
        active_session_id = str(uuid.uuid4())
        sessions[active_session_id] = {
            "id": active_session_id,
            "title": message[:50],
            "created": time.time(),
            "messages": []
        }
        save_sessions(sessions)

    session = sessions[active_session_id]
    session["messages"].append({"role": "user", "content": message})

    messages_for_api = [
        {"role": "system", "content": config["openrouter_system_prompt"]}
    ] + session["messages"]

    def generate():
        global active_session_id
        try:
            resp = req_lib.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config['openrouter_api_key']}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:2998",
                    "X-Title": "Aura TTS"
                },
                json={
                    "model": config["openrouter_model"],
                    "messages": messages_for_api,
                    "temperature": config["openrouter_temperature"],
                    "max_tokens": config["openrouter_max_tokens"],
                    "stream": True
                },
                stream=True
            )

            full_content = ""
            prompt_tokens = 0
            completion_tokens = 0

            for line in resp.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        line_str = line_str[6:]
                    if line_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(line_str)
                        if "usage" in chunk:
                            prompt_tokens = chunk["usage"].get("prompt_tokens", 0)
                            completion_tokens = chunk["usage"].get("completion_tokens", 0)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            full_content += content
                            yield f"data: {json.dumps({'content': content})}\n\n"
                    except json.JSONDecodeError:
                        continue

            session["messages"].append({"role": "assistant", "content": full_content})
            save_sessions(sessions)

            yield f"data: {json.dumps({'done': True, 'prompt_tokens': prompt_tokens, 'completion_tokens': completion_tokens})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")

@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    session_list = []
    for sid, sdata in sorted(sessions.items(), key=lambda x: x[1].get("created", 0), reverse=True):
        session_list.append({
            "id": sdata["id"],
            "title": sdata.get("title", "Untitled"),
            "created": sdata.get("created", 0),
            "message_count": len(sdata.get("messages", []))
        })
    return jsonify({"sessions": session_list, "active": active_session_id})

@app.route("/api/sessions", methods=["POST"])
def create_session():
    global active_session_id
    data = request.json
    title = data.get("title", "New Session")
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "id": session_id,
        "title": title,
        "created": time.time(),
        "messages": []
    }
    active_session_id = session_id
    save_sessions(sessions)
    return jsonify({"id": session_id, "title": title})

@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    global active_session_id
    if session_id in sessions:
        del sessions[session_id]
        save_sessions(sessions)
        if active_session_id == session_id:
            active_session_id = None
        return jsonify({"ok": True})
    return jsonify({"error": "Session not found"}), 404

@app.route("/api/sessions/<session_id>/activate", methods=["POST"])
def activate_session(session_id):
    global active_session_id
    if session_id in sessions:
        active_session_id = session_id
        return jsonify({"ok": True, "session": sessions[session_id]})
    return jsonify({"error": "Session not found"}), 404

@app.route("/api/sessions/<session_id>/messages", methods=["GET"])
def get_session_messages(session_id):
    if session_id in sessions:
        return jsonify({"messages": sessions[session_id].get("messages", [])})
    return jsonify({"error": "Session not found"}), 404

@app.route("/api/sessions/<session_id>/rename", methods=["POST"])
def rename_session(session_id):
    data = request.json
    if session_id in sessions and "title" in data:
        sessions[session_id]["title"] = data["title"]
        save_sessions(sessions)
        return jsonify({"ok": True})
    return jsonify({"error": "Session not found"}), 404

if __name__ == "__main__":
    print(f"\n  {config['name']} TTS — http://localhost:2998\n")
    app.run(host="0.0.0.0", port=2998, debug=False)
