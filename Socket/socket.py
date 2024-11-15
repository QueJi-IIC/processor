import socketio
import time
from QueJI_Feature.play import runner
import QueJI_Feature.cvo as cvo

# Socket.IO Client Initialized
sio = socketio.Client()

# Event for Connection
@sio.event
def connect():
    print("Connected to the server!")

# Event for DisConnection
@sio.event
def disconnect():
    print("Disconnected from server")

# Event for Connection Errors
@sio.event
def connect_error(data):
    print("Connection failed:", data)

def yolo_task():
    inittime = time.time()
    cvo.start_Cam()
    while True:
        try:
            # Get the current YOLOv9 output (True, False, or None)
            detection_status = runner()
            print(f"Detection status: {detection_status}")

            # Check if the model returned None (indicating it stopped or is inactive)
            if time.time() - inittime > 2:
                if detection_status is None:
                    print("YOLO model inactive or stopped")
                    sio.emit('detection_status', {'detected': 'inactive'})
                else:
                    # Emit the detection status to the server
                    sio.emit('detection_status', {'detected': detection_status, 'fire': False, 'weapon': False, })
                inittime = time.time()

        except Exception as e:
            # Handle unexpected errors gracefully
            print("Error in YOLO detection:", e)
            # Optionally, emit an error status to the server
            sio.emit('detection_status', {'detected': 'error'})

# Define headers
headers = {
    'client-id': 'a9f1c553-b377-4801-9e15-326d62f378ce',
    'client-secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJhOWYxYzU1My1iMzc3LTQ4MDEtOWUxNS0zMjZkNjJmMzc4Y2UiLCJpYXQiOjE3MzE2OTk5MTUsImV4cCI6MTczNDMyNzkxNX0.hs2_DNQ7YobwTUg5Qktn6_D2s8eio-ZAEsWMA0lYlsY',
    'platform': 'hardware',
}

# Connecting Socket.IO server with headers
sio.connect('http://localhost:5500', headers=headers)  # Replace with your server address

# Start the YOLO background task
sio.start_background_task(yolo_task)

# Keep the client running to listen for events and keep emitting data
sio.wait()