import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
import tempfile
import pdfplumber
from typing import List, Optional
from llm import llm_response, llm_generate_score
import pandas as pd

# import pandas as pd

app = FastAPI(
    title="Criteria Extraction API",
    description="Extract criteria from job descriptions",
)


@app.post("/extract-criteria")
async def extract_criteria(file: UploadFile = File(...)):
    """
    Extract criteria from a job description file (PDF or DOCX)

    Args:
        file: Uploaded job description file (PDF or DOCX)

    Returns:
        JSON response indicating success and message
    """
    # Validate file type
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400, detail="Only PDF and DOCX files are supported"
        )

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # TODO: Add logic to extract criteria from the PDF or DOCX file

        with pdfplumber.open(temp_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        criteria = llm_response(text)

        os.unlink(temp_file_path)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Successfully processed file: {file.filename}",
                "criteria": criteria.criteria,
            },
        )

    except Exception as e:
        if "temp_file_path" in locals():
            os.unlink(temp_file_path)

        raise HTTPException(
            status_code=500, detail=f"An error occurred during processing: {str(e)}"
        )


@app.post("/score-resumes")
async def score_resumes(files: List[UploadFile] = File(...), criteria: str = Form()):
    """
    Score resumes against specified criteria

    Args:
        criteria: JSON string containing list of criteria
        files: List of uploaded resume files (PDF or DOCX)

    Returns:
        JSON response with scores for each resume
    """
    try:
        # Parse the criteria JSON string into a Python list
        criteria_list = json.loads(criteria)

        if not isinstance(criteria_list, list):
            raise HTTPException(
                status_code=400,
                detail="Criteria must be a JSON-encoded list of strings",
            )

        # Validate files
        for file in files:
            if not file.filename.endswith((".pdf", ".docx")):
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is not supported. Only PDF and DOCX files are accepted.",
                )

        # List to store results for each resume
        list_of_scores = []

        for file in files:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(file.filename)[1]
            ) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            # TODO: Add logic to extract criteria from the PDF or DOCX file

            with pdfplumber.open(temp_file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            os.unlink(temp_file_path)

            scores = llm_generate_score(text, criteria_list)
            list_of_scores.append(dict(scores))
            output_csv = pd.DataFrame(list_of_scores).to_csv()
            # TODO load list of dict as pandas df. Then output df as csv and return

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "csv": output_csv,
            },
        )

    except Exception as e:
        if "temp_file_path" in locals():
            os.unlink(temp_file_path)

        raise HTTPException(
            status_code=500, detail=f"An error occurred during processing: {str(e)}"
        )
