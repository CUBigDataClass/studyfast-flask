from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
	rV = {"home": "test"}
	return jsonify(rV)


@app.route('/api/v1/search', methods=['GET'])
def search():
	retVal = {"hello": "world"}
	return jsonify(retVal)


if __name__ == '__main__':
    app.run(debug=True, port=65010)


