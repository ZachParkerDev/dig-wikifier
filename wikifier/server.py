from flask import Flask
from flask import request
from flask_cors import CORS
import json
import requests
from optparse import OptionParser
import codecs
from requests.auth import HTTPBasicAuth
from extractor import AnchorTextExtractor
from graph_builder import GraphBuilder
from similarity.verse_similarity import VerseSimilarity
from flask import jsonify

app = Flask(__name__)
# Load configs from file. File path must be set using command `export APP_SETTINGS=path/to/config.cfg
app.config.from_envvar('APP_SETTINGS')
CORS(app)

config = {}
redis_host = app.config.get('REDIS_HOST')
redis_port = app.config.get('REDIS_PORT')

anchor_text_extractor = AnchorTextExtractor()
verse_similarity = VerseSimilarity(app.config.get('VERSE_EMBEDDINGS'), app.config.get('VERSE_NODEMAP'))
graph_builder = GraphBuilder(redis_host, redis_port, verse_similarity)

print("Initialization complete")
@app.route('/')
def home():
    return 'Wikifier implementation'

@app.route('/annotate', methods=['POST'])
def create_bipartite_graph():
    request_data = json.loads(request.data)
    tokens = anchor_text_extractor.extract_tokens(request_data["text"])
    gp = graph_builder.process(tokens=tokens)
    response = app.response_class(
        response = json.dumps(gp),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_nx_graph', methods=['POST'])
def create_and_return_bipartite_graph():
    request_data = json.loads(request.data)
    tokens = anchor_text_extractor.extract_tokens(request_data["text"])
    gp = graph_builder.process_nx_graph(tokens=tokens)

    response = app.response_class(
        response = json.dumps(gp),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_properties', methods=['POST'])
def get_properties():
    request_data = json.loads(request.data)
    data = graph_builder.get_qnode_properties(request_data)
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_similarity_score', methods=['POST'])
def get_similarity_score():
    request_data = json.loads(request.data)
    data = graph_builder.get_similarity(request_data)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_statements', methods=['POST'])
def get_statements():
    request_data = json.loads(request.data)
    data = graph_builder.get_statements(request_data)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/get_identifiers', methods=['POST'])
def get_identifiers():
    request_data = json.loads(request.data)
    data = graph_builder.get_identifiers(request_data)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response