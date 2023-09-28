import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import cvProcess as cvp

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Route for processing cv
@app.route('/process-cv', methods=['POST'])
def process_cv_route():
    print("cv process works!")

    try:
        cv_file = request.files["cv"]
        if cv_file and cv_file.filename.endswith('.pdf'):
            cv_file.save(os.path.join(app.root_path, 'static/' + cv_file.filename))
            result = cvp.process_cv(cv_file)
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Invalid CV file format'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# Route for getting recommendations
@app.route('/get-recommendations', methods=['POST'])
def get_recommendations_route():

    try:
        cvText = request.data  # Use request.json to access JSON data

        print(cvText)

        recommendations = cvp.generate_recommendations()  # Call the generate_recommendations function

        if recommendations['best_language'] is None:
            return jsonify({'message': 'No programming languages detected'}), 300

        return jsonify(recommendations), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
