import requests
import os


def check_grounding(answer_candidate: str, facts: list[dict]) -> dict:
    """
    Performs a grounding check using the Google Cloud Discovery Engine API.

    This function sends a POST request to the specified Discovery Engine endpoint,
    providing an answer candidate and a list of supporting facts to be validated.

    Args:
        answer_candidate (str): The answer text to be checked for grounding.
        facts (list): A list of dictionaries, where each dictionary contains a
            'factText' key representing a supporting fact.

    Returns:
        dict: The JSON response from the API if successful.
    """
    endpoint = f"https://discoveryengine.googleapis.com/v1alpha/projects/{ os.environ['PROJECT_ID']}/locations/global/groundingConfigs/default_grounding_config:checkGrounding"
    access_token = os.environ.get('GCLOUD_ACCESS_TOKEN', os.popen("gcloud auth print-access-token").read().strip())
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "answerCandidate": answer_candidate,
        "facts": facts
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()  # Return the API response
    response.raise_for_status()


def fact_formatter(facts: list[str]) -> list[dict]:
    return [{'factText': fact} for fact in facts]


def add_citations(answer_candidate: str, grounded_response: dict) -> str:
    """
    Adds citation quotes to an answer candidate based on the Discovery Engine API response.

    Args:
      answer_candidate (str): The answer text to be augmented with citations.
      grounded_response (dict): The JSON response from the 'check_grounding' API call.

    Returns:
      str: The answer candidate with citation markers appended.
    """

    citations = grounded_response['answerCandidateCitation'].get("citations", [])
    for citation in citations:
        start_pos = int(citation["startPos"])  # Convert to integers for manipulation
        end_pos = int(citation["endPos"])
        citation_marker = f" {citation['citationIndices'] }"
        # Insert citation marker at the end of the cited text
        answer_candidate = answer_candidate[:end_pos] + citation_marker + answer_candidate[end_pos:]
        # Adjust offsets for subsequent citations, as markers change the string length
        end_pos += len(citation_marker)

    return answer_candidate