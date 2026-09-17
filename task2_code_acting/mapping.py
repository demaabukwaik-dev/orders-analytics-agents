from llm import ask_llm
from prompts import build_mapping_prompt
from helper import extract_json


def understand_question(question, schema):
    system_prompt, user_prompt = build_mapping_prompt(question, schema)
    response = ask_llm(system_prompt, user_prompt)
    decision = extract_json(response)
    print("Understanding:", decision)

    if not decision or decision.get("status") not in ("clear", "ambiguous"):
        return {"status": "ambiguous", "question": "I could not understand the question. Can you rephrase it?"}

    if decision["status"] == "clear":
        for col in (decision.get("mapping") or {}).values():
            if col not in schema:
                return {"status": "ambiguous", "question": f"Column '{col}' does not exist. Can you clarify?"}

    return decision