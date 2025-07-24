#WebRAG
RAG-based-Chatbot


A chatbot for retrieving real-time current affairs and general information using Streamlit, SerpAPI, Hugging Face Inference API, and LangChain.

## Project Overview
The WebRAG Chatbot is designed to provide accurate and context-aware responses to user queries, with a focus on current affairs (e.g., 2025 Pahalgam terror attack) and general knowledge (e.g., AI, Indian Army).
It leverages web scraping for up-to-date information, a large language model for response generation, and conversational memory for follow-up queries. The chatbot features a user-friendly Streamlit interface and a robust Flask backend.

## Features
- **Real-Time Web Scraping**: Uses SerpAPI and BeautifulSoup to fetch current information from news and Wikipedia sources, ensuring responses reflect events up to May 2025.
- **LLM Integration**: Employs Hugging Face's `mistralai/Mixtral-8x7B-Instruct-v0.1` for generating concise, context-based answers.
- **Conversational Memory**: LangChain’s `ConversationBufferMemory` maintains chat history, enabling coherent follow-up responses (e.g., “What was the response to that attack?”).
- **Frontend**: Streamlit provides an intuitive chat interface for user interaction.
- **Backend**: Flask API processes queries, integrating scraping and LLM components.
- **Error Handling**: Robust logging and retries for API and scraping failures.



## Prerequisites
- **Operating System**: Windows 10/11 (or compatible OS, e.g., macOS, Linux).
- **Python**: Version 3.8 or higher.
- **Git**: For cloning the repository (optional).
- **API Keys**:
  - SerpAPI key from [serpapi.com](https://serpapi.com/).
  - Hugging Face API key from [huggingface.co](https://huggingface.co/).
- **Internet Connection**: Required for web scraping and LLM API calls.

## Setup Instructions
Follow these steps to set up the DeepEdge AI Chatbot locally.

1. **Clone the Repository** (if using Git):
   git clone https://github.com/Akashkalakonda/RAG-based-Chatbot.git
   cd RAG-based-Chatbot


**Running Instructions**:
  - The "Necessary Instructions for Running the Application" section is prominently placed and detailed, covering:
    - Starting the Flask backend (`python app.py`).
    - Starting the Streamlit frontend (`streamlit run app.py`).
    - Using the chatbot interface (`http://localhost:8501`).
      
