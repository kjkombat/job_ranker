# job_ranker
part of an assessment
## Getting Started
Follow these steps to set up and run the project:
### Prerequisites

Python 3.8 or higher
uv package manager

### Setup Instructions

1. Clone the repository:
bash
`Copygit clone https://github.com/username/repo-name.git
cd repo-name`

2. Set up a virtual environment and install dependencies using uv:
bash
`
# Install uv if you don't have it already
pip install uv

# Create and activate a virtual environment
uv venv

# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install dependencies from requirements.in
uv pip install -r requirements.in
`
3. Set up .env file
Add .env file at same directory level as main.py. Follow is the sample.
`
MISTRAL_API_KEY = "" #Your mistral key here
`

3. Run the application:
bashCopypython main.py
The server will start, typically on http://127.0.0.1:8000

### API Documentation
Once the application is running, you can access the Swagger documentation at:
http://127.0.0.1:8000/docs

This interactive documentation allows you to explore and test all available API endpoints.

### Core Functionality
The application uses the Mistral AI LLM to analyze job descriptions and resumes. The core functionality includes:
LLM Module
The `llm.py` file contains the implementation for interacting with the Mistral LLM API:

1. Criteria Extraction: Analyzes job descriptions to extract the top 5 criteria that can be used for resume scoring.
2. Resume Scoring: Evaluates a candidate's resume against the extracted job criteria, providing a numerical score (1-5) for each criterion.
3. Dynamic Model Generation: Creates Pydantic models on-the-fly to structure the LLM output based on the specific job criteria.

The API endpoints that leverage this functionality are fully documented in the Swagger interface.

### Contributing

Here's how you can contribute:

#### Reporting Issues

- Use the GitHub issue tracker to report bugs or suggest features
- Clearly describe the issue including steps to reproduce when it is a bug
- Make sure to include relevant information and logs

#### Submitting Changes

- Create a new branch (git checkout -b feature/your-feature-name)
- Make your changes
- Run the tests to ensure nothing breaks
- Commit your changes (git commit -am 'Add some feature')
- Push to the branch (git push origin feature/your-feature-name)
- Create a new Pull Request

#### Pull Request Guidelines

- Update the README.md with details of changes if applicable
- The PR should work against the main branch
- Follow the existing code style
- One pull request per feature