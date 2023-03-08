from model import Sample
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import jsonpickle
import json 
from bson import ObjectId
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis

#MongoDBStore
class MongoDBStore:
    
    def initialize(self, name: str, configuration: dict):
        """
        It creates a connection to a MongoDB database, and creates a collection in that database
        
        :param name: The name of the collection
        :type name: str
        :param configuration: dict
        :type configuration: dict
        """
        
        #MONGODB
        self.name = name

        MONGO_URI = configuration['mongo_uri'] # donde está alojado

        self.client = MongoClient(MONGO_URI) # client es la conexion con la bbdd

        self.db = self.client[configuration['mongo_db_name']] # base de datos

        self.collection = self.db[name] # crea una collection
        
        
        
    # cierra la conexion con la bbdd
    def close(self):
        self.client.close()
    
    # guarda un sample
    def store(self, sample: Sample) -> Sample:
        """
        > The function takes a sample object, converts it to JSON, 
        inserts it into the database, and then returns the sample 
        object with the id of the inserted document
        
        :param sample: Sample - the sample to store
        :type sample: Sample
        """
        
        sample_json = json.loads(jsonpickle.encode(sample))
      
        
        result = self.collection.insert_one(sample_json)

        sample = self.retrieve(result.inserted_id)
       
        sample.id = str(result.inserted_id)
        
        
        return sample
    
    # recupera un sample
    def retrieve(self, id: str) -> Sample:
        """
        > The function takes in a string, converts it to an ObjectId, 
        finds the document in the database, unpickles it, and returns the sample
        
        :param id: str
        :type id: str
        :return: A Sample object
        """
        
        if type(id) == str:
            id = ObjectId(id)
            
        sample_dict = self.collection.find_one({"_id": id})
        
        u = jsonpickle.unpickler.Unpickler()
        sample = u.restore(sample_dict)
        
        return sample
    
    def update(self, sample:Sample) -> Sample:
        """
        It takes a sample object, converts it to a json object, then 
        replaces the document in the database with the new json object
        
        :param sample: Sample
        :type sample: Sample
        :return: The sample object is being returned.
        """
        
        original_id = sample._id
        
        
        sample_json = json.loads(jsonpickle.encode(sample))
        #sample_json["id"] = original_id

        sample_json["_id"] = original_id
       
        result = self.collection.replace_one({"_id":original_id},
                                             sample_json)

        sample = self.retrieve(sample.id)
        #sample.id = original_id
        sample._id = original_id
        
        return sample
        
    # elimina un sample
    def remove(self, id: str):
        
        self.collection.delete_one({"_id": id})
      
    """
        It takes a URL as a parameter, searches the database 
        for a sample with that URL, and returns the sample if it exists
        
        :param url: The URL of the sample
        :type url: str
        :return: A sample object
    """  
    def find_by_url(self, url: str) -> Sample:
        
        result = self.collection.find_one({"url":url})
        
        if result is not None:
            u = jsonpickle.unpickler.Unpickler()
            sample = u.restore(result)
            
            return sample
        else:
            return None
        

#ElasticSearcher
class ElasticSearcher:
    
    def initialize(self, name: str, configuration: dict):
        """
        This function initializes the Elasticsearch object with the configuration parameters passed in
        from the configuration file.
        
        :param name: The name of the plugin
        :type name: str
        :param configuration: dict
        :type configuration: dict
        """
        
        self.name = name

        # ELASTICSEARCH
        self.es = Elasticsearch(configuration['elastic_uri'],
                        ca_certs=configuration['elastic_cert'],
                        http_auth=(configuration['elastic_user'], 
                        configuration['elastic_password']))
    
    def close(self):
        self.es.close()
        
    
    def store(self, sample: Sample) -> Sample:
        """
        It takes a sample, creates a document with the sample's url 
        and the indexable items of its representations, and stores the 
        document in Elasticsearch
        
        :param sample: The sample to be stored
        :type sample: Sample
        :return: The sample
        """
        # nuevo doc que recorre las representations que tenga el metodo indexable fields
        doc = {
            "url": sample.url
        }
        for r in sample.representations:
            for indexable_item in r.get_indexable_items():
                
                doc[indexable_item.name] = ' '.join(indexable_item.values) # crea un doc con ese contenido separado con espacios
                
        
        sample_id = sample.id
        
        self.es.index(index=self.name, id=sample_id, document=doc)
        
        return sample
    
    def remove(self, id: str):
        
        es.delete(index=self.name, id=id)
    
    def update(self, sample:Sample) -> Sample:
        """
        It creates a document with the url and the indexable items of the sample, and then updates the
        document in the index
        
        :param sample: The sample to be indexed
        :type sample: Sample
        :return: The sample object
        """
        # nuevo doc que recorre las representations que tenga el metodo indexable fields
        doc = {
            "url": sample.url
        }
        for r in sample.representations:
            for indexable_item in r.get_indexable_items():
                
                doc[indexable_item.name] = ' '.join(indexable_item.values) # crea un doc con ese contenido separado con espacios
                
        sample_id = sample.id
        
        self.es.update(index=self.name, id=sample_id, doc=doc)
        
        return sample
    
    def search_similar(self, sample: Sample) -> list:
        
        dsl_search = Search(index=self.name).using(self.es)
        
        doc = {
            "url": sample.url
        }
        
        fields = []
        for r in sample.representations:
            for indexable_item in r.get_indexable_items():
             
                fields.append(indexable_item.name)
                #doc[indexable_item.name] = ' '.join(indexable_item.values)

        '''for k, v in doc.items():
            if k != 'basic-content':
                print(k,v,'\n')'''
         
        '''content_dsl = dsl_search.query(MoreLikeThis(fields=["basic-content",
                                                            "basic-geo_loc",
                                                            "basic-https",
                                                            "unrated_engines",
                                                            "positive_engines",
                                                            "negative_engines",
                                                            "basic-label",
                                                            "categories",
                                                            "basic-whois",
                                                            "basic-ip",
                                                            "basic-tld"], 
                                                    like=[doc['basic-content'],
                                                          doc['basic-geo_loc'],
                                                          doc['basic-https'],
                                                          doc['unrated_engines'],
                                                          doc['positive_engines'],
                                                          doc['negative_engines'],
                                                          doc['basic-label'],
                                                          doc['categories'],
                                                          doc['basic-whois'],
                                                          doc['basic-ip'],
                                                          doc['basic-tld']]))'''
        
                                                    
        content_dsl = dsl_search.query(MoreLikeThis(fields=fields,
                                                    like=[{"_index":self.name,
                                                           "_id": sample.id}]))
        response = content_dsl.execute()
        
        result = []
        max_score = response.hits.max_score
        
        for hit in response:
            
            result.append({"id":hit.meta.id,"score":hit.meta.score/max_score,"url":hit.url})
            #print(hit)
        
        #print(str(result))
        return result
        
        
#SampleStore
class SampleStore:
    
    def __init__(self):
        """
        The function __init__() initializes the class 
        by creating two objects, one for storing and one for searching
        """
        self.storer = MongoDBStore()
        self.searcher = ElasticSearcher()
        
    def initialize(self, name: str, configuration: dict):
        """
        The function initializes the name and configuration of the storer and searcher
        
        :param name: The name of the index
        :type name: str
        :param configuration: A dictionary containing the configuration of the index
        :type configuration: dict
        """
        
        self.name = name
        self.storer.initialize(name, configuration)
        self.searcher.initialize(name, configuration)
        
    def close(self):
        """
        It closes the storer and searcher.
        """
        self.storer.close()
        self.searcher.close()
        
    def store(self, sample: Sample) -> Sample:
        """
        > Store a sample in the database and index it for searching
        
        :param sample: The sample to store
        :type sample: Sample
        :return: The new sample that was stored.
        """
        new_sample = self.storer.store(sample)
        self.searcher.store(new_sample)
        
        return new_sample
    
    
    def remove(self, id: str):
        """
        > Remove the document with the given id from the index
        
        :param id: the id of the document to remove
        :type id: str
        """
        self.storer.remove(id)
        self.searcher.remove(id)
        
    def retrieve(self, id: str) -> Sample:
        """
        > Retrieve a sample from the storer
        
        :param id: str
        :type id: str
        :return: A Sample object
        """
        
        return self.storer.retrieve(id)
    
    def update(self, sample: Sample) -> Sample:
        """
        > Update the sample in the storer and searcher
        
        :param sample: Sample
        :type sample: Sample
        :return: The new sample.
        """
        new_sample = self.storer.update(sample)
        self.searcher.update(sample)
        
        return new_sample
    
    
    def find_by_url(self, url: str) -> Sample:
        """
        It returns a sample object from the storer object, which is a class that inherits from the
        storer class
        
        :param url: str
        :type url: str
        """
        
        return self.storer.find_by_url(url)
    
    def search_similar(self, sample : Sample) -> list:
        """
        > This function takes a sample and returns a list of similar samples
        
        :param sample: Sample
        :type sample: Sample
        :return: A list of samples that are similar to the sample passed in.
        """
        
        return self.searcher.search_similar(sample)
