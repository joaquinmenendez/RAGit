import os
import vertexai

from vertexai.preview.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

vertexai.init(project=os.environ['PROJECT_ID'], location=os.environ['LOCATION'])

def calculate_tokens(text: str) -> int:
    # TODO: docstring
    model = GenerativeModel(os.environ["GENERATIVE_MODEL"])
    return model.count_tokens(text).total_tokens


# TODO: evaluate if its worth it to create a class from langchain_core.embeddings to include the task_type method
def text_embedding(text: str) -> list:
    """Generate text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained(os.environ['EMBEDDING_MODEL'])
    text_embedding_input = TextEmbeddingInput( task_type="RETRIEVAL_DOCUMENT", text=text)
    embeddings = model.get_embeddings([text_embedding_input])
    return embeddings[0].values
