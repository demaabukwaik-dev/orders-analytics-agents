import re
import json
from sys import flags

from llm import ask_llm
from prompts import system_prompt
from actions import load_orders, process_orders, generate_summary
from state import state_for_llm

ALLOWED_ACTIONS = ["load_orders", "process_orders", "generate_summary", "Finish"]


def execute_action(action, state):

    if action == "load_orders":
        load_orders(state)

    elif action == "process_orders":
        process_orders(state)

    elif action == "generate_summary":
        generate_summary(state)


def extract_json(text):
    match = re.search(r"\{.*?\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON returned from LLM")
    return json.loads(match.group(0))


def decide_next_action(current_state):
    user_prompt = f"current_state: {current_state}"
    action_llm = ask_llm(system_prompt, user_prompt)
    action_json = extract_json(action_llm)

    action = action_json.get("next_action")
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Invalid action from LLM: {action}")

    return action


def run_agent(state):

    while True:
        action = decide_next_action(state_for_llm())
        print({"next_action": action})

        if action == "Finish":
            print("Order processing completed.")
            print("-----------------------------------------------------------------------")
            break

        execute_action(action, state)