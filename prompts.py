from langchain.prompts import PromptTemplate

_question_prompt_template = """ 
Eres una inteligencia artificial diseñada para responder preguntas sobre el contenido que aparece en un video.
 Esta es una transcripciÓn del video:
---
TRANSCRIPCIÓN: {context}
--- 

Utilizando el contenido de la transcripcion mencionada arriba, responde a la pregunta. 

PREGUNTA: {question}

REPSUESTA:
"""
question_prompt = PromptTemplate(
    template=_question_prompt_template,
    input_variables=['question', 'context']
)
