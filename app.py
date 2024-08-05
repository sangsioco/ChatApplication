from web_socket_server import WebSocketServer, socketio, app
from flask import render_template
from flask_socketio import join_room, leave_room, send, emit

app = WebSocketServer().create_app()
message_storage = {}

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'Anonymous')
    message = data.get('message')
    if message:
        emit('message', {'username': username, 'message': message}, broadcast=True)

@socketio.on('get_user_message')
def handle_get_user_messages(data):
    username = data.get('username')
    
    if not username:
        return  # Ignore if username is not provided

    messages = message_storage.get(username, [])
    socketio.emit('get_user_message', {'username': username, 'messages': messages})

@socketio.on('get_all_messages')
def handle_get_all_messages(data):
    username = data.get('username')
    
    if not username:
        return  # Ignore if username is not provided

    messages = message_storage.get(username, [])
    socketio.emit('get_all_messages', {'username': username, 'messages': messages})

@socketio.on('join')
def on_join(data):
    username = data.get('username')
    room = data.get('room')
    if username and room:
        join_room(room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f'{username} has left the room.', room=room)

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