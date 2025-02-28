import os
from dotenv import load_dotenv
from mistralai import Mistral
from pydantic import BaseModel


load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])


class ExtractedCriteria(BaseModel):
    criteria: list[str]


def llm_response(job_description):
    chat_response = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Given the parsed job description. Extract the top 5 job criteria.",
            },
            {
                "role": "user",
                "content": job_description,
            },
        ],
        response_format=ExtractedCriteria,
        max_tokens=256,
        temperature=0,
    )
    response = chat_response.choices[0].message.parsed
    return response
