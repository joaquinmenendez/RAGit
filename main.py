import os

from video_to_subtitle import get_transcription_youtube, add_time_window_to_video
from vector_db import transcription_to_db, load_db
from llm import answer_question_vertex
from embeddings import calculate_tokens
from check_grounding import check_grounding, fact_formatter, add_citations

url = "https://www.youtube.com/watch?v=NgbEL2HbXWw"

raw_transcript, chunked_transcript = get_transcription_youtube(url)
print(f'Number of tokens: {calculate_tokens(raw_transcript)}')

if os.path.exists("./chroma_db"):
    db = load_db()
else:
    db = transcription_to_db(transcriptions=chunked_transcript)


query = 'Que son los miembros manija?'

# LLM naive approach
answer = answer_question_vertex(question=query, context=raw_transcript)
print(f'Respuesta: {answer}')

# Chroma approach
response = db.similarity_search(query, k=3)
answer_context = '\n\n'.join([i.page_content for i in response])
answer_url = add_time_window_to_video(url, metadata=response[0].metadata)
answer = answer_question_vertex(question=query, context=answer_context)
print(f'Respuesta: {answer}\nLink:{answer_url}')

# Test check grounding
facts = fact_formatter([i.page_content for i in response])
grounded = check_grounding(answer_candidate=answer, facts=facts)
answer_with_citations = add_citations(answer_candidate=answer, grounded_response=grounded)