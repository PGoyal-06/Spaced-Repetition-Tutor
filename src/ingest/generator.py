# src/ingest/generator.py

import os
import json
from openai import OpenAI

# Initialize the v1.x OpenAI client (reads OPENAI_API_KEY from env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FLASHCARD_FN = {
    "name": "create_flashcard",
    "description": "Generate a flashcard (question & answer) from a text passage.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "A concise question covering one fact or concept from the passage."
            },
            "answer": {
                "type": "string",
                "description": "A concise answer to the question."
            }
        },
        "required": ["question", "answer"],
    },
}

def generate_flashcard(chunk_text: str, source_id: str) -> dict:
    """
    Call GPT-4o via function-calling to create a single flashcard (Q/A pair).
    Uses two concrete few-shot examples to force proper question/answer output.
    """
    # 1) System prompt with two examples, using triple quotes to avoid unterminated-string issues
    system_msg = """
You are an educational assistant. When given a short text passage,
you must return exactly one JSON object matching the `create_flashcard` schema.
Do NOT repeat the passage verbatim—always craft a clear question about one fact or concept,
and provide a concise answer.

Example 1:
Passage: "Plants use sunlight to make sugars via photosynthesis."
Response:
{ "question": "What process do plants use to convert light into chemical energy?", "answer": "Photosynthesis" }

Example 2:
Passage: "A script will use whatever shell invoked it. To specify a shell,
you include a hash-bang line (#!<shell>) at the top, for example #!/bin/bash or #!/bin/sh."
Response:
{ "question": "What line do you add at the top of a shell script to specify its interpreter?", "answer": "#!/bin/bash" }
"""

    user_msg = f"Now create a flashcard for this passage (source ID: {source_id}):\n\n{chunk_text}"

    # 2) Call the API
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg},
        ],
        functions=[FLASHCARD_FN],
        function_call={"name": "create_flashcard"},
    )

    # 3) Extract the JSON arguments
    choice = resp.choices[0]
    call = getattr(choice.message, "function_call", None)
    if not call:
        return {"question": "", "answer": "", "source": source_id}

    try:
        args = json.loads(call.arguments)
    except Exception:
        args = {}

    question = args.get("question", "").strip()
    answer   = args.get("answer",   "").strip()

    # 4) Fallback if the model still failed
    if not question or not answer or question.lower() in chunk_text.lower():
        question = "What is the key concept described in this passage?"
        answer   = chunk_text.replace("\n", " ").strip()[:200] + "..."

    return {"question": question, "answer": answer, "source": source_id}
