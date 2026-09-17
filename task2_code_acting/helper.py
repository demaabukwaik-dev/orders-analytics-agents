import re
import json

import pandas as pd


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def extract_code(text):
    code = text.strip()
    code = code.replace("```python", "").replace("```", "")
    return code.strip()

def build_schema(df):
    schema = {}
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]) and df[col].nunique() <= 10:
            schema[col] = {"type": "text", "values": sorted(df[col].dropna().unique().tolist())}
        else:
            schema[col] = str(df[col].dtype)
    return schema

def to_json_safe(result):
    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")
    if isinstance(result, pd.Series):
        return result.to_dict()
    if hasattr(result, "item"):
        return result.item()
    return result