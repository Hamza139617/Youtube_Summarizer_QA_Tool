from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory



from transcript import get_transcript, process, chunk_transcript
from ai_model import creating_llm, creating_embedding_model, create_faiss_index


embedding_model = creating_embedding_model()
processed_transcript = ""

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

    chain =  prompt | llm | StrOutputParser()

    return chain


def retrieving_summary(query, faiss_index, k=7):
    """
    Retrieve relevant context from the FAISS index based on the user's query
    """

    relevant_context = faiss_index.similarity_search(query, k=k)

    return relevant_context


def create_qa_prompt_template():
    """
    for creating the prompt template for question and answering based on video content
    """

    qa_template = """
You are an expert assistant providing detailed answers based on the following video content.

    Relevant Video Context: {context}

    Based on the above context, please answer the following question:
    Question: {question}
"""

    prompt = PromptTemplate(
        template=qa_template,
        input_variables=["context", "question"]
    )

    return prompt



def generate_answer(question, faiss_index, qa_chain, k=7):
    """
    Retrieve relevant context and generate an answer based on user input
    """

    relevant_context = retrieving_summary(question, faiss_index, k=k)

    answer = qa_chain.invoke({"context":relevant_context, "question": question})

    return answer


def summarize_video(video_url: str):
    """
    For summarizing the video
    """

    global fetched_transcript, processed_transcript

    if video_url:
        fetched_transcript = get_transcript(video_url)
        processed_transcript = process(fetched_transcript)
    else:
        return "Please provide a valid Youtube URL."

    if processed_transcript:

        llm = creating_llm()

        summary_prompt = create_summary_prompt()

        summary_chain = create_summary_chain(llm, summary_prompt)

        try:
            summary = summary_chain.invoke({"transcript":processed_transcript})
        except:
            try:
                chunks = chunk_transcript(processed_transcript, chunk_size=3000, chunk_overlap=200)

                chunk_summaries = [summary_chain.invoke({"transcript":chunk}) for chunk in chunks]

                combine_summaries = "\n".join(chunk_summaries)

                summary = summary_chain.invoke({"transcript":combine_summaries})

            except Exception as e:
                print(f"Error : {e}")

                summary = "The video is too long\n Sorry couldn't summarize it "

        return summary

    else:

        return "No transcript available. Please fetch the transcript first"
        


def answer_question(video_url, user_question):
    """
    for answering the user question and also summarizing the youtube video
    """

    global fetched_transcript, processed_transcript

    if not processed_transcript:
        if video_url:

            fetched_transcript = get_transcript(video_url)
            processed_transcript = process(fetched_transcript)
        else:
            return "Please provide a valid Youtube URL"


    if processed_transcript and user_question:

        chunks = chunk_transcript(processed_transcript)

        llm = creating_llm()

#        embedding_model = creating_embedding_model()

        faiss_index = create_faiss_index(chunks, embedding_model)

        qa_prompt = create_qa_prompt_template()
        qa_chain = create_summary_chain(llm, qa_prompt)

        answer = generate_answer(user_question, faiss_index, qa_chain)
        return answer
    else:
        return "Please provide a valid question and ensure the transcript has been fetched."

