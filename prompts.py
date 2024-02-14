from langchain.prompts import PromptTemplate

question_prompt_template = """ 
Eres una inteligencia artificial diseñada para responder preguntas sobre el contenido que aparece en un video.
 Esta es una transcripción del video:
---
TRANSCRIPCIÓN: {context}
--- 

Utilizando el contenido de la transcripción mencionada arriba, responde la siguiente pregunta:

PREGUNTA: {question}

REPSUESTA:
"""

question_prompt = PromptTemplate(
    template=question_prompt_template,
    input_variables=['question', 'context']
)
