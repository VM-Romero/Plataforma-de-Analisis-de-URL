from model import Representation, Sample, IndexableItem, LabelInfo
import requests
import base64
from urllib.parse import urlparse # para conseguir el hostname dada la url
import socket # para saber la ip de un sitio web
from tld import get_tld # get top level domain
import json
import whois


# SampleAnalyzer (clase interfaz)
class SampleAnalyzer:
    
    def initialize(self, name: str, configuration: dict):
        """
        Arguments
        ----------
        name: str
            Nombre del analizador a inicializar
            
        configuration: dict
            Diccionario con parámetros de configuración
            
        Return
        ---------- 
            Inicializa el analizador name.
        """
    
    def analyze(self, sample: Sample) -> list:
        """
        Arguments
        ----------
        sample: Sample
            Sample a analizar
            
        Return
        ----------
        list
            Lista de representaciones del sample
        """


# VirusTotalAnalyzer
class VirusTotalAnalyzer(SampleAnalyzer):
    
    def initialize(self, name, configuration):
        """
        The function takes in a name and a configuration dictionary, and sets the name and API_KEY
        attributes of the object.
        
        :param name: The name of the module
        :param configuration: A dictionary containing the configuration parameters for the extension
        """
        
        self.name = name
        
        # clave de mi cuenta en la API de VirusTotal
        self.API_KEY = configuration['virustotal_api_key']
        
        
    def analyze(self, sample) -> list:
        """
        > We create a list of representations, 
        we get the URL ID from the sample, 
        we make a request to
        VirusTotal, we create two representations, 
        we load the data from the response into the
        representations, and we return the list of representations
        
        :param sample: the sample to be analyzed
        :return: A list of representations.
        """
        self.sample = sample
        
        result = [] # lista de representaciones
        
        url_id = base64.urlsafe_b64encode(sample.url.encode()).decode().strip("=") # id de la url del sample
        
        url = "https://www.virustotal.com/api/v3/urls/{}".format(url_id)

        headers = {"accept": "application/json",
                   "x-apikey": self.API_KEY
                   }
        try:
            response = requests.get(url, headers=headers)
            
            vt_analysis = VirusTotalAnalysisRepresentation("VT analysis", "Analysis for {}".format(sample.url))
            vt_analysis.load_from_VT_response(response.json())
            
            result.append(vt_analysis)

            vt_info = VirusTotalInfoRepresentation("VT info", "Info of {}".format(sample.url))
            vt_info.load_from_VT_response(response.json())
            
            result.append(vt_info)
        except:
            print("ERROR VT")
        
        return result
    
# VirusTotalAnalysisRepresentation
class VirusTotalAnalysisRepresentation(Representation):
    
    def __init__(self, name, description):
        """
        The __init__ function is a special function in Python classes. 
        It is used to initialize the
        attributes of the class.
        
        :param name: The name of the representation
        :param description: A string that describes the representation
        """
        Representation.__init__(self, name, description)
        self.name = name
        self.description = description
    
    def load_from_VT_response(self, response):
        """
        It takes a VirusTotal response and creates three lists: 
        
        - positive: a list of the names of the engines that detected the 
                    file as malicious
        - negative: a list of the names of the engines that detected the 
                    file as benign
        - unrated: a list of the names of the engines that did not detect the 
                    file as malicious or benign
        
        The function is a little more complicated than that, but that's the gist of it. 
        
        Let's see how it works. 
        
        First, we'll create a VirusTotal object and use it to scan a file. 
        
        Then, we'll use the function to create the three lists. 
        
        Finally, we'll print the lists.
        
        :param response: The response from VirusTotal
        """
        #positive = [] # maliciosos
        self.negative = [] # benignos
        self.unrated = [] # sin calificar
        self.positive = [] #malignos
        
        for entry in response["data"]["attributes"]["last_analysis_results"].values():
            if entry["result"] == "clean":
                self.negative.append(entry["engine_name"])
            elif entry["result"] == "unrated":
                self.unrated.append(entry["engine_name"])
            # todo lo que no sea clean o unrated es malware, phising, 
            # malicious, suspicious o spam, los cuales pueden 
            # considerarse como positivo
            else:
                self.positive.append(entry["engine_name"])
        
    def get_indexable_items(self) -> list:
        """
        It takes a list of strings, replaces the spaces with underscores, and returns a list of
        IndexableItem objects
        :return: A list of IndexableItem objects.
        """
        
        result = []
        
        result.append(IndexableItem("positive_engines", [x.replace(" ","_") for x in self.positive]))
        
        result.append(IndexableItem("negative_engines", [x.replace(" ","_") for x in self.negative]))
 
        result.append(IndexableItem("unrated_engines", [x.replace(" ","_") for x in self.unrated]))
        
        return result
    
    def has_label_info(self) -> bool:
        """
        This function returns True if the label information is available for the given image
        :return: True
        """
        
        return True
    
    def get_label_info(self) -> LabelInfo:
        """
        If there are more positive labels than negative labels, return "positive" as the label and
        "unknown" as the confidence. If there are more negative labels than positive labels, return
        "negative" as the label and "unknown" as the confidence. If there are an equal number of
        positive and negative labels, return "unknown" as the label and "unknown" as the confidence.
        :return: LabelInfo("positive", "unknown")
        """
        
        if len(self.positive) > len(self.negative):
            return LabelInfo("positive", "unknown")
        
        if len(self.positive) < len(self.negative):
            return LabelInfo("negative", "unknown")
        
        return LabelInfo("unknown", "unknown")
            
            
    
# VirusTotalInfoRepresentation
class VirusTotalInfoRepresentation(Representation):
    
    def __init__(self, name, description):
        """
        The __init__ function is a special function in Python classes. 
        It is used to initialize the attributes of the class.
        
        :param name: The name of the representation
        :param description: A string that describes the representation
        """
        Representation.__init__(self, name, description)
        self.name = name
        self.description = description

    def load_from_VT_response(self, response):
        """
        This function takes in a VirusTotal response and 
        extracts the categories of the file.
        
        :param response: The response from VirusTotal
        """
        
        self.categories = list(response["data"]["attributes"]["categories"].values())
        
    
    def get_indexable_items(self) -> list:
        """
        It returns a list of IndexableItem objects, which are basically a tuple of (field_name,
        field_value)
        :return: A list of IndexableItem objects.
        """
        
        result = []
        
        # hay que volverlo "procesable" para Elasticsearch
        result.append(IndexableItem("categories", [x.replace(" ","_") for x in self.categories]))
        
        return result
        
    
    def has_label_info(self) -> bool:
        """
        It returns a boolean value.
        :return: False
        """

        return False
        

# BasicAnalyzer

class BasicAnalyzer(SampleAnalyzer):
    def initialize(self, name, configuration):
        """
        This function is called when the extension is initialized.
        
        :param name: The name of the plugin
        :param configuration: A dictionary containing the parameters for the algorithm
        """
        
        self.name = name
        
    def analyze(self, sample) -> list:
        """
        > The function takes a sample as input and returns a list of representations
        
        :param sample: the sample to be analyzed
        :return: A list of BasicRepresentation objects.
        """
        result = []
        basic_info = BasicRepresentation("Basic info", "Basic info of {}".format(sample.url))
        
        #url
        basic_info.url = sample.url
        
        # ip address
        url_parsed = urlparse(sample.url)
        
        ip_add = socket.gethostbyname(url_parsed.hostname) # tiene que ser con el hostname
        basic_info.ip_add = ip_add
        
        # geographic location
        response = requests.get(f'https://ipapi.co/{ip_add}/json/').json()
        location_json = {
            "country": response.get("country_name")
        }
        
        geo_loc = location_json["country"] # geo_loc tiene que ser string
        if geo_loc == "null" or geo_loc is None:
            geo_loc = "unknown"
        basic_info.geo_loc = geo_loc
        
        # url length
        url_len = len(sample.url)
        basic_info.url_len = url_len
        
        # top level domain 
        tld = get_tld(sample.url)
        basic_info.tld = tld
        
        # who is domain complete or incomplete ¿¿¿¿a que se refiere con completo o incompleto????
        wi = whois.whois(url_parsed.hostname)
        #who_is = wi.text
        '''
        Whois saca:
            - domain_name
            - registrar
            - whois_server !!!!
            - referral_url
            - updated_date
            - creation_date
            - expiration_date
            - name_servers !!!!
            - status
            - emails
            - dnssec
            - name
            - org !!!!
            - address
            - city
            - state !!!!
            - registrant_postal_code
            - country
        '''
        whois_server = wi["whois_server"]
        org = wi["org"]
        state = wi["state"]
        
        # name_servers da problemas porque es una lista y no un string
        l_whois = [whois_server, org, state]
        
        basic_info.l_whois = l_whois
 
        # https or http
        if sample.url.startswith("https"):
            https = "yes"
        else:
            https = "no"
            
        basic_info.https = https
            
        # raw webpage content
        response = requests.get(sample.url)
        content = response.text
        
        basic_info.content = content
        
        label = "unknown"
            
        basic_info.label = label
        
        result.append(basic_info)
        
        return result
   

# BasicRepresentation
class BasicRepresentation(Representation):
    
    def __init__(self, name, description):
        """
        The __init__ function is a special function in Python classes. 
        It is used to initialize the attributes of the class
        
        :param name: The name of the representation
        :param description: A string that describes the representation
        """
        Representation.__init__(self, name, description)
        self.name = name
        self.description = description
    
    def get_indexable_items(self) -> list:
        """
        It takes a list of strings and returns a list of IndexableItem objects
        :return: A list of IndexableItem objects.
        """
        
        result = []
        
        result.append(IndexableItem("basic-url", [self.url]))
        result.append(IndexableItem("basic-ip", [self.ip_add]))
        result.append(IndexableItem("basic-geo_loc", [self.geo_loc]))
        result.append(IndexableItem("basic-tld", [self.tld]))
        result.append(IndexableItem("basic-whois", self.l_whois))
        result.append(IndexableItem("basic-https", [self.https]))
        result.append(IndexableItem("basic-content", [self.content]))
        result.append(IndexableItem("basic-label", [self.label]))
    
        return result
    
    def has_label_info(self) -> bool:
        """
        This function returns True if the label information is available for the given image
        :return: True
        """
        
        return True
    
    def get_label_info(self) -> LabelInfo:
        """
        It returns a LabelInfo object with the label and the label type
        :return: LabelInfo(self.label, "unknown")
        """
        
        return LabelInfo(self.label, "unknown")
