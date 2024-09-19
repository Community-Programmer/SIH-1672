from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

output_file = 'mouse_movement_data.txt'

@app.route('/post-records', methods=['POST'])
def post_records():
    data = request.json
    
    if not data or not all(key in data for key in ['times', 'xPositions', 'yPositions']):
        return jsonify({'error': 'Invalid data format'}), 400
    
    try:
        with open(output_file, mode='a') as file:
            for i in range(len(data['times'])):
                file.write(f"{data['times'][i]},{data['xPositions'][i]},{data['yPositions'][i]}\n")
        
        return jsonify({'message': 'Data successfully written to text file'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
