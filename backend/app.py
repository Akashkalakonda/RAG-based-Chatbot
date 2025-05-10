from flask import Flask, request, jsonify
from scraper import search_and_scrape
from llm import generate_response
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Initialize LangChain memory
memory = ConversationBufferMemory()

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query')
        logger.info(f"Received query: {user_query}")

        # Scrape content
        scraped_content = search_and_scrape(user_query)
        logger.debug(f"Scraped content length: {len(scraped_content)}")

        # Generate response
        response = generate_response(user_query, scraped_content)

        # Update memory
        memory.save_context({"input": user_query}, {"output": response})

        return jsonify({"response": response})
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)