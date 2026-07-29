# 🎥 VidMind — YouTube Summarizer & RAG Q&A Bot

> **Turn long YouTube videos into interactive knowledge.**

VidMind is a Python-based AI application that lets you **summarize YouTube videos and have conversations about their content**.

Instead of watching a long coding tutorial or lecture just to find one specific answer, you can paste the YouTube URL, generate a summary, and ask questions directly about the video.

---

## ✨ How It Works

VidMind has two main capabilities:

### 📝 1. Video Summarization

```text
YouTube URL
     ↓
YouTube Transcript API
     ↓
Transcript Processing
     ↓
Text Chunking (for long videos)
     ↓
Groq LLM
     ↓
Video Summary
```

The application extracts the video's transcript, processes it, and sends it to a Groq-powered LLM to generate a concise summary.

For longer transcripts, the content is divided into smaller chunks and summarized before producing the final summary.

---

### 🔎 2. RAG-Based Q&A

When the user asks a question about the video:

```text
YouTube Transcript
       ↓
Text Chunking
       ↓
Hugging Face Embeddings
       ↓
FAISS Vector Store
       ↓
Similarity Search
       ↓
Relevant Transcript Chunks
       ↓
Context + Question
       ↓
LangChain Prompt
       ↓
Groq LLM
       ↓
Answer
```

Instead of passing the entire transcript to the LLM, VidMind retrieves the **most relevant pieces of the transcript** using semantic similarity search.

This is the core of the project's **Retrieval-Augmented Generation (RAG)** pipeline.

---

## 🧠 Conversational Memory

VidMind also supports conversational follow-up questions.

It uses:

* `RunnableWithMessageHistory`
* `InMemoryChatMessageHistory`
* `MessagesPlaceholder`

to maintain the conversation history.

For example:

```text
User: What is RAG?

AI: RAG stands for Retrieval-Augmented Generation...

User: Why is it useful?

AI: It is useful because...
```

The second question can be interpreted in the context of the previous conversation.

`RunnableWithMessageHistory` is designed specifically to wrap a runnable and manage its chat message history using a session ID.

---

## 🛠️ Tech Stack

| Technology                            | Used For                       |
| ------------------------------------- | ------------------------------ |
| 🐍 **Python**                         | Core application               |
| 🔗 **LangChain**                      | RAG pipeline, prompts & memory |
| ⚡ **Groq**                            | LLM inference                  |
| 🗂️ **FAISS**                         | Vector similarity search       |
| 🤗 **Hugging Face**                   | Text embeddings                |
| 🎥 **YouTube Transcript API**         | Transcript extraction          |
| ✂️ **RecursiveCharacterTextSplitter** | Transcript chunking            |
| 💬 **Gradio**                         | Web interface                  |
| 🔐 **python-dotenv**                  | Environment variables          |

The project uses LangChain's `ChatGroq` integration to connect to Groq-hosted chat models.

---

## 🏗️ Project Structure

```text
VidMind/
│
├── main.py
├── interface.py
├── summarize.py
├── ai_model.py
├── transcript.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

### `main.py`

The entry point of the application.

```python
from interface import create_interface

def main():
    create_interface()

if __name__ == "__main__":
    main()
```

---

### `interface.py`

Responsible for the **Gradio UI**.

It creates:

* YouTube URL input
* Summary output
* Question input
* Answer output
* Summarize button
* Q&A button

The UI connects these components directly to the backend functions:

```python
summarize_btn.click(
    summarize_video,
    inputs=video_url,
    outputs=summary_output
)

question_btn.click(
    answer_question,
    inputs=[video_url, question_input],
    outputs=answer_output
)
```

---

### `transcript.py`

Handles the YouTube data pipeline:

```text
YouTube URL
     ↓
Extract Video ID
     ↓
Fetch Transcript
     ↓
Process Transcript
     ↓
Split Into Chunks
```

The `RecursiveCharacterTextSplitter` is used to divide large transcripts into manageable chunks.

---

### `ai_model.py`

Responsible for initializing the AI components:

```python
ChatGroq(...)
```

for the LLM,

```python
HuggingFaceEmbeddings(...)
```

for embeddings, and:

```python
FAISS.from_texts(...)
```

for creating the vector index.

---

### `summarize.py`

This is the main application logic.

It brings the components together to create:

* Summary generation
* RAG retrieval
* Question answering
* Prompt templates
* Chat memory
* LangChain chains

The RAG chain follows the basic LangChain pipeline:

```python
prompt | llm | parser
```

while the Q&A chain is wrapped with:

```python
RunnableWithMessageHistory(...)
```

to maintain conversational context.

---

## 🔄 Overall Architecture

```text
                    ┌─────────────────┐
                    │   YouTube URL   │
                    └────────┬────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Transcript API      │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Process & Chunk      │
                  │ Transcript           │
                  └──────────┬──────────┘
                             ↓
                 ┌──────────────────────┐
                 │ Hugging Face         │
                 │ Embeddings           │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │       FAISS          │
                 │  Vector Similarity   │
                 └──────────┬───────────┘
                            ↓
                       User Question
                            ↓
                 ┌──────────────────────┐
                 │ Retrieve Relevant    │
                 │ Transcript Chunks    │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ LangChain Prompt     │
                 │ + Chat History       │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │      Groq LLM        │
                 └──────────┬───────────┘
                            ↓
                    Generated Answer
```

---

## 🔑 Key Concepts Demonstrated

This project demonstrates practical implementation of:

* **Retrieval-Augmented Generation (RAG)**
* **Vector embeddings**
* **FAISS similarity search**
* **Semantic retrieval**
* **LangChain LCEL**
* **Prompt engineering**
* **Conversational memory**
* **LLM integration**
* **Transcript processing & chunking**
* **Gradio AI interfaces**

---

## 🚀 The Idea

The goal behind VidMind is simple:

> **Don't watch an entire video just to find one answer.**

**Paste the URL → Get the summary → Ask questions → Talk to the video.** 🎥🤖
