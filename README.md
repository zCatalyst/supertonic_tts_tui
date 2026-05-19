# Aura

A TUI-styled web frontend for voice synthesis powered by [Supertonic 3](https://github.com/supertone-inc/supertonic) — a state-of-the-art neural text-to-speech model — with an integrated AI conversation mode via [OpenRouter](https://openrouter.ai/).

Type a message and hear it spoken aloud, or switch to AI mode for a full conversational experience with streaming replies and voice synthesis.

## Features

### TTS Mode
- **10 Voices** — 5 female (F1-F5) and 5 male (M1-M5) with editable descriptions
- **8 Themes** — Wabi-Sabi, Catppuccin, Matrix, Monokai, Nord, Dracula, Gruvbox, Tokyo Night
- **Live Glyph Animations** — Braille-pattern ASCII art that breathes, thinks, and speaks
- **Configurable** — Language, quality steps, speed, text animation speed
- **Audio Controls** — Play, pause, stop per message

### AI Mode
- **OpenRouter Integration** — Connect any model available on OpenRouter
- **Streaming Replies** — Watch responses appear in real-time
- **Token Display** — See prompt and completion token counts per message
- **Session Management** — Create, switch, and delete conversation sessions
- **TTS Voice Replies** — AI responses are automatically spoken via Supertonic
- **Configurable Settings** — API key, model, system prompt, temperature, max tokens

### Shared
- **Persistent Config** — Settings saved to `aura_config.json`
- **Mode Toggle** — Click the mode indicator in the status bar to switch between TTS and AI

## Installation

### Prerequisites

- Python 3.10+

### Setup

```bash
cd supertonic_tts

pip install flask supertonic requests

python aura.py
```

The first run downloads the Supertonic model from Hugging Face automatically.

### Access

Open **http://localhost:2998**

## Configuration

### TTS Settings (Sidebar → config)

| Setting | Description | Range |
|---|---|---|
| `glyph` | Toggle ASCII animation | on/off |
| `lang` | Language code | en, ja, etc. |
| `steps` | Synthesis quality steps | 5-12 |
| `speed` | Speech speed multiplier | 0.7-2.0 |
| `text_ms` | Typewriter animation speed | 0-100ms |

### AI Settings (Sidebar → ai)

| Setting | Description | Example |
|---|---|---|
| `api_key` | Your OpenRouter API key | `sk-or-v1-...` |
| `model` | Model identifier | `anthropic/claude-sonnet-4-20250514` |
| `temp` | Creativity/temperature | 0.0-2.0 |
| `max_tok` | Max response tokens | 256-32768 |
| `system` | System prompt | `You are a helpful assistant.` |

### Getting an OpenRouter API Key

1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to **Keys** in your account settings
4. Create a new API key
5. Copy the key and paste it into the `api_key` field in the AI settings sidebar
6. Click **save** — the app will automatically switch to AI mode

### Popular Models on OpenRouter

| Provider | Model ID |
|---|---|
| Anthropic Claude Sonnet 4 | `anthropic/claude-sonnet-4-20250514` |
| Anthropic Claude Opus 4 | `anthropic/claude-opus-4-20250514` |
| OpenAI GPT-4o | `openai/gpt-4o` |
| Google Gemini 2.5 Pro | `google/gemini-2.5-pro` |
| DeepSeek V4 Flash (free) | `deepseek/deepseek-v4-flash:free` |
| Meta Llama 4 Maverick | `meta-llama/llama-4-maverick` |

Browse all available models at [openrouter.ai/models](https://openrouter.ai/models)

### Config File

Copy `aura_config.example.json` to `aura_config.json` to set defaults:

```bash
cp aura_config.example.json aura_config.json
```

Edit the file to pre-configure your API key, preferred model, and other settings. The `aura_config.json` file is gitignored.

## Usage

### TTS Mode
1. Type a message and press **Enter** (or click **send**)
2. Glyph animation shows the AI thinking, then speaking
3. Audio plays automatically with ▶ ❚❚ ■ controls

### AI Mode
1. Click the mode indicator (`tts`) in the status bar to switch to `ai`
2. Configure your OpenRouter API key and model in the sidebar
3. Type a message and press **Enter**
4. Watch the streaming response appear with token counts
5. The reply is automatically spoken via TTS
6. Create new sessions with the **+ new** button in the sessions panel

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` | Send message |
| `Shift+Enter` | New line |
| `Escape` | Cancel edit / dismiss |

## Project Structure

```
supertonic_tts/
├── aura.py                      # Flask backend
├── templates/
│   └── index.html               # Frontend UI
├── aura_config.json             # User config (gitignored)
├── aura_config.example.json     # Config template
├── aura_sessions.json           # AI conversation sessions
├── requirements.txt             # Python dependencies
└── README.md
```

## Credits

Built on **Supertonic 3** by [Supertone Inc.](https://github.com/supertone-inc/supertonic)

- **Supertonic** — https://github.com/supertone-inc/supertonic
- **OpenRouter** — https://openrouter.ai/

This project is freely open-source.

## License

MIT License
