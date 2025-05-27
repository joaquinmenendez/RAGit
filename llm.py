import vertexai
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, SafetySetting

from vertexai.preview.generative_models import GenerativeModel
from prompts import question_prompt, fill_punctuation_prompt

VERTEX_SAFETY_SETTINGS = {
    genai.types.HarmCategory.HARM_CATEGORY_SEXUAL: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_VIOLENCE: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_TOXICITY: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_DEROGATORY: genai.types.HarmBlockThreshold.BLOCK_NONE
}


def add_punctuation(raw_transcription: str) -> str:
    vertexai.init(project=os.environ['PROJECT_ID'],
                  location=os.environ['LOCATION'])

    model = GenerativeModel("gemini-1.0-pro")
    prompt = fill_punctuation_prompt.format_prompt(
        raw_transcription=raw_transcription).text
    print("RAGit! DEBUG: add_punctuation using model: gemini-1.0-pro")
    response = model.generate_content(
        contents=prompt, safety_settings=VERTEX_SAFETY_SETTINGS
    )
    return response.text


def answer_question_vertex(question: str, context: str) -> str:
    vertexai.init(project=os.environ['PROJECT_ID'],
                  location=os.environ['LOCATION'])

    model = GenerativeModel("gemini-1.0-pro")
    prompt = question_prompt.format_prompt(question=question,
                                           context=context).text
    print("RAGit! DEBUG: answer_question_vertex using model: gemini-1.0-pro")
    response = model.generate_content(contents=prompt,
                                      safety_settings=VERTEX_SAFETY_SETTINGS
                                      )
    return response.text


def answer_question_genai(question: str, context: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.0-pro")
    prompt = question_prompt.format_prompt(question=question,
                                           context=context).text
    print("RAGit! DEBUG: answer_question_genai using model: gemini-1.0-pro")
    response = model.generate_content(contents=prompt,
                                      safety_settings=[
                                          SafetySetting(category=HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=HarmBlockThreshold.BLOCK_NONE),
                                          SafetySetting(category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=HarmBlockThreshold.BLOCK_NONE),
                                          SafetySetting(category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=HarmBlockThreshold.BLOCK_NONE),
                                          SafetySetting(category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=HarmBlockThreshold.BLOCK_NONE),
                                      ])
    return response.text
