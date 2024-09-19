from flask import Flask, request, jsonify
import csv
import os
from flask_cors import CORS  # Import CORS


app = Flask(__name__)
CORS(app)  

output_file = 'mouse_movement_data.csv'

@app.route('/post-records', methods=['POST'])
def post_records():
    data = request.json
    

    if not data or not all(key in data for key in ['times', 'xPositions', 'yPositions']):
        return jsonify({'error': 'Invalid data format'}), 400
    
    try:
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
       
            if os.stat(output_file).st_size == 0:
                writer.writerow(['Time (s)', 'X Position', 'Y Position'])

            # Write the data
            for i in range(len(data['times'])):
                writer.writerow([data['times'][i], data['xPositions'][i], data['yPositions'][i]])
        
        return jsonify({'message': 'Data successfully written to CSV'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
