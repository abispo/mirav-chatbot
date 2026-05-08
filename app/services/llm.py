from openai import OpenAI
from app.core.config import settings
from app.prompts import system_prompt, user_prompt
from app.services.search import search_perfumes


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(user_query: str):
    results = search_perfumes(user_query)

    perfumes_context = "\n\n".join([
    f"""
Perfume: {r[2]}
Descrição: {r[1]}
"""
    for r in results
])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt.format(
                    perfumes_context=perfumes_context,
                    user_query=user_query
                )
            }
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response.choices[0].message.content