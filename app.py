from web_socket_server import WebSocketServer, socketio, app
from flask import render_template

app = WebSocketServer().create_app()
message_storage = {}

@socketio.on('message')
def handle_message(data):
    author = data.get('user')
    message = data.get('message')
    
    if not author or not message:
        return  # Ignore if author or message is not provided

    print(f'Received message from {author}: {message}')

    if author not in message_storage:
        message_storage[author] = []
    
    message_storage[author].append(message)
    
    # Emit the new message to all connected clients
    socketio.emit('message', {'author': author, 'message': message})


@socketio.on('get_user_message')
def handle_get_user_messages(data):
    author = data.get('author')
    
    if not author:
        return  # Ignore if author is not provided

    messages = message_storage.get(author, [])
    socketio.emit('get_user_message', {'author': author, 'messages': messages})

@socketio.on('get_all_messages')
def handle_get_all_messages(data):
    author = data.get('user')
    
    if not author:
        return  # Ignore if author is not provided

    messages = message_storage.get(author, [])
    socketio.emit('get_all_messages', {'author': author, 'messages': messages})


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    
@app.route('/')
def index():
    return render_template('WebSocketClient.html')

if __name__ == '__main__':
    socketio.run(app)
