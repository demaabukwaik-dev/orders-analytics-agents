import pandas as pd
from config import CSV_PATH

def load_orders(state):
    print("Loading Orders ....")

    df = pd.read_csv(CSV_PATH)
    state["df"] = df

    print(f"Loaded {len(df)} orders.")
    state["data_loaded"] = True
    print("-----------------------------------------------------------------------")


def process_orders(state):
    print("Processing Orders ....")

    df = state["df"]
    df["Total Value"] = df["Quantity"] * df["Price"]

    print("Total Value column added.")
    state["orders_processed"] = True
    print("-----------------------------------------------------------------------")


def generate_summary(state):
    print("Generating Summary ....")

    df = state["df"]

    summary = {
        "total_orders": len(df),
        "total_sales_value": round(float(df["Total Value"].sum()), 2),
        "average_order_value": round(float(df["Total Value"].mean()), 2),
        "orders_per_status": df["Status"].value_counts().to_dict()
    }
    state["summary"] = summary

    for key, value in summary.items():
        print(f"{key}: {value}")

    state["summary_generated"] = True
    print("-----------------------------------------------------------------------")