from flask import Flask, request, Response, jsonify
from store import SampleStore
from analyzers import VirusTotalAnalyzer, BasicAnalyzer
from model import Sample, SampleStatus
from datetime import datetime
from bson import json_util
import json
import jsonpickle
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import threading
import argparse

def load_configuration(json_path):
    with open(json_path, 'r') as config_file:
        data = config_file.read()
    
    return json.loads(data)


parser = argparse.ArgumentParser()
parser.add_argument('--config', action='store', \
                    help='JSON config file', \
                    required=True)

params = parser.parse_args()
configuration = load_configuration(params.config)
# Initializing the analyzers and the sample store.
app = Flask(__name__)
CORS(app)

store_name = configuration['sample_store_name']

sample_store = SampleStore()
sample_store.initialize(store_name, configuration)

analyzers = []

vt_analyzer = VirusTotalAnalyzer()
basic_analyzer = BasicAnalyzer()

vt_analyzer.initialize(store_name, configuration)
basic_analyzer.initialize(store_name, configuration)

analyzers.append(vt_analyzer)
analyzers.append(basic_analyzer)

def analysis_thread(sample, analyzers, sample_store):
    """
    > For each analyzer, analyze the sample and add the resulting 
    representations to the sample
    
    :param sample: The sample to analyze
    :param analyzers: A list of analyzers to run on the sample
    :param sample_store: The sample store to use for storing the sample
    """
    
    for analyzer in analyzers:
        representations = analyzer.analyze(sample)
        sample.representations.extend(representations)
        
    if len(sample.representations) > 0:
        
        sample.analysis_date = datetime.now()
        
        sample.sample_status = SampleStatus.INDEXED
        
        new_sample = sample_store.update(sample)
    else:
        sample_store.remove(sample.id)


"""
It takes a URL from a POST request, creates a new sample object, 
stores it in the database, and starts a thread to analyze the sample.
"""
@cross_origin()
@app.route('/samples', methods=['POST'])
    
def create_sample():
    
    url = request.json['url']
    
    url_sample = sample_store.find_by_url(url)
    #print(str(url_sample))
    if url_sample is None:
    
        sample = Sample(url)
        new_sample = sample_store.store(sample)
        
        thread = threading.Thread(target=analysis_thread, args=(new_sample, analyzers, sample_store))
        thread.start()
        
        #new_sample.identifier = str(new_sample.id)
        response = jsonpickle.encode(new_sample, unpicklable = False)
        #response = jsonify(new_sample)
        return Response(response, mimetype='application/json')
    
    else:
        response = jsonpickle.encode(url_sample, unpicklable = False)
        #response = jsonify(new_sample)
        return Response(response, mimetype='application/json')
        
"""
It takes a sample ID, retrieves the sample from the sample store, 
and returns it as a JSON response.

:param id: The id of the sample to retrieve
:return: A JSON object containing the sample with the given ID.
"""
@cross_origin()
@app.route('/samples/<id>', methods=['GET'])
    
def get_sample(id):
    sample = sample_store.retrieve(id)
    
    response = jsonpickle.encode(sample, unpicklable = False)
    
    return Response(response, mimetype='application/json')

"""
    It takes a sample id, retrieves the sample from the store, 
    searches for similar samples, and returns the results as a JSON response
    
    :param id: The id of the sample to search for similar samples
    :return: A list of similar samples.
"""
@cross_origin()
@app.route('/similares/<id>', methods=['GET'])
    
def get_similares(id):
    
    sample = sample_store.retrieve(id)
    
    similar_samples = sample_store.search_similar(sample)
    #print(similar_samples)
    #response = jsonpickle.encode(similar_samples, unpicklable = False)
    
    response = jsonpickle.encode(similar_samples, unpicklable = False)
    
    return Response(response, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
    