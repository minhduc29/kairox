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

def ask_claude(image_b64: str, prompt: str) -> str:
    """Send screenshot + prompt to Claude vision and return the answer."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300, # limit response length (to reduce API cost)
        tools=[
            {
                "type": "web_search_20250305",
                "name": "web_search"
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    # extract text from response (web search adds extra content blocks)
    result = ""
    for block in message.content:
        if block.type == "text":
            result += block.text
    return result

def capture_screen_and_query():
    print("[*] Taking screenshot...")
    img_b64 = take_screenshot()

    print("[*] Asking Claude...")
    prompt = (
        """Look at this screenshot, determine the correct answer, and answer concisely. 
        If it is a multiple choice question, state only the correct option letter and answer, nothing else. 
        If it is a free response question, state the correct answer (if any) and explain in two sentences maximum. 
        You have access to web search — use it if you need to look something up to answer accurately."""
    )
    answer = ask_claude(img_b64, prompt)

    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60 + "\n")

def quit_program():
    print("[*] Quitting.")
    listener.stop()

listener = keyboard.GlobalHotKeys({
    "<ctrl>+<shift>+a": capture_screen_and_query,
    "<esc>": quit_program
})

def main():
    print(f"[*] Kairox running.")
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
