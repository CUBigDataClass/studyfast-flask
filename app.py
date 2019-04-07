from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube import API
from apiclient.discovery import build 
from dotenv import load_dotenv
import os


app = Flask(__name__)
api = Api(app)

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SEC = os.getenv("CLIENT_SEC")
API_SERVICE_NAME = os.getenv("API_SERVICE_NAME")
API_VERSION = os.getenv("API_VERSION")
API_KEY = os.getenv("API_KEY")


@app.route('/', methods=['GET'])
def home():
	rV = {"home": "test"}
	return jsonify(rV)


@app.route('/api/v1/search', methods=['GET'])
def search():

	title = []
	youtube = build(API_SERVICE_NAME, API_VERSION,developerKey=API_KEY)

	request = youtube.search().list(q = "hello", type = "video", part = "id, snippet")


	response = request.execute()

	return jsonify(response)


	# r = api.get('search', q="hello")
	# return jsonify(r)
	# resp = youtube.search().list(q="hello")
	# return jsonify(resp)


if __name__ == '__main__':
    app.run(debug=True, port=65010)


