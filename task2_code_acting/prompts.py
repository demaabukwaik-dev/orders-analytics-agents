def build_mapping_prompt(question, schema):
    system_prompt = f"""
You understand questions about an orders dataset.

Dataset columns and types:
{schema}

For columns with listed values, use only those exact values.

Your job:
1. Understand what the user wants.
2. Map every word in the question that refers to data to an exact column name.
   The user may use different words than the column names.
   Examples of such mappings:
   "item" -> Product, "cost" -> Price, "number of items" -> Quantity, "order state" -> Status
3. Decide if the question is clear or ambiguous.

Column rules:
- Always answer using the existing columns as they are.
- Do NOT create or suggest a derived value (a value calculated from other columns),
  unless the user's own words explicitly ask for a combined amount.
- Never treat a derived value as an alternative meaning of a word.

Clear or ambiguous:
- A question is clear when its words point to an existing column, or to values inside a column. Use them.
- If a word describes a state or category, match it to the listed values with the closest meaning.
- A question is ambiguous only when its words do not point to any specific column, and several columns fit.
- Do not guess in that case. Ask a short clarification question with the possible options.

Use ONLY column names from the list above.

Return ONLY one JSON object, in one of these forms:
{{"status": "clear", "intent": "what the user wants, in one short sentence", "mapping": {{"user word": "Column"}}}}
{{"status": "ambiguous", "question": "Do you mean ...?"}}
"""
    user_prompt = f"Question: {question}"
    return system_prompt, user_prompt


def build_code_prompt(question, intent, mapping, schema):
    system_prompt = f"""
You write pandas code for an existing DataFrame named df.

Dataset columns and types:
{schema}

Rules:
- Use only the column names listed above, exactly as written.
- Always use bracket access: df["Column"].
- Do not import anything. pd is already available.
- No loops, no functions, no print.
- Store the final answer in a variable named result.
- Return ONLY executable Python code. No explanation, no markdown.
"""
    user_prompt = f"""Question: {question}
Intent: {intent}
Column mapping: {mapping}"""
    return system_prompt, user_prompt