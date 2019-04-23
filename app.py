from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube import API
from apiclient.discovery import build 
from dotenv import load_dotenv
import os
import requests
import asyncio
from requests_futures.sessions import FuturesSession

app = Flask(__name__)
api = Api(app)

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv('.env')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SEC = os.getenv("CLIENT_SEC")
API_SERVICE_NAME = os.getenv("API_SERVICE_NAME")
API_VERSION = os.getenv("API_VERSION")
API_KEY = os.getenv("API_KEY")
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@app.route('/ping', methods=['GET'])
def home():
    rV = {"pong": True}
    resp = jsonify(rV)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    #return jsonify(rV)
    return resp


@app.route('/api/v1/video/<video_id>', methods=['GET'])
def get_video(video_id):
    query = request.args.get('search')
    # Get the ml result
    ml_url = 'https://ml-service.studyfast.xyz/video/' + video_id
    ml_response = requests.get(ml_url, params={'search': query}).json()
    # Get video details from youtube
    req = youtube.videos().list(id=video_id, part='snippet')
    response = req.execute()
    response['topics'] = ml_response
    return jsonify(response)


@app.route('/api/v1/list', methods=['GET'])
def search():
    query = request.args.get('search')

    title = []

    req = youtube.search().list(q = query, type = "video", part = "snippet", maxResults=40)
    response = req.execute()

    # Get all of the results in parallel
    items = response.get("items")
    payload = {'search':search}
    req_urls = ['https://ml-service.studyfast.xyz/valid_transcript/' + i["id"]["videoId"] for i in items]
    session = FuturesSession()
    network_calls = [session.get(u, params=payload) for u in req_urls]
    raw_results = [req.result() for req in network_calls]
    results = [r.json() for r in raw_results]

    # Get the final list of videos
    videos = []
    for i in range(0, len(items)):
        item = items[i]
        has_transcript = results[i]['transcript']
        if has_transcript:
            item = clean_youtube_search_result(item)
            videos.append(item)
            

    resp = jsonify(videos)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def clean_youtube_search_result(result):
    result.pop('etag')
    result.pop('kind')
    result.get('snippet').pop('channelId')
    result.get('snippet').pop('publishedAt')
    result.get('snippet').pop('liveBroadcastContent')
    return result


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")


