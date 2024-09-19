import time
import pyautogui
import requests
import random

# Configuration
backend_url = 'http://127.0.0.1:5000/post-records'  # Change to your backend URL if needed
records_buffer_size = 2500
time_limit = 10  # in seconds

# Data collection
records = {
    'times': [],
    'xPositions': [],
    'yPositions': []
}

# Start collecting data
start_time = time.time()

try:
    while True:
        # Get current mouse position
        x, y = pyautogui.position()
        elapsed_time = time.time() - start_time

        # Collect data
        records['times'].append(elapsed_time)
        records['xPositions'].append(x)
        records['yPositions'].append(y)

        # Print current position
        print(f"Time: {elapsed_time:.2f}s, X: {x}, Y: {y}")

        # Check if we reached the buffer size or the time limit
        if len(records['times']) >= records_buffer_size or elapsed_time >= time_limit:
            # Send data to the backend
            response = requests.post(backend_url, json=records)
            print(response.json())  # Print the server response
            
            # Reset records
            records = {
                'times': [],
                'xPositions': [],
                'yPositions': []
            }
            start_time = time.time()  # Reset timer after sending

        # Simulate mouse movement
        new_x = random.randint(100, 800)  # Random X position
        new_y = random.randint(100, 600)  # Random Y position
        pyautogui.moveTo(new_x, new_y, duration=0.1)  # Move to new position

        # Sleep for a short time before collecting the next position

except KeyboardInterrupt:
    print("Data collection stopped.")
