# Kairox

Kairox is an AI-powered program that lets you instantly capture your screen using hotkeys and send it to an LLM (e.g., OpenAI or Claude) for quick Q&A and problem solving.

---

## 🧠 Overview

Kairox removes the friction of copy-pasting into AI tools.

Instead of:

- taking screenshots manually
- switching tabs
- pasting into ChatGPT/Claude

You can:

- press a hotkey
- capture your screen
- get an answer directly in your terminal

Kairox acts as a real-time assistant. For example, if you're working through a problem or studying for a quiz and get 
stuck, you can instantly capture your screen and receive contextual help without breaking your workflow.

---

## ⚙️ How it works

```
Hotkey → Screen Capture → Context Builder → LLM API → CLI Output
```

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/minhduc29/kairox.git
cd kairox
```

---

### 2. Create and activate virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_claude_key_here
```

> ⚠️ Do NOT commit your `.env` file. Use `.env.example` as a template.

---

### 5. Run the program

```bash
python3 main.py
```

---

### 6. Usage

- Press your configured hotkey to capture screen and sends to LLM
- Output will be displayed in the terminal

*(More modes/hotkeys coming soon)*

---

## ⚠️ Notes

This project is built for:

- personal use
- experimentation
- learning

The codebase is customized to my needs. That said, it currently only works on macOS. However, it’s structured so others 
can explore, learn from it, or build on top of it.

---

## 🤝 Contributing

Contributions, ideas, and experiments are welcome. Feel free to open issues or PRs.
