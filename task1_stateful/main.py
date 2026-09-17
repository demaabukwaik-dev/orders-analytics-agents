from fastapi import FastAPI
from pydantic import BaseModel

from state import state, state_for_llm
from agent import decide_next_action, execute_action

app = FastAPI()


# define the state format expected by the API
class OrderState(BaseModel):
    data_loaded: bool
    orders_processed: bool
    summary_generated: bool


# handle order processing requests
@app.post("/orders")
def orders(request_state: OrderState):

    # put the flags from the request into the agent state
    state.update(request_state.model_dump())

    action = decide_next_action(state_for_llm())

    if action == "Finish":
        return {
            "next_action": "Finish",
            "summary": state["summary"]
        }

    execute_action(action, state)

    return {
        "next_action": action,
        "state": state_for_llm()
    }