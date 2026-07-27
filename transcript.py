import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_video_id(url: str):
    """
    For capturing the video id
    """

    pattern = r'https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None



def get_transcript(url : str):
    """
    For getting all the transcripts
    """

    video_id = get_video_id(url)

    if video_id is None:
        return None

    ytt_api = YouTubeTranscriptApi()

    transcripts = ytt_api.list(video_id)

    transcript = ""

    for t in transcripts:

        if t.language_code == 'en':
            if t.is_generated:

                if len(transcript) == 0:
                    transcript = t.fetch()
            else:

                transcript = t.fetch()
                break

    return transcript if transcript else None



def process(transcript : List):
    """
    For processing the transcript
    """

    txt = ""

    for i in transcript:

        try:
            txt += f"Text: {i.text} Start: {i.start}\n"
        except KeyError as k:
            print(f"There was an error while processing transcript \n Error : {k}")
            pass

    return txt



def chunk_transcript(processed_transcript: str, chunk_size: int = 400, chunk_overlap: int = 10):
    """
    for chunking
    """

    if processed_transcript is None:
        return None
    

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.split_text(processed_transcript)
    return chunks



