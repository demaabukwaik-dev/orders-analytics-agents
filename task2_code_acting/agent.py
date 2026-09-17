import pandas as pd

from config import CSV_PATH
from llm import ask_llm
from prompts import build_code_prompt
from mapping import understand_question
from code_exec import execute_code
from helper import extract_code, build_schema


def load_orders():
    df = pd.read_csv(CSV_PATH)
    df["Total_Value"] = df["Quantity"] * df["Price"]
    return df

def run_agent(question, df):
    schema = build_schema(df)

    # 1. Understand + Decide
    decision = understand_question(question, schema)
    if decision["status"] == "ambiguous":
        return {"status": "ambiguous", "question": decision.get("question", "Can you clarify your question?")}

    # 2. Generate Code
    system_prompt, user_prompt = build_code_prompt(
        question, decision.get("intent"), decision.get("mapping"), schema
    )
    code = extract_code(ask_llm(system_prompt, user_prompt))
    print("Code:\n", code)

    # 3. Execute
    try:
        result = execute_code(code, df, pd)
    except Exception as e:
        print("Error:", e)
        return {"status": "error", "code": code, "error": str(e)}

    # 4. Return Result
    print("Result:\n", result)
    return {"status": "success", "mapping": decision.get("mapping"), "code": code, "result": result}