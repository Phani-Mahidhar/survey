from flask import Flask, request, jsonify
from pymongo import MongoClient

from gpt_driver import generate_gpt_response

app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["surveys"]
surveys_collection = db["questions"]


@app.route('/survey/generate', methods=['POST'])
def generate_survey():
    prompt = request.json['prompt']
    response = generate_gpt_response(prompt)
    survey = {'questions': response}
    return jsonify({'survey': survey})


@app.route('/survey/add', methods=['POST'])
def add_survey():
    survey = request.json['survey']
    result = surveys_collection.insert_one(survey)
    survey_id = result.inserted_id
    return jsonify({'survey_id': survey_id})


@app.route('/survey/<survey_id>', methods=['GET'])
def get_survey(survey_id):
    survey = surveys_collection.find_one({'_id': survey_id})
    return jsonify({'survey': survey['survey']})


@app.route('/survey/<survey_id>', methods=['PUT'])
def update_survey(survey_id):
    survey = request.json['survey']
    result = surveys_collection.update_one({'_id': survey_id}, {'$set': {'survey': survey}})
    if result.modified_count > 0:
        return jsonify({'message': 'Survey questionnaire updated successfully'})
    else:
        return jsonify({'message': 'Error updating survey questionnaire'})


@app.route('/survey', methods=['GET'])
def get_all_surveys():
    surveys = surveys_collection.find({})
    return jsonify({'surveys': surveys})


if __name__ == '__main__':
    app.run()
