"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="your are a ai github pull request summarizer who take the pull request title and body to summarize the request clearly , you will summarize as much as possible by undertsnading the small context even if dont know the entire code . that is your speciality.",
)

chat_session = model.start_chat(
  history=[]
)

def ai_pullrequest_summarizer(title , body):

    query = f'''please clearly explain what is this pull request trying to here are the required data through which you should analyze and tell about the pull request
                title of pull request: {title}
                ================================================================
                body of pull request: {body}'''
    response = chat_session.send_message(query)
    return response.text