import vertexai
import os
import google.generativeai as genai

from vertexai.preview.generative_models import GenerativeModel
from prompts import question_prompt

VERTEX_SAFETY_SETTINGS = {
    genai.types.HarmCategory.HARM_CATEGORY_SEXUAL: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_VIOLENCE: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_TOXICITY: genai.types.HarmBlockThreshold.BLOCK_NONE,
    genai.types.HarmCategory.HARM_CATEGORY_DEROGATORY: genai.types.HarmBlockThreshold.BLOCK_NONE
}


def answer_question_vertex(question: str, context: str) -> str:
    vertexai.init(project=os.environ['PROJECT_ID'],
                  location=os.environ['LOCATION'])

    model = GenerativeModel(os.environ["GENERATIVE_MODEL"])
    prompt = question_prompt.format_prompt(question=question,
                                           context=context).text
    response = model.generate_content(contents=prompt,
                                      safety_settings=VERTEX_SAFETY_SETTINGS
                                      )
    return response.text


def answer_question_genai(question: str, context: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(os.environ["GENERATIVE_MODEL"])
    prompt = question_prompt.format_prompt(question=question,
                                           context=context).text
    response = model.generate_content(contents=prompt,
                                      safety_settings={
                                          'harassment': 'block_none',
                                          'hate_speech': 'block_none',
                                          'sexual': 'block_none',
                                          'dangerous': 'block_none',
                                      })
    return response.text
