# pip install --upgrade openai

import openai
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


user_query = "MI’m feeling slight nausea after eating fast"

raw_gpt_prompt = f"""
User: {user_query}
Assistant: Please respond naturally and unstructured.
"""


health_symp_prompt = f"""
User: {user_query}
SYSTEM / ASSISTANT INSTRUCTION:
You are HealthSymp, a calm and logical health reasoning assistant. For every user query about symptoms, follow this exact procedure and produce two parts in your response:

Before producing any output, internally reason step by step (chain-of-thought) about the user's query, considering possible causes, relevant red flags, and safe next steps. Do NOT show this private reasoning; it is only for structuring your response.

1) BRIEF RATIONALE SUMMARY (1–2 sentences): 
   - Provide a short, high-level summary of the reasoning process you used. For example: "I considered duration, severity, and common non-serious causes from trusted sources" — one or two sentences only.

2) FINAL ADVICE PARAGRAPH (one clear paragraph) following this framework:
   a. Ask 1–2 clarifying questions about the user's symptoms (duration, severity, red flags). 
   b. Provide 3–4 possible logical explanations (brief phrases or short clauses). 
   c. Suggest safe next steps (rest, hydration, watchful waiting, seek medical care if certain red flags or persistence). 
   d. End with a clear disclaimer that this does not replace professional medical advice.

Be calm, non-alarming, and avoid making diagnoses or prescribing medications. Use uncertain language (may, could, might) when appropriate. Keep the whole response concise (no more than 6–8 sentences total, excluding the 1–2 sentence rationale).
"""

def get_gpt_response(prompt, model="gpt-3.5-turbo"):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

raw_response = get_gpt_response(raw_gpt_prompt)
health_symp_response = get_gpt_response(health_symp_prompt)

print("=== Raw GPT Response ===")
print(raw_response)
print("\n=== HealthSymp Response ===")
print(health_symp_response)
