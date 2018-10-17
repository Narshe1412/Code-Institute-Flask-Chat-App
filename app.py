import os
from datetime import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
messages = []

def add_messages(username, message):
    """ Add messages to the message list """
    now = datetime.now().strftime("%H:%M:%S")
    message_dict = {"timestamp": now, "from": username, "message": message}
    messages.append(message_dict)
    

def get_all_messages():
    """Get all of messages in the system and separate them by a BR tag"""
    return messages
    

@app.route('/', methods=["GET", "POST"])
def index():
    """ Main page with instructions """
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")
    
    
@app.route('/<username>')
def user(username):
    """Display chat messages"""
    message = get_all_messages()
    return render_template("chat.html", username=username, chat_messages = message)
    
    
@app.route('/<username>/<message>')
def send_message(username, message):
    """Create a new message and redirect back to the chat page """
    add_messages(username, message)
    return redirect(username)
    
    
app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)