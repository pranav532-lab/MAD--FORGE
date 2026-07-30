import os
import json
from typing import Dict, Any
from openai import OpenAI

client = OpenAI(
    api_key="OPENAI_API_KEY"
)

SYSTEM_PROMPT = """
You are an information extraction assistant.

Your ONLY job is to extract structured information from the user's prompt.

Return ONLY valid JSON.

The JSON must ALWAYS have this structure:

{
  "services": [],
  "industries": [],
  "locations": [],
  "company_types": [],
  "company_characteristics": [],
  "keywords": [],
  "search_goal": ""
}

Rules:

1. Never add explanations.
2. Never use markdown.
3. Never wrap JSON inside ``` blocks.
4. If information is unavailable, return an empty array [].
5. search_goal should be one short sentence.
6. keywords should contain useful search terms.
"""


def process_prompt(user_prompt: str) -> Dict[str, Any]:
    """
    Converts a natural language prompt into structured JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    data = json.loads(response.choices[0].message.content)

    return validate_output(data)


def validate_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures every required key exists.
    """

    schema = {
        "services": [],
        "industries": [],
        "locations": [],
        "company_types": [],
        "company_characteristics": [],
        "keywords": [],
        "search_goal": ""
    }

    for key, default in schema.items():
        if key not in data:
            data[key] = default

    return data


if __name__ == "__main__":

    prompt = """
    I own an AI Automation Agency.

    I build AI chatbots, workflow automations,
    knowledge management systems and internal AI tools.

    Find marketing agencies in Chennai
    that have a good online presence.
    """

    result = process_prompt(prompt)

    print(json.dumps(result, indent=4))