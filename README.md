Rule-Based Interactive Terminal Assistant / Chatbot

A Python-based interactive customer support assistant that handles queries using regex pattern matching and JSON-driven dataset resolution.

Features

JSON Dataset Loading: Dynamically loads FAQ patterns and responses from faqs.json.

Built-in Fallbacks: Uses default responses if the JSON dataset is missing or corrupted.

Input Normalization: Case-folding and whitespace trimming for robust parsing.

Regex Keyword Extraction: Matches intent using regex patterns.

State Management: Smooth conversation loop with clean exit keywords (exit, bye, quit).

How to Run

Place chatbot.py and faqs.json in the same directory.

Run the script using Python 3:

python chatbot.py
