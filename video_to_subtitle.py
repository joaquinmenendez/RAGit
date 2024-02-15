from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re


def get_video_id(video_url):
    youtube_id_match = re.search(r'(?<=v=)[^&#]+', video_url)
    youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+',
                                                     video_url)
    if youtube_id_match:
        return youtube_id_match.group(0)
    else:
        return None


def concatenate_youtube_captions(captions: list[dict], num_words: int = 100) -> list:
    """
    Concatenates captions into multiple chunks with limited number of words per chunk.

    Args:
      captions: A list of captions, where each caption is a dictionary with "text", "start" & "duration" keys.
      num_words: The maximum number of words allowed in each chunk.
                 Default 100 words (this is the default number of word in a minute)

    Returns:
      A list of dictionaries, where each dictionary represents a chunk with "text", "start", and "duration" keys.
    """
    chunks = []
    current_chunk = {"text": "", "start": captions[0]["start"], "duration": 0}

    for caption in captions:
        # Check if the current chunk already has enough words.
        if len(current_chunk["text"].split()) >= num_words:
            chunks.append(current_chunk)
            current_chunk = {"text": "", "start": caption["start"],
                             "duration": 0}
        current_chunk["text"] += " " + caption["text"]
        current_chunk["duration"] += caption["duration"]
    # Add the last chunk (if it has any text).
    if current_chunk["text"]:
        chunks.append(current_chunk)
    return chunks


def concatenate_stt_captions(captions: list[dict], num_words: int = 100) -> list:
    """
    Concatenates captions from Speech-to-Text service into multiple chunks with
    limited number of words per chunk.

    Args:
      captions: A list of captions, where each caption is a dictionary with "text", "start" & "duration" keys.
      num_words: The maximum number of words allowed in each chunk.
                 Default 100 words (this is the default number of word in a minute)

    Returns:
      A list of dictionaries, where each dictionary represents a chunk with "text", "start", and "duration" keys.
    """
    chunks = []
    current_chunk = {"text": "", "start": captions[0]["Start time"], "duration": 0}

    for caption in captions:
        # Check if the current chunk already has enough words.
        if len(current_chunk["text"].split()) >= num_words:
            chunks.append(current_chunk)
            current_chunk = {"text": "", "start": caption["Start time"],
                             "duration": 0}
        current_chunk["text"] += " " + caption["Transcript"]
        current_chunk["duration"] += caption["End time"] - caption["Start time"]
    # Add the last chunk (if it has any text).
    if current_chunk["text"]:
        chunks.append(current_chunk)
    return chunks


# TODO write docstring
def get_transcription_youtube(url: str, languages: list[str] = None):
    """
    Args:
        url:
        languages:

    Returns:

    """
    languages = languages if languages else ['es']
    video_id = get_video_id(url)
    print(YouTubeTranscriptApi.list_transcripts(video_id).find_transcript(
        languages))
    transcript = YouTubeTranscriptApi.get_transcript(video_id,
                                                     languages=languages)
    raw_transcript = TextFormatter().format_transcript(transcript)
    chunked_transcript = concatenate_youtube_captions(captions=transcript)
    return raw_transcript, chunked_transcript


def add_time_window_to_video(url, metadata: dict):
    new_url = url
    start = int(metadata.get('start', 0))
    duration = int(metadata.get('duration', 0))
    end = start + duration

    if start:
        new_url += f"&t={start}"
    if end > start:
        new_url += f"&end={end}"
    return new_url
