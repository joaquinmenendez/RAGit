# RAGit!

## Overview
This project has been refactored to utilize newer Google generative AI models. The `llm.py` module now employs "gemini-1.0-pro" for generative tasks such as punctuation addition and question answering. For generating text embeddings, `embeddings.py` uses the "text-embedding-004" model. These changes aim to leverage the latest advancements in generative AI for improved performance and capabilities.

## Setup and Configuration
Before running any Python scripts in this project, you need to configure your environment by setting the following environment variables:

*   `PROJECT_ID`: Your Google Cloud Project ID. This is required for Vertex AI services to identify your project.
*   `LOCATION`: The Google Cloud location/region where your Vertex AI services are hosted (e.g., "us-central1", "europe-west4").

You can set these variables in your terminal session like this:

```bash
export PROJECT_ID="your-gcp-project-id"
export LOCATION="your-gcp-location"
```
Replace `"your-gcp-project-id"` and `"your-gcp-location"` with your actual project ID and location.
For some functionalities, particularly those directly using the Generative AI API (like `answer_question_genai` in `llm.py`), a `GOOGLE_API_KEY` might also be necessary.

## Running the Demo (`demo.py`)
The `demo.py` script is provided to offer a straightforward way to test some of the core functionalities of the RAGit project. It showcases:
1.  Adding punctuation to a sample raw text.
2.  A basic Retrieve-Augment-Generate (RAG) question-answering cycle using a sample context and question. It demonstrates text embedding generation and then uses the Vertex AI endpoint (`answer_question_vertex`) for answering.

To run the demo, navigate to the project's root directory in your terminal and execute:
```bash
python demo.py
```
Ensure that the `PROJECT_ID` and `LOCATION` environment variables are set as described in the "Setup and Configuration" section. The script includes error handling for missing modules and environment variables.

## Known Issues
During development and testing within the provided sandbox environment, the following significant issue was encountered:

*   **`ModuleNotFoundError: No module named 'google.generativeai'`**:
    *   Execution of both `main.py` (in previous subtasks) and `demo.py` was consistently blocked by this error.
    *   This error persisted despite `google-ai-generativelanguage>=0.6.0` (which should provide the `google.generativeai` module) being correctly specified in `requirements.txt` and multiple attempts to reinstall, update, and force-reinstall dependencies. Adjustments to `PYTHONPATH` were also attempted without success.
    *   This suggests a potential environment-specific issue within the development sandbox that may require further investigation to resolve the module discoverability problem. Users attempting to run this project in a different environment should ensure their Python setup correctly recognizes the installed `google-ai-generativelanguage` package.

## To Do
- [ ] Get text from video 
  - [x] Youtube API (unofficial)
  - [ ] GCP StT automatic
  - [ ] Local StT models (abstract class)
- [x] Function to perform embedding (multilingual gecko)
- [x] Lift Vector DB (vector search? or Chroma?)
- [x] RAG prompt (query answer)
- [x] Generate citations to document/chunk (Check grounding? Citation?)
- [x] Get starting time for a chunk
- [ ] Wrap up all together

### Extra mile
- [ ] Implement [Semantic Chunking](https://python.langchain.com/docs/modules/data_connection/document_transformers/semantic-chunker) to create chunks (default is len words)
- [ ] Optimize StT by adding punctuation (LLM calling)
- [ ] Dynamically select the prompt by using the language in the video (worth it?  what if query is in a != language?)
- [ ] Enable RAG fusion


## Videos
1 - [El ORIGEN de los distintos ACENTOS de Argentina](https://www.youtube.com/watch?v=NgbEL2HbXWw), id: NgbEL2HbXWw
