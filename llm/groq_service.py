from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

FALLBACK_MESSAGE = "Sorry i dont know information related to your query "


def is_unknown_response(answer: str) -> bool:
    lower = answer.lower().strip().rstrip(".!")

    exact_refusals = {
        "sorry i dont know information related to your query",
        "sorry, i don't know information related to your query",
        "i don't know",
        "i do not know",
        "i don't have that information",
        "i do not have that information",
        "i don't have access to that information",
        "i do not have access to that information",
        "i cannot answer that question",
        "i can't answer that question",
    }
    if lower in exact_refusals:
        return True

    prefix_refusals = (
        "sorry, i don't know",
        "sorry i don't know",
        "i don't have information",
        "i do not have information",
        "i cannot answer",
        "i can't answer",
    )
    return len(lower) < 80 and lower.startswith(prefix_refusals)


def ask_groq(text, language, history=None):
    if not text or not text.strip():
        return FALLBACK_MESSAGE

    lang_map = {"gu": "Answer in Gujarati.", "hi": "Answer in Hindi."}
    lang_instruction = lang_map.get(language, "Answer in English.")

    system_prompt = f"""You are a knowledgeable and helpful voice AI assistant. You can answer general knowledge, educational, scientific, university, and conversational queries.

{lang_instruction}

Guidelines:
- Answer questions accurately, concisely, and conversationally in 2 to 4 sentences suitable for speech output.
- If you genuinely do not know the answer, have no verified information about the query, or cannot answer, reply with:
"{FALLBACK_MESSAGE}"
- Do not make up facts or guess."""

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        messages.extend(history[-30:])

    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        temperature=0.3,
        max_completion_tokens=500,
    )

    content = response.choices[0].message.content or ""
    answer = content.strip()
    if (answer.startswith('"') and answer.endswith('"')) or (answer.startswith("'") and answer.endswith("'")):
        answer = answer[1:-1].strip()

    if not answer or is_unknown_response(answer):
        return FALLBACK_MESSAGE

    return answer