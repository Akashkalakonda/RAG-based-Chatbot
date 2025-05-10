from huggingface_hub import InferenceClient
import logging
import re
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

memory = ConversationBufferMemory()

def generate_response(query, context, retries=3, delay=2):
    try:
        if not HUGGINGFACE_API_KEY:
            logger.error("HUGGINGFACE_API_KEY not found in .env file")
            return "Error: HUGGINGFACE_API_KEY not found in .env file."
        
        logger.info("Initializing InferenceClient for mistralai/Mixtral-8x7B-Instruct-v0.1")
        client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token=HUGGINGFACE_API_KEY, timeout=30)
        
        memory_context = memory.load_memory_variables({}).get("history", "")
        is_current_affairs = any(keyword in query.lower() for keyword in ["current affairs", "attack", "terror", "news", "2025"])
        if is_current_affairs and not context.strip():
            return "Error: No recent information found for the query. Please try a more specific query or check reliable news sources."
        
        # Truncate context to 4000 characters to fit within Mixtral's limits
        truncated_context = context[:4000]
        input_prompt = (
            f"You are an assistant with access to recent web-scraped information. "
            f"For queries about current affairs or events after October 2021, rely EXCLUSIVELY on the provided context and conversation history, "
            f"ignoring any internal knowledge. Summarize key details (e.g., dates, events, outcomes) from the context. "
            f"If the context is insufficient, state so clearly. "
            f"Conversation History: {memory_context}\n"
            f"Context: {truncated_context or 'No context available.'}\n"
            f"Question: {query}\n"
            f"Answer in 1-2 sentences, using only the context and history for current affairs: "
        )
        
        for attempt in range(retries):
            try:
                logger.info(f"Generating response (attempt {attempt + 1})")
                response = client.text_generation(
                    input_prompt,
                    max_new_tokens=200,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True
                )
                cleaned_response = re.sub(r'.*Answer in 1-2 sentences:\s*', '', response, flags=re.DOTALL).strip()
                
                if not cleaned_response or len(cleaned_response.split()) < 5:
                    cleaned_response = "Sorry, I couldn't generate a clear answer based on the provided context. Please try rephrasing the query."
                
                memory.save_context({"input": query}, {"output": cleaned_response})
                logger.debug(f"Generated response: {cleaned_response}")
                return cleaned_response
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise
        raise Exception("All retry attempts failed.")
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"Error generating response: {str(e)}."

































































