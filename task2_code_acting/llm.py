from openai import OpenAI

from config import MODEL_NAME, BASE_URL, API_KEY

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


def ask_llm(system_prompt, user_prompt):

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return completion.choices[0].message.content