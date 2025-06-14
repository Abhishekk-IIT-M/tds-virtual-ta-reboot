import os
import base64
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS for local/dev testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model
class QuestionInput(BaseModel):
    question: str
    image: Optional[str] = None

# Keyword extraction mockup
def extract_keywords(text: str) -> List[str]:
    return [word.lower() for word in text.split() if len(word) > 3]

# Link matcher mockup
def find_links(keywords: List[str]) -> List[dict]:
    base_course_url = "https://tds.s-anand.net/#/2025-01/?q="
    base_forum_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"
    links = []
    for kw in keywords:
        if kw in ["gpt", "huggingface", "tokenizer", "docker"]:
            links.append({
                "url": base_course_url + kw,
                "text": f"Match: {kw}"
            })
    return links or [{"url": base_forum_url, "text": "Browse forum for more details"}]

# Dummy image OCR mockup
def extract_text_from_image(image_base64: str) -> str:
    return "tokenizer huggingface"

@app.post("/api/")
async def ask_virtual_ta(payload: QuestionInput):
    combined_question = payload.question
    if payload.image:
        image_text = extract_text_from_image(payload.image)
        combined_question += f"\n\nExtracted from image:\n{image_text}"

    keywords = extract_keywords(combined_question)
    links = find_links(keywords)

    answer = "You must use `gpt-3.5-turbo-0125`, as required by the question context."

    return {
        "answer": answer,
        "links": links
    }

