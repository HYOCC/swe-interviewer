from openai import OpenAI
import os
from dotenv import load_dotenv

# Loads the api_key from a secure file called openAI_key.env
load_dotenv()
api_key = os.getenv('gpt_key')

if api_key: # Checks for valid api_key
    client = OpenAI(api_key=api_key) 
else:
    print('failed get OpenAI API Key\nPlease make sure filed is called openAI_key.env and inside contains OPENAI_API_KEY=\'YOUR KEY\'')

# Overall AI 
class ai():
    def __init__(self, job_description=None):
        self.job_description = job_description 



# AI responsible for the coding section 
class coding_ai(ai):
    def __init__(self, job_description=None):
        super().__init__(job_description)
        
        self.instruction = (
        "Generate Software Engineering coding questions at a difficulty level between LeetCode Medium and Hard. "
        "Format responses using HTML elements such as <b>, <i>, or <p> to enhance readability and presentation. "
        "Ensure the output is suitable for direct assignment to the .innerHTML property of an HTML element. "
        "Align the content and style with LeetCode's structured and professional format, and tailor each question to fit the provided job description if applicable."
        "dont include ```html ``` any where"
        )
    
    def start(self):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.instruction},
                {
                    'role': 'assistant',
                    'content': 'ask one coding question. User will be coding in python'
                }
            ],
            stream=True # Enable streaming for smaller chunks
        )

        
        
        return completion 
            
            



