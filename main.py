import os
import pandas as pd

from video_to_subtitle import get_transcription_youtube, \
    concatenate_stt_captions
from vector_db import transcription_to_db, load_db
from llm import answer_question_vertex, add_punctuation
from embeddings import calculate_tokens
from check_grounding import check_grounding, fact_formatter, add_citations, \
    links_to_references

# Get transcripts directly from YouTube ---------------------------------------
url = "https://www.youtube.com/watch?v=NgbEL2HbXWw"

raw_transcript, chunked_transcript = get_transcription_youtube(url)
print(f'Number of tokens: {calculate_tokens(raw_transcript)}')

# Add punctuation (YouTube's generated transcripts does not have punctuation) --
corrected_transcription = add_punctuation(raw_transcript)

# Using StT transcriptions -----------------------------------------------------
stt_df = pd.read_csv(
    './multimedia/el_origen_de_los_distintos_acentos_de_argentina_datazo.csv')
chunked_transcript_stt = concatenate_stt_captions(stt_df.to_dict('records'),
                                                  num_words=130)
[c.update({'url': url}) for c in chunked_transcript_stt]

# Mount Chroma DB --------------------------------------------------------------
if os.path.exists("./chroma_db"):
    db = load_db()
else:
    # db = transcription_to_db(transcriptions=chunked_transcript)
    db = transcription_to_db(transcriptions=chunked_transcript_stt)

# Define question --------------------------------------------------------------
query = 'Cómo se llama el libro de los acentos?'

# LLM naive approach (use entire transcript) -----------------------------------
if calculate_tokens(raw_transcript) < 30000:
    answer = answer_question_vertex(question=query, context=corrected_transcription)
    print(f'Respuesta: {answer}')
else:
    raise NotImplementedError('Transcription is too long')

# Chroma approach with check grounding ----------------------------------------
response = db.similarity_search(query, k=3)  # TODO: Langchain retrievers

answer_context = '\n\n'.join([i.page_content for i in response])
answer = answer_question_vertex(question=query, context=answer_context)

facts = fact_formatter([i.page_content for i in response])

grounded = check_grounding(answer_candidate=answer, facts=facts)
answer_with_citations, references = add_citations(answer_candidate=answer,
                                                  grounded_response=grounded)
print(answer_with_citations)
print(links_to_references(response, references))
