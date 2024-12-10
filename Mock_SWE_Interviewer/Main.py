from flask import Flask, render_template, jsonify, Response
import webview 
import threading
import openAI_file 
import time 

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

# Global flag to track if the question has been generated
question_generated = False

# Sends the coding question to html
@flask_app.route('/question')
def send_question():
    global question_generated

    def generate():
        sentences = [
            "This is the first line.<br>This is the second line.",
            "<div>Hello, World!</div>",
            "Click <a href='https://example.com'>here</a> to visit our site.",
            "<h1>Welcome to My Website</h1>",
            "Line one.<br>Line two.<br>Line three.",
            "An image: <img src='/static/resource/Test_img/image.png' alt='An example image'>",
            "<p>This is a paragraph.</p>",
            "<ul><li>Item 1</li><li>Item 2</li></ul>",
            "Newline example: First line.<br>Second line.<br>Third line.",
            "This is bold text: <strong>bold</strong> and italic text: <em>italic</em>."
        ]
        # For testing purposes use this 
        for chunk in sentences: 
            yield f'data: {chunk}\n\n'
            time.sleep(.05)
        
        '''
        for chunk in coding_ai.start():
            print(chunk.choices[0].delta.content, flush=True)
            yield f'data: {chunk.choices[0].delta.content}\n\n'
            time.sleep(0.025)  # Simulating delay between messages
        '''

    if not question_generated:
        question_generated = True
        return Response(generate(), mimetype='text/event-stream')
    
    return jsonify({'data': 'True'})



'''
WebView Process
'''
def create_webview():
    webview.create_window('Main', "http://127.0.0.1:5000/", fullscreen=True)
    webview.start()

if __name__ == "__main__":
    ''' Testing purposes do not activate
    # initializes coding ai for the job that the user is preparing for
    description = input('description of the job?: ')    
    coding_ai = openAI_file.coding_ai(description)
    '''
    
    # Threading for Flask 
    flask_thread = threading.Thread(target=flask_start)
    flask_thread.start() 
    
    # Creates webview for easier access
    create_webview()
    
    # Starts with a question
    send_question()