import os
from typing import List
from dotenv import load_dotenv
from mistralai import Mistral
from pydantic import BaseModel, create_model
import re


load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])


class ExtractedCriteria(BaseModel):
    criteria: list[str]


class ExtracteUsername(BaseModel):
    username: str


def llm_response(job_description):
    chat_response = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Given the parsed job description. Extract top 5 job criteria. These criteria are to be then used to score from 1-5 each so it needs to be brief and can be used to score resumes against.",
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


def llm_generate_score(job_resume, scoring_criteria):

    scoring_criteria_cleaned = [
        re.sub(r"[^a-zA-Z0-9]", "_", s) for s in scoring_criteria
    ]
    scoring_class = create_class_from_strings(scoring_criteria_cleaned, "ScoreResume")
    system_prompt = f"""Given the parsed job resume. Return the following
                  username: Extracted name of the candidate in format first name followed by a space then second name. If candidate name has more than two names then keep the same format just add space for each name.
                    {"   ".join(f"{score}: Score candidate resume from 1 - 5 according to this criteria" for score in scoring_criteria_cleaned)}
                  """
    candidate_name = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": job_resume,
            },
        ],
        response_format=scoring_class,
        max_tokens=256,
        temperature=0,
    )
    response = candidate_name.choices[0].message.parsed
    return response


def create_class_from_strings(strings: List[str], class_name: str = "DynamicModel"):

    field_definitions = {string: (str, "5") for string in strings}
    field_definitions["username"] = (str, "")
    dynamic_model = create_model(class_name, **field_definitions)
    return dynamic_model
