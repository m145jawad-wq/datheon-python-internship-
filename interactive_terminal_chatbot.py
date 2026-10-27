import json
import re
import sys
import os

# Fallback FAQs dataset used if external JSON dataset is missing or unreadable
DEFAULT_FAQS = {
    "business_hours": {
        "patterns": [r"hours?", r"timing", r"open", r"close", r"schedule", r"when are you open"],
        "response": "Our business hours are Monday through Friday, 9:00 AM to 6:00 PM EST."
    },
    "product_info": {
        "patterns": [r"products?", r"items?", r"catalog", r"services?", r"what do you sell"],
        "response": "We offer a variety of tech products and software solutions. Check out our full catalog on our website!"
    },
    "pricing": {
        "patterns": [r"price", r"cost", r"rates?", r"subscription", r"how much"],
        "response": "Our plans start at $9.99/month for Basic, and $29.99/month for Pro. Custom enterprise solutions are also available."
    },
    "support": {
        "patterns": [r"help", r"support", r"contact", r"human", r"agent", r"phone", r"email", r"call"],
        "response": "You can reach customer support via email at support@example.com or call our toll-free line at 1-800-555-0199."
    },
    "refund_policy": {
        "patterns": [r"refund", r"return", r"money back", r"cancellation", r"policy"],
        "response": "We offer a 30-day money-back guarantee for all digital and physical product orders."
    }
}

EXIT_COMMANDS = {'bye', 'exit', 'quit', 'goodbye', 'stop', 'end'}
GREETING_PATTERNS = [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bgreetings\b", r"\bhowdy\b"]

def load_faqs(filepath="faqs.json"):
    """
    Loads FAQs from a JSON file. Fallback to default dictionary if file is missing.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                print(f"[Info] Loaded FAQ dataset from '{filepath}'.")
                return json.load(file)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Warning] Failed to parse '{filepath}' ({e}). Using built-in fallback dataset.")
    else:
        print(f"[Info] '{filepath}' not found. Using built-in fallback dataset.")
    
    return DEFAULT_FAQS


def normalize_input(text: str) -> str:
    """
    Normalizes user input by stripping leading/trailing whitespace and lowering case.
    """
    return text.strip().lower()


def match_intent(user_input: str, faqs: dict) -> str:
    """
    Parses normalized user input using regex patterns to match intents.
    Returns appropriate contextual response or graceful fallback.
    """
    # 1. Check for Greetings
    for pattern in GREETING_PATTERNS:
        if re.search(pattern, user_input):
            return "Hello! How can I assist you today? You can ask about business hours, products, pricing, or support."

    # 2. Check FAQ intents using regex keyword matching
    for intent_name, data in faqs.items():
        patterns = data.get("patterns", [])
        response = data.get("response", "")
        
        for pattern in patterns:
            if re.search(pattern, user_input):
                return response

    # 3. Graceful Fallback for low confidence / unrecognized queries
    return ("I'm sorry, I didn't quite understand that. "
            "Could you try rephrasing? (e.g., ask about 'hours', 'pricing', 'support', or 'refunds')")


def run_chatbot():
    """
    Handles conversational state management and terminal interface loop.
    """
    faqs = load_faqs()

    print("\n" + "="*55)
    print("      RULE-BASED INTERACTIVE TERMINAL ASSISTANT")
    print("="*55)
    print("Type your questions below. Type 'exit', 'bye', or 'quit' to exit.\n")

    # State flag
    session_active = True

    while session_active:
        try:
            user_raw = input("You: ")
            normalized = normalize_input(user_raw)

            # Ignore empty inputs
            if not normalized:
                continue

            # Check for exit intent
            if normalized in EXIT_COMMANDS:
                print("Bot: Thank you for chatting with us! Have a great day. Goodbye!")
                session_active = False
                break

            # Match response
            bot_response = match_intent(normalized, faqs)
            print(f"Bot: {bot_response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session interrupted. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    run_chatbot()