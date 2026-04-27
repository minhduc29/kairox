import anthropic
import base64
import os
import subprocess
import tempfile
from dotenv import load_dotenv
from pynput import keyboard

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def take_screenshot() -> str:
    """Take a screenshot on macOS and return it as a base64 string."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_path = f.name
    subprocess.run(["screencapture", "-i", tmp_path]) # only works on macOS
    with open(tmp_path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    os.unlink(tmp_path)
    return data

def ask_claude(image_b64: str | None = None, text: str | None = None) -> str:
    """Send prompt to Claude API and return the answer."""
    if not image_b64 and not text:
        raise ValueError("At least one of image or text must be provided for context.")

    # Build prompt content based on given image and text
    content = []
    if image_b64:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_b64,
            }
        })

    prompt = """Help me determine the correct answer, and answer concisely. 
If it is a multiple choice question, state only the correct option letter and answer, nothing else. 
If it is a free response question, state the correct answer (if any) and explain in two sentences maximum. 
You have access to web search — use it if you need to look something up to answer accurately."""
    content.append({
        "type": "text",
        "text": f"{prompt}{f"\nContext: {text}" if text else ""}", # same prompt for both image and text
    })

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300, # limit response length (to reduce API cost)
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search"
        }],
        messages=[{
            "role": "user",
            "content": content,
        }],
    )

    # Extract text from response (web search adds extra content blocks)
    result = []
    for block in message.content:
        if block.type == "text":
            result.append(block.text)
    return "".join(result)

def capture_screen_and_query():
    print("[*] Taking screenshot...")
    img_b64 = take_screenshot()

    print("[*] Asking Claude...")
    answer = ask_claude(img_b64)

    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60 + "\n")

def query_clipboard():
    text = subprocess.check_output(["pbpaste"]).decode("utf-8")
    if not text:
        print("[*] No text in clipboard.")
        return

    print("[*] Asking Claude with clipboard text...")
    answer = ask_claude(text=text)

    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60 + "\n")

def print_hotkeys():
    print("[*] Hotkeys:")
    print("\tCtrl+Shift+H - Print this list")
    print("\tCtrl+Shift+A - Capture screen and query")
    print("\tCtrl+Shift+C - Query clipboard text")
    print("\tEsc - Quit\n")

def quit_program():
    print("[*] Quitting.")
    listener.stop()

listener = keyboard.GlobalHotKeys({
    "<ctrl>+<shift>+a": capture_screen_and_query,
    "<ctrl>+<shift>+c": query_clipboard,
    "<ctrl>+<shift>+h": print_hotkeys,
    "<esc>": quit_program
})

def main():
    print(f"[*] Kairox running.")
    print(f"    Press Ctrl+Shift+H for list of hotkeys\n")
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
