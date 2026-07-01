# BriefAI

An autonomous AI document agent that finds, reads, and summarizes your local files using natural language.

## What it does
- Searches your Documents, Downloads, and Desktop for PDFs and Word files
- Accepts drag and drop file uploads directly in the UI
- Reads and summarizes file contents using a ReAct agent loop powered by GPT-4o-mini
- Returns clean, structured answers in a consumer-grade dark UI built with Streamlit

## Tech Stack
Python, Streamlit, OpenAI GPT-4o-mini, ReAct Agent, pypdf, python-docx, Docker

## Run locally
pip install -r requirements.txt
streamlit run UI.py

## Run with Docker
docker build -t briefai .
docker run -p 8501:8501 --env-file .env briefai

<img width="1907" height="890" alt="image" src="https://github.com/user-attachments/assets/fcdc60d8-afce-43f6-8fcf-889bf5ee0d09" />
<img width="1862" height="858" alt="image" src="https://github.com/user-attachments/assets/f0b2a375-df8e-4279-ab99-63bd28172d67" />

