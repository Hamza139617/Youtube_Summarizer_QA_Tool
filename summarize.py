from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_summary_prompt():
    """
    create a prompttemplate for summarizing a youtube video transcript
    """

    template = """
You are an AI assistant tasked with summarizing YouTube video transcripts. Provide concise, informative summaries that capture the main points of the video content.

    Instructions:
    1. Summarize the transcript in a single concise paragraph.
    2. Ignore any timestamps in your summary.
    3. Focus on the spoken content (Text) of the video.

    Note: In the transcript, "Text" refers to the spoken words in the video, and "start" indicates the timestamp when that part begins in the video.<|eot_id|><|start_header_id|>user<|end_header_id|>
    Please summarize the following YouTube video transcript:
    {transcript}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["transcript"]
    )

    return prompt

def create_summary_chain(llm, prompt):
    """
    used for creating the chain 
    """

    chain = llm | prompt | StrOutputParser()

    return chain



