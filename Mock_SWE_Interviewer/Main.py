from flask import Flask, render_template, Response, request, jsonify
import webview 
import threading
import openAI_file 
import time 
import requests
import voice

# Setting functioncall params
tools = [
  {
      "type": "function",
      "function": {
          "name": "process_advising_ai",
          'description': 'call this whenever the user is asking for advise or help',
          "parameters": {
              "type": "object",
              'properties': {}
          },
      },
  }
]


'''
Flask Process
'''
flask_app = Flask(__name__)

# Starts Flask 
def flask_start():
    flask_app.run(debug=True, use_reloader=False)
    
# First page that renders when flask starts
@flask_app.route('/')
def home():
    return render_template('coding_page.html')

# Sends the coding question to html
@flask_app.route('/question')
def send_question():
    global full_question
    print('creating coding questions | send_question\n') #Logging
    full_question = ''
    def generate():
        global full_question
        sentences = [
            "Given an array of integers nums and an integer target,",
            "return indices of the two numbers such that they add up to target.",
            "You may assume that each input would have exactly one solution,",
            "and you may not use the same element twice.",
            "You can return the answer in any order.",
            "Example:",
            "Input: nums = [2, 7, 11, 15], target = 9",
            "Output: [0, 1]",
            "Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
            "Constraints:",
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ]
        
        # For testing purposes use this 
        for chunk in sentences: 
            full_question += chunk
            yield f'data: {chunk}\n\n'
            time.sleep(.05)
            
        '''
        # Streams each chunk of the data to html
        for chunk in coding_ais.start():
            processed_chunk = chunk.choices[0].delta.content
            if processed_chunk is not None:
                full_question += processed_chunk
                yield f'data: {processed_chunk}\n\n'
                time.sleep(0.005)  # Simulating delay between messages
        '''
        
        # Records the full question into ai so when a new one is asked, it wont ask a similar
        coding_ais.record_ai_response(full_question)
        print(f'Question Response:\n{full_question}\n')# Log
        yield "event: end\ndata: Stream complete\n\n"

        
    return Response(generate(), mimetype='text/event-stream')

# starts the formatter question
@flask_app.route('/format') 
def format():
    global full_question

    format_ai = openAI_file.formatter_question(full_question)
    
    def generate():
        total_format = ''
        for chunk in format_ai.create_bonework(): 
            processed_chunk = chunk.choices[0].delta.content
            if processed_chunk is not None:
                total_format += processed_chunk
                yield f'data: {processed_chunk}\n\n'
                time.sleep(0.005)  # Simulating delay between messages
                
        print(f'Formatting response:\n\n{total_format}\n\n')# Log
        
        yield "event: end\ndata: Stream complete\n\n" 
    
    return Response(generate(), mimetype='text/event-stream')

# Gets the voice transcript data from html 
@flask_app.route('/speech_data', methods=['POST'])
def receive_speech_data():
    global last_user_message
    
    speech = request.json
    last_user_message = speech
    
    print(f'Received speech data: {speech} | receive_speech_data\n') # Log
    

    # Process speech to general AI to know what function to be called
    response = general_ai.send_message_general_ai(speech)    
    
    # Check if ai called any function or just a normal message
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0].function.name
        print(f'Running function: {response} | receive_speech_data\n')# Log 
        eval(response + '()')
        print(f'tool call was called by ai: {tool_call} | send_message_general_ai\n')# Log 
    else:
        print(f'No tool call response was called by ai: {response.choices[0].message.content} | send_message_general_ai\n')
        voice.create_audio(response.choices[0].message.content)
    
    return jsonify({'status':'received'}) 

# Create endpoint to getting the user code 
@flask_app.route('/get_user_code', methods = ['POST'])
def get_user_code(): 
    global user_code 
    
    print('get_user_code\n\n')# Log 
    
    user_code = request.json
    
    print(f'{user_code}\n')# Log
    
    return jsonify({'user_code': 'receieved'})

# Process for advisor AI 
def process_advising_ai():
    
    print(f'advising ai processing for user code:\n{user_code}\nprocessing_advising_ai\n')# Log
    
    # set_user_code, set_coding_questoin for setting ai setting
    advising_ais.set_coding_question(full_question)
    advising_ais.set_user_code(user_code)
    
    # def formulate_answer
    response = advising_ais.formulate_answer(last_user_message)
    
    # Proccess response first to only get the message
    'voice.create_audio(response)'
    

# Creates the webview and starts it
def create_webview():
    webview.create_window('Main', "http://127.0.0.1:5000/", fullscreen=True)
    webview.start()


if __name__ == "__main__":
    
    # initializes coding ai for the job that the user is preparing for
    description = input('description of the job?: ')   
    preferred_lang = input('preferred coding lang?: ') 
    coding_ais = openAI_file.coding_ai(preferred_lang, description)
    advising_ais = openAI_file.advisor_ai() 
    general_ai = openAI_file.ai(description) #implement all possible functions that the ai has
    
    # Threading for Flask 
    flask_thread = threading.Thread(target=flask_start)
    flask_thread.start()
    
    # Creates webview for easier access
    create_webview()
    # No other code will run below this as create_webview will keep running however any server ran function will still be ran
    
    
    
    

    