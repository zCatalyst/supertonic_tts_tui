# Jarvis TTS Terminal

A terminal-styled voice assistant interface powered by [Supertonic 3](https://github.com/supertone-inc/supertonic) — a state-of-the-art neural text-to-speech model.

Type a message and hear it spoken aloud with a sleek, dense terminal UI.

## Features

- **Terminal UI** — Dense, CLI-style interface with collapsible sidebar
- **10 Voices** — 5 female (F1-F5) and 5 male (M1-M5) voices with editable descriptions
- **8 Themes** — Catppuccin, Matrix, Monokai, Nord, Dracula, Gruvbox, Tokyo Night, Solarized Dark
- **Configurable** — Adjust language, quality steps, speed, and text animation speed
- **Audio Controls** — Play, pause, and stop speech playback per message
- **Persistent Config** — Settings saved to `jarvis_config.json`

## Installation

### Prerequisites

- Python 3.10+

### Setup

```bash
# Clone or navigate to the project
cd supertonic_tts

# Install dependencies
pip install flask supertonic

# Run the application
python jarvis_terminal.py
```

The first run will automatically download the Supertonic model from Hugging Face.

### Access

Open your browser to **http://localhost:2998**

## Usage

1. Type a message in the input area and press **Enter** (or click **send**)
2. The system processes your text and generates speech
3. Audio plays automatically with play/pause/stop controls
4. Use the sidebar to switch voices, themes, and adjust settings

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` | Send message |
| `Shift+Enter` | New line in input |
| `Escape` | Cancel voice description edit |

## Credits

This project is built on top of **Supertonic 3** by [Supertone Inc.](https://github.com/supertone-inc/supertonic)

- **Supertonic** — https://github.com/supertone-inc/supertonic
- **Supertonic 3** — High-quality neural TTS with diffusion-based synthesis

This project is freely open-source.

## License

MIT License
