from fastapi import FastAPI
from pydantic import BaseModel

from agent import load_orders, run_agent
from helper import to_json_safe

app = FastAPI()

df = load_orders()


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(request: Question):
    response = run_agent(request.question, df)
    if "result" in response:
        response["result"] = to_json_safe(response["result"])
    return response