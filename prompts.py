from langchain.prompts import PromptTemplate

question_prompt_template = """ 
Eres una inteligencia artificial diseñada para responder preguntas sobre el contenido que aparece en un video.
 Esta es una transcripción del video:
---
TRANSCRIPCIÓN: {context}
--- 

Utilizando el contenido de la transcripción mencionada arriba, responde la siguiente pregunta.
Si la pregunta es compleja respondela por partes:

PREGUNTA: {question}

REPSUESTA:
"""

question_prompt = PromptTemplate(
    template=question_prompt_template,
    input_variables=['question', 'context']
)


fill_punctuation_template = """
Eres un experto trascribiendo videos. Tu tarea consiste en editar trasncripciones de video sin puntuación ni mayúsculas 
y devolver la misma transcripción con puntuación, comas y mayúsculas correctas.

Ejemplo:

Entrada:

el dia de hoy vamos a hablar sobre la importancia de la puntuacion en la escritura

Salida:

El día de hoy vamos a hablar sobre la importancia de la puntuación en la escritura.

Instrucciones:

Analiza la entrada:

Identifica las palabras, frases y oraciones dentro de la transcripción.
Reconoce los diferentes tipos de palabras (sustantivos, verbos, adjetivos, etc.).
Detecta la estructura de las oraciones (sujeto, verbo, objeto).
Predice la puntuación:

Coma (,): Separa elementos dentro de una frase.
Punto (.): Indica el final de una oración.
Punto y coma (;): Separa dos oraciones independientes relacionadas entre sí.
Puntos suspensivos (...): Indican que la oración está incompleta o que se omite información.
Signos de interrogación (?): Indican una pregunta.
Signos de exclamación (!): Indican sorpresa, énfasis o emoción.
Predice las mayúsculas:

Primera letra de la oración: Debe ser mayúscula.
Nombres propios: Deben comenzar con mayúscula.
Títulos y cargos: Deben comenzar con mayúscula.
Considera el contexto:

El estilo de puntuación puede variar según el contexto y el tipo de texto.
Es importante ser consistente con la puntuación a lo largo de la transcripción.
La puntuación correcta puede mejorar la legibilidad y la comprensión del texto.

Entrada: {raw_transcription}

Salida:
"""
fill_punctuation_prompt = PromptTemplate(
    template=fill_punctuation_template,
    input_variables=["raw_transcription"]
)