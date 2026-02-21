"""Mobile HITL (Human-in-the-Loop) test checklist route.

GET /mobile-test   — interactive checklist for a human tester on their phone.

Each scenario specifies what to do and what to observe.  The tester marks
each one PASS / FAIL / SKIP.  Results are stored in sessionStorage so they
survive page scrolling without hitting the server.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["mobile-test"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

# ── Test scenarios ────────────────────────────────────────────────────────────
# Each dict: id, category, title, steps (list), expected
SCENARIOS = [
    # Layout
    {
        "id": "L01",
        "category": "Layout",
        "title": "Sidebar renders as horizontal strip",
        "steps": [
            "Open the Mission Control page on your phone.",
            "Look at the top section above the chat window.",
        ],
        "expected": (
            "AGENTS and SYSTEM HEALTH panels appear side-by-side in a "
            "horizontally scrollable strip — not stacked vertically."
        ),
    },
    {
        "id": "L02",
        "category": "Layout",
        "title": "Sidebar panels are horizontally scrollable",
        "steps": [
            "Swipe left/right on the AGENTS / SYSTEM HEALTH strip.",
        ],
        "expected": "Both panels slide smoothly; no page scroll is triggered.",
    },
    {
        "id": "L03",
        "category": "Layout",
        "title": "Chat panel fills ≥ 60 % of viewport height",
        "steps": [
            "Look at the TIMMY INTERFACE chat card below the strip.",
        ],
        "expected": "The chat card occupies at least 60 % of the visible screen height.",
    },
    {
        "id": "L04",
        "category": "Layout",
        "title": "Header stays fixed while chat scrolls",
        "steps": [
            "Send several messages until the chat overflows.",
            "Scroll the chat log up and down.",
        ],
        "expected": "The TIMMY TIME / MISSION CONTROL header remains pinned at the top.",
    },
    {
        "id": "L05",
        "category": "Layout",
        "title": "No horizontal page overflow",
        "steps": [
            "Try swiping left or right anywhere on the page.",
        ],
        "expected": "The page does not scroll horizontally; nothing is cut off.",
    },
    # Touch & Input
    {
        "id": "T01",
        "category": "Touch & Input",
        "title": "iOS does NOT zoom when tapping the input",
        "steps": [
            "Tap the message input field once.",
            "Watch whether the browser zooms in.",
        ],
        "expected": "The keyboard rises; the layout does NOT zoom in.",
    },
    {
        "id": "T02",
        "category": "Touch & Input",
        "title": "Keyboard return key is labelled 'Send'",
        "steps": [
            "Tap the message input to open the iOS/Android keyboard.",
            "Look at the return / action key in the bottom-right of the keyboard.",
        ],
        "expected": "The key is labelled 'Send' (not 'Return' or 'Go').",
    },
    {
        "id": "T03",
        "category": "Touch & Input",
        "title": "Send button is easy to tap (≥ 44 px tall)",
        "steps": [
            "Try tapping the SEND button with your thumb.",
        ],
        "expected": "The button registers the tap reliably on the first attempt.",
    },
    {
        "id": "T04",
        "category": "Touch & Input",
        "title": "SEND button disabled during in-flight request",
        "steps": [
            "Type a message and press SEND.",
            "Immediately try to tap SEND again before a response arrives.",
        ],
        "expected": "The button is visually disabled; no duplicate message is sent.",
    },
    {
        "id": "T05",
        "category": "Touch & Input",
        "title": "Empty message cannot be submitted",
        "steps": [
            "Leave the input blank.",
            "Tap SEND.",
        ],
        "expected": "Nothing is submitted; the form shows a required-field indicator.",
    },
    {
        "id": "T06",
        "category": "Touch & Input",
        "title": "CLEAR button shows confirmation dialog",
        "steps": [
            "Send at least one message.",
            "Tap the CLEAR button in the top-right of the chat header.",
        ],
        "expected": "A browser confirmation dialog appears before history is cleared.",
    },
    # Chat behaviour
    {
        "id": "C01",
        "category": "Chat",
        "title": "Chat auto-scrolls to the latest message",
        "steps": [
            "Scroll the chat log to the top.",
            "Send a new message.",
        ],
        "expected": "After the response arrives the chat automatically scrolls to the bottom.",
    },
    {
        "id": "C02",
        "category": "Chat",
        "title": "Multi-turn conversation — Timmy remembers context",
        "steps": [
            "Send: 'My name is <your name>.'",
            "Then send: 'What is my name?'",
        ],
        "expected": "Timmy replies with your name, demonstrating conversation memory.",
    },
    {
        "id": "C03",
        "category": "Chat",
        "title": "Loading indicator appears while waiting",
        "steps": [
            "Send a message and watch the SEND button.",
        ],
        "expected": "A blinking cursor (▋) appears next to SEND while the response is loading.",
    },
    {
        "id": "C04",
        "category": "Chat",
        "title": "Offline error is shown gracefully",
        "steps": [
            "Stop Ollama on your host machine (or disconnect from Wi-Fi temporarily).",
            "Send a message from your phone.",
        ],
        "expected": "A red 'Timmy is offline' error appears in the chat — no crash or spinner hang.",
    },
    # Health panel
    {
        "id": "H01",
        "category": "Health",
        "title": "Health panel shows Ollama UP when running",
        "steps": [
            "Ensure Ollama is running on your host.",
            "Check the SYSTEM HEALTH panel.",
        ],
        "expected": "OLLAMA badge shows green UP.",
    },
    {
        "id": "H02",
        "category": "Health",
        "title": "Health panel auto-refreshes without reload",
        "steps": [
            "Start Ollama if it is not running.",
            "Wait up to 35 seconds with the page open.",
        ],
        "expected": "The OLLAMA badge flips from DOWN → UP automatically, without a page reload.",
    },
    # Scroll & overscroll
    {
        "id": "S01",
        "category": "Scroll",
        "title": "No rubber-band / bounce on the main page",
        "steps": [
            "Scroll to the very top of the page.",
            "Continue pulling downward.",
        ],
        "expected": "The page does not bounce or show a white gap — overscroll is suppressed.",
    },
    {
        "id": "S02",
        "category": "Scroll",
        "title": "Chat log scrolls independently inside the card",
        "steps": [
            "Scroll inside the chat log area.",
        ],
        "expected": "The chat log scrolls smoothly; the outer page does not move.",
    },
    # Safe area / notch
    {
        "id": "N01",
        "category": "Notch / Home Bar",
        "title": "Header clears the status bar / Dynamic Island",
        "steps": [
            "On a notched iPhone (Face ID), look at the top of the page.",
        ],
        "expected": "The TIMMY TIME header text is not obscured by the notch or Dynamic Island.",
    },
    {
        "id": "N02",
        "category": "Notch / Home Bar",
        "title": "Chat input not hidden behind home indicator",
        "steps": [
            "Tap the input field and look at the bottom of the screen.",
        ],
        "expected": "The input row sits above the iPhone home indicator bar — nothing is cut off.",
    },
    # Clock
    {
        "id": "X01",
        "category": "Live UI",
        "title": "Clock updates every second",
        "steps": [
            "Look at the time display in the top-right of the header.",
            "Watch for 3 seconds.",
        ],
        "expected": "The time increments each second in HH:MM:SS format.",
    },
]


@router.get("/mobile-test", response_class=HTMLResponse)
async def mobile_test(request: Request):
    """Interactive HITL mobile test checklist — open on your phone."""
    categories: dict[str, list] = {}
    for s in SCENARIOS:
        categories.setdefault(s["category"], []).append(s)
    return templates.TemplateResponse(
        request,
        "mobile_test.html",
        {"scenarios": SCENARIOS, "categories": categories, "total": len(SCENARIOS)},
    )
