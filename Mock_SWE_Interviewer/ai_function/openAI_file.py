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

# Queues user mesasge to be proccessed by openAI
def send_message(message, history):
    print(f'adding message to chatgpt chat history: \'{message}\' | send_message\n')# Log    
    history.append({'role':'user', 'content':message})
    print(f'Current chat history:\n{history} | send_message\n')

# Process the chat history and sends the response without stream 
def process_response_no_streaming(history): 
    
    print(f'processing response for chat history: {history} | process_response_no_streaming\n') # Log
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
    
    print(f'completion response:\n{completion} | process_response_no_streaming\n')# Log 
    
    return completion 

# Process the chat history and sends the response with stream
def process_response_yes_streaming(history): 
    
    print(f'processing response for chat history: {history} | process_response_yes_streaming\n') # Log
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        streaming = True # Streams the response in part 
    )

    print(f'completion response:\n{completion} | process_response_yes_streaming\n')# Log 
    
    return completion 

def log_ai_response(response: str, history: list):
    
    print(f'loggin ai\'s response: \'{response}\' to chat history\n{history} | log_ai_response\n')# Log
    
    history.append({'role': 'assistant', 'content': response})
    

# Overall AI 
class ai():
    def __init__(self, job_description:str, function = None):
        
        self.instruction = f'You are the behavioral part of the interviewer process. You are responsible for replciating normal and mannerful human interaction as a interviewer. This interview is specifically related to a CS major job. This is the description of the job:\n{job_description}'
        self.chat_history = [
            {'role': 'system', 'content': self.instruction}
        ] 
        self.function = function 
        
        
    def send_message_general_ai(self, message):
        # WIP 
        print(f'sending message to general ai: \'{message}\' | send_message_general_ai\n') # Log
        
        send_message(message, self.chat_history)
        
        response = process_response_no_streaming(self.chat_history)
        
        return response
        
# AI responsible for the coding section 
class coding_ai(ai):
    def __init__(self, job_description:str, coding_lang:str):
                        
        self.instruction = (
        "Generate Software Engineering coding questions at a difficulty level between LeetCode Medium and Hard. "
        "Format responses using HTML elements such as <b>, <i>, or <p> to enhance readability and presentation. "
        "Ensure the output is suitable for direct assignment to the .innerHTML property of an HTML element. "
        "Align the content and style with LeetCode's structured and professional format, and tailor each question to fit the provided job description if applicable. "
        "dont include ```html ``` any where "
        "use <br> for breaking lines "
        f"Coding language to use is {coding_lang}"
        f'\nDescription of the job is: {job_description}'
        )
        
        self.chat_history = [
            {'role': 'system', 'content': self.instruction}
        ] 
    
    # asks a new question 
    def start(self):
        
        print(f'Creating new coding question | start\n')
        
        send_message(f'please ask one coding question that you havent asked before above', self.chat_history)
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_history,
            stream=True # Enable streaming for smaller chunks
        )
        
        return completion # returns answers in iterators 
    
    def record_ai_response(self, response): 
        print(f'logging ai_response: {response} | record_ai_response\n')# Log
        
        self.chat_history.append({'role':'assistant', 'content': response})
            

# Formatting the questions 
class formatter_question(ai):
    def __init__(self, question):
        self.question = question
        self.instruction = 'Create the starting function for this question, ONLY the starting function as in creating the necessary class for it and only give the function name and its parameters. Break in line as in starting a new line for the code should be indicated by \'\\n\' LTIERALLY as in \\n right after the line ends followed spaces for proper indentions(4 spaces per level, for example 4 spaces for codes inside a function and 8 spaces inside the codes inside the function if the code has nested loop) instead of tabs. No python no ``` necessary.'

    
    def create_bonework(self):
        
        print(f'creating bonework for new program question:\n{self.question} | create_bonework\n') #Log 
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.instruction},
                {
                    'role': 'assistant',
                    'content': f'The question is the following\n\n{self.question}'
                }
            ],
            stream=True # Enable streaming for smaller chunks
        )
        return completion # returns answers in iterators 


class advisor_ai(ai):
    # Add instrucitons for advisor AI 
    def __init__(self):
        self.instruction = 'You are responsible to give advise to the user on their code for a coding question. Do not explicitly give the answer to them. Think of this as a coding interview and the person is asking you (the interviewer) for a little help on where to begin etc and how to proceed. The structure of the code such as the beginning has been given to the user and not user created. Talk like you will be talking to the person directly using voice'
        
        self.chat_history = [
            {'role': 'system', 'content': self.instruction}
        ] 
        
    def set_coding_question(self, coding_question:str):
        print(f'setting coding question:\n{coding_question} | set_coding_question\n') # Log
        self.coding_question = coding_question
        
    def set_user_code(self, user_code:str):
        print(f'setting user_code:\n{user_code} | set_user_code\n') # Log
        self.user_code = user_code 
        
    def formulate_answer(self, user_question: str):
        # WIP
        print(f'formulating answers for user\nuser question: {user_question} | formulate_answer\n')
        
        self.chat_history.append({'role':'user', 'content': user_question})
        self.chat_history.append({'role':'assistant', 'content': f'This is the coding question: \n {self.coding_question} \n\n This is what user has for his code right now: \n {self.user_code}'})
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_history
        )
        ai_message = completion.choices[0].message
        
        print(f'ai response: \'{ai_message}\'\n')
        
        log_ai_response(ai_message, self.chat_history) # Log
        
        return ai_message
        
    
    def get_chat_history(self):
        return self.chat_history 