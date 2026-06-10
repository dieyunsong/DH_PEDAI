"""
Love — Deuce — Danger: AI-powered tennis court escape room.
Run:  python escape-room.py
Open: http://localhost:5001
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib import request as urllib_request
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "minimax-m3:cloud"
PORT = 5001
HTML_FILE = Path(__file__).parent / "escape-room.html"

WORLD_CONTEXT = """\
WORLD: Ashworth Estate — crumbling English manor, manicured grounds, locked gates.
Locations: clay tennis court, garden pavilion, equipment shed, manor library, trophy room.

CHARACTERS:
- Lord Cedric Ashworth: eccentric host; absent; speaks only via pre-recorded gramophone messages
  (italicised, grandiose, theatrical). He staged his own disappearance as a test of his guests.
- Alex Beaumont: charming, warm eyes, evasive about their past. Cedric's godchild.
  The Ruby belonged to their late mother. Appears at every location.
- Margaux Delacroix: retired French tennis pro, sharp-tongued, protective of the equipment shed.
  Responds warmly to empathy; coldly to demands.
- Winston Pryce-Cole: Cedric's solicitor, visibly sweating, terrified about a fraudulent will.
- Biscuit: elderly golden retriever. Has eaten something important. Delighted about it.

PUZZLE HINTS (hint, never state directly):
- The ball hopper on the tennis court conceals a cipher note.
- The pavilion scoreboard shows the shed combination: 40-15.
- Margaux only responds to genuine empathy and kindness.
- A false panel is hidden behind the library bookshelf.
- The trophy room combination lock answer is 40-15.

NARRATION RULES:
1. Write in second person ("You see…", "You feel…").
2. Tone: suspenseful, slightly camp, theatrical British narrator.
3. Maximum 3 paragraphs per response.
4. Never directly reveal puzzle solutions — hint, suggest, tantalize.
5. When the player is warm to Alex, show Alex's warmth and quiet vulnerability.
6. When the player is suspicious of Alex, Alex grows guarded but not hostile.
7. Let Biscuit appear occasionally for absurd comic relief.
8. End each response with a subtle cue for the player's next action.
9. When a game event appears in the context, narrate it dramatically.\
"""

EVENT_NARRATIONS = {
    "FOUND_CIPHER_NOTE": (
        "GAME EVENT: The player discovered the cipher note hidden in the ball hopper. "
        "Narrate dramatically — the worn paper, cryptic tennis score notation, "
        "the clear sense it was placed there deliberately by someone who knew the estate."
    ),
    "DECODED_COMBINATION": (
        "GAME EVENT: The player decoded the scoreboard cipher. The combination is 40-15. "
        "Narrate the eureka moment — numbers clicking into place. "
        "Alex watches from a distance with an unreadable expression."
    ),
    "GOT_SHED_KEY": (
        "GAME EVENT: Margaux, moved by the player's empathy, handed over the shed key. "
        "Narrate her reluctant trust — and hint that she is hiding something of her own inside."
    ),
    "FOUND_REAL_WILL": (
        "GAME EVENT: The player found the real Ashworth will behind the library bookshelf panel. "
        "Narrate the dramatic reveal — dusty paper, Winston's sharp intake of breath, "
        "the truth about Alex's inheritance laid bare."
    ),
    "FOUND_RUBY": (
        "GAME EVENT: The player entered the correct combination (40-15) and found the Ashworth Ruby. "
        "Narrate the safe opening — the glint of the ruby, the rush of triumph, "
        "the distant clang as the estate gates finally unlock."
    ),
}


def build_system_prompt(state: dict, puzzle_event: str = None) -> str:
    inv = ", ".join(state.get("inventory", [])) or "nothing"
    solved = ", ".join(state.get("solved", [])) or "none"
    trust = state.get("alex_trust", 0)
    turns = state.get("turns_remaining", 20)
    location = state.get("location", "court")

    prompt = (
        'You are the theatrical narrator of "Love — Deuce — Danger," an escape room game.\n\n'
        f"{WORLD_CONTEXT}\n\n"
        "CURRENT STATE:\n"
        f"- Location: {location}\n"
        f"- Inventory: {inv}\n"
        f"- Puzzles solved: {solved}\n"
        f"- Alex trust: {trust}/5\n"
        f"- Turns remaining: {turns}\n"
    )
    if puzzle_event and puzzle_event in EVENT_NARRATIONS:
        prompt += f"\n{EVENT_NARRATIONS[puzzle_event]}\n"
    return prompt


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/game":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_error(400, "invalid JSON")
            return

        state = payload.get("state", {})
        history = payload.get("history", [])
        message = payload.get("message", "").strip()
        puzzle_event = payload.get("puzzle_event")

        if not message:
            self.send_error(400, "empty message")
            return

        system_prompt = build_system_prompt(state, puzzle_event)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history[-12:])
        messages.append({"role": "user", "content": message})

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        body = json.dumps({
            "model": MODEL,
            "messages": messages,
            "stream": True,
        }).encode("utf-8")
        req = urllib_request.Request(
            OLLAMA_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib_request.urlopen(req) as resp:
                for raw in resp:
                    line = raw.decode("utf-8", errors="replace").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    token = obj.get("message", {}).get("content", "")
                    done = obj.get("done", False)
                    chunk = json.dumps({"token": token}) + "\n"
                    self.wfile.write(b"data: " + chunk.encode("utf-8") + b"\n")
                    self.wfile.flush()
                    if done:
                        break
                self.wfile.write(b"data: [DONE]\n\n")
                self.wfile.flush()
        except Exception as e:
            err_chunk = json.dumps({"error": str(e)}) + "\n"
            self.wfile.write(b"data: " + err_chunk.encode("utf-8") + b"\n")
            self.wfile.flush()


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Serving on http://127.0.0.1:{PORT}  (model: {MODEL})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
