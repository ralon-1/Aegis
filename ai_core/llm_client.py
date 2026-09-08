import ollama

from ai_core.prompt_templates import SYSTEM_PROMPT


def ask_ai(prompt: str, history=None) -> str:

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = ollama.chat(
        model="phi3",
        messages=messages,
        format="json",
        options={"temperature": 0.0}
    )

    return response["message"]["content"]