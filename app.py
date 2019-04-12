from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube import API
from apiclient.discovery import build 
from dotenv import load_dotenv
import os
import requests

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
	rV.headers['Access-Control-Allow-Origin'] = '*'
	return jsonify(rV)


@app.route('/api/v1/search', methods=['GET'])
def search():
	query = request.args.get('search')
	#query = "academy"

	title = []
	youtube = build(API_SERVICE_NAME, API_VERSION,developerKey=API_KEY)

	req = youtube.search().list(q = query, type = "video", part = "snippet", maxResults=40)


	response = req.execute()
	videos = []
	items = response.get("items")
	for i in items:
		idval = i["id"]["videoId"]
		ml_result = ml_helper(idval, query)
		print(ml_result)
		if not ml_result.get("error"):
			i["topics"] = ml_result
			videos.append(i)
			

	return jsonify(videos)

@app.route('/api/v1/ml', methods=['GET'])
def getmldata():
	line = "https://modeler.studyfast.xyz"
	
	temp = requests.get(line).json()

	return temp

def ml_helper(vidid, search):
	base_url = "https://ml-service.studyfast.xyz/video/"
	request_url = base_url + vidid
	payload = {'search':search}
	response = requests.get(request_url, params=payload)
	return response.json()



if __name__ == '__main__':
    app.run(debug=True, port=65010, host="0.0.0.0")


