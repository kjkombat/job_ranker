from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
import pdfplumber
from llm import llm_response

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
