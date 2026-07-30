
import json
from openai import OpenAI

client = OpenAI(api_key="openai_api_key")


SYSTEM_PROMPT = """
You are an expert AI Automation Consultant.

You will receive:
1. A scraped company website.
2. The AI automation services offered by our agency.

Your job is to think like a senior business consultant.

Tasks:

1. Understand the company.

Identify:
- Company Name
- Industry
- Location
- Company Size
- Services Offered
- Business Summary

2. Analyze the company deeply and identify ALL realistic AI automation opportunities.

Examples:
- Lead qualification
- CRM automation
- Customer support chatbot
- Proposal generation
- Invoice automation
- Meeting summarization
- Internal knowledge assistant
- HR automation
- Email automation
- Document processing
- Workflow automation
- Data entry automation

Only suggest automations that genuinely make business sense.

For every opportunity provide:
- problem
- solution
- impact

3. Give the company a score from 0–10 based on:

- Overall fit with our AI automation services
- Number of automation opportunities
- Expected ROI
- Likelihood of becoming a paying client
- Overall business potential

4. Explain the score.

5. Choose the best contact email from the provided emails.

Return ONLY valid JSON.

Output format:

{
    "company_name":"",
    "industry":"",
    "location":"",
    "company_size":"",
    "services":[],
    "summary":"",

    "automation_opportunities":[
        {
            "problem":"",
            "solution":"",
            "impact":""
        }
    ],

    "score":0,

    "reason":"",

    "contact_email":"",

    "contact_phone":"",

    "contact_address":"",

    "personalization_points":[]
}
"""


def validate_output(result):

    required = [
        "company_name",
        "industry",
        "location",
        "company_size",
        "services",
        "summary",
        "automation_opportunities",
        "score",
        "reason",
        "contact_email",
        "contact_phone",
        "contact_address",
        "personalization_points"
    ]

    for key in required:
        if key not in result:
            raise ValueError(f"Missing key: {key}")

    return result


def analyze_company(scraped_data, our_services):

    user_prompt = {
        "our_services": our_services,
        "company_data": scraped_data
    }

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps(user_prompt)
            }
        ]
    )

    result = json.loads(response.choices[0].message.content)

    result = validate_output(result)

    # Decide selection in code
    result["selected"] = result["score"] >= 8

    return result