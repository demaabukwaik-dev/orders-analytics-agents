state = {
    "data_loaded": False,
    "orders_processed": False,
    "summary_generated": False,
    "df": None,
    "summary": None
}


def state_for_llm():
    return {
        "data_loaded": state["data_loaded"],
        "orders_processed": state["orders_processed"],
        "summary_generated": state["summary_generated"]
    }