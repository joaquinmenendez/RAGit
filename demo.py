# Before running, ensure PROJECT_ID and LOCATION environment variables are set.

import os
import vertexai

# Attempt to import llm and embeddings functions
try:
    from llm import add_punctuation, answer_question_vertex
    from embeddings import text_embedding
except ModuleNotFoundError as e:
    print(f"Error importing RAGit modules: {e}")
    print("Please ensure that llm.py and embeddings.py are in the same directory or accessible in PYTHONPATH.")
    print("Also, ensure all dependencies from requirements.txt are installed.")
    exit(1)
except ImportError as e:
    print(f"Error importing specific functions: {e}")
    print("Please check the function names and definitions in llm.py and embeddings.py.")
    exit(1)

# --- Initialization ---
PROJECT_ID = os.environ.get('PROJECT_ID')
LOCATION = os.environ.get('LOCATION')

if not PROJECT_ID:
    print("Error: Please set the PROJECT_ID environment variable.")
    exit(1)
if not LOCATION:
    print("Error: Please set the LOCATION environment variable.")
    exit(1)

try:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    print(f"Vertex AI initialized successfully with project {PROJECT_ID} in {LOCATION}")
except Exception as e:
    print(f"Error initializing Vertex AI: {e}")
    print("Please ensure your Google Cloud credentials are set up correctly and the project/location are valid.")
    exit(1)

# --- Demonstrate add_punctuation ---
print("\n--- Punctuation Demo ---")
raw_text_punctuation = "hello world this is a test how are you i hope this works"
print(f"Original text for punctuation: '{raw_text_punctuation}'")
try:
    punctuated_text = add_punctuation(raw_text_punctuation)
    print(f"Punctuated text: '{punctuated_text}'")
except Exception as e:
    print(f"Error during add_punctuation: {e}")
    # Print debug statements if they exist, as they might indicate model issues
    if "RAGit! DEBUG" in str(e): # A simple check
        print("This might be related to the model call within add_punctuation.")
print("--- End of Punctuation Demo ---\n")

# --- Demonstrate RAG Q&A ---
print("\n--- RAG Q&A Demo ---")
context_qa = ("The Gemini 1.0 Pro model is a large language model created by Google. "
              "It can be used for various tasks like translation, summarization, and question answering. "
              "This project, RAGit, uses Gemini 1.0 Pro to answer questions about video transcripts after processing them.")
question_qa = "What is Gemini 1.0 Pro and how is it used in the RAGit project?"

print(f"Context for Q&A: '{context_qa}'")
print(f"Question for Q&A: '{question_qa}'")

try:
    # Demonstrate text_embedding
    print("Generating embedding for the context...")
    context_embedding = text_embedding(context_qa)
    # It's a long vector, so just print confirmation and a small part of it.
    print(f"Generated embedding for context (first 5 values): {context_embedding[:5]}...")
    
    # Demonstrate answer_question_vertex
    print("Answering question using RAG setup...")
    answer = answer_question_vertex(question=question_qa, context=context_qa) 
    print(f"Answer from LLM: '{answer}'")
except ModuleNotFoundError as e: # Catching here as well if a sub-module fails
    print(f"A module was not found during RAG Q&A: {e}")
    print("This could be due to an issue with a dependency of the RAG functions.")
except Exception as e:
    print(f"Error during RAG Q&A: {e}")
    # Print debug statements if they exist
    if "RAGit! DEBUG" in str(e):
        print("This might be related to the model calls within text_embedding or answer_question_vertex.")

print("--- End of RAG Q&A Demo ---")

print("\nDemo script finished.")
