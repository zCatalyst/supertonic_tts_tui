# Aura

A TUI-styled web frontend for voice synthesis powered by [Supertonic 3](https://github.com/supertone-inc/supertonic) — a state-of-the-art neural text-to-speech model.

Type a message and hear it spoken aloud through a sleek, terminal-inspired interface with live glyph animations.

## Features

- **TUI-styled web UI** — Dense, CLI-inspired design with collapsible sidebar
- **10 Voices** — 5 female (F1-F5) and 5 male (M1-M5) with editable descriptions
- **8 Themes** — Wabi-Sabi, Catppuccin, Matrix, Monokai, Nord, Dracula, Gruvbox, Tokyo Night
- **Live Glyph Animations** — Braille-pattern ASCII art that breathes, thinks, and speaks
- **Configurable** — Language, quality steps, speed, text animation speed
- **Audio Controls** — Play, pause, stop per message
- **Persistent Config** — Settings saved to `aura_config.json`

## Installation

### Prerequisites

- Python 3.10+

### Setup

```bash
cd supertonic_tts

pip install flask supertonic

python aura.py
```

The first run downloads the Supertonic model from Hugging Face automatically.

### Access

Open **http://localhost:2998**

## Usage

1. Type a message and press **Enter** (or click **send**)
2. Glyph animation shows the AI thinking, then speaking
3. Audio plays automatically with ▶ ❚❚ ■ controls
4. Use the sidebar to switch voices, themes, toggle glyphs, and adjust settings

### Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` | Send message |
| `Shift+Enter` | New line |
| `Escape` | Cancel voice description edit |

## Credits

Built on **Supertonic 3** by [Supertone Inc.](https://github.com/supertone-inc/supertonic)

- **Supertonic** — https://github.com/supertone-inc/supertonic
- **Supertonic 3** — High-quality neural TTS with diffusion-based synthesis

This project is freely open-source.

## License

MIT License
