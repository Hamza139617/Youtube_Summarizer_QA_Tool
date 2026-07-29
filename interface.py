import gradio as gr
from summarize import summarize_video, answer_question

def create_interface():
    """
    creates a visually attracting interface for the client
    """
    with gr.Blocks() as interface:
        video_url = gr.Textbox(label="Youtube Video URL ", placeholder="Enter your URL")

        summary_output = gr.Textbox(label="Video Summary")
        question_input = gr.Textbox(label="Ask a Question About the Video", placeholder="e.g. What is the topic of the video")
        answer_output = gr.Textbox(label="Answer to Your Question")

        summarize_btn = gr.Button("Summarize Video")
        question_btn = gr.Button("Ask a Question")



        summarize_btn.click(summarize_video, inputs=video_url, outputs=summary_output)
        question_btn.click(answer_question, inputs=[video_url, question_input], outputs=answer_output)

    interface.launch(server_name="0.0.0.0", server_port=7860)


