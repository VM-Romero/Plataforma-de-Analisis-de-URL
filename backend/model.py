from datetime import datetime
import enum

#Sample
class Sample:
    
    def __init__(self, url: str):
        """
        This function takes a url as a string and creates a new Sample object 
        with the url, id,creation_date, analysis_date, sample_status, 
        and representations attributes
        
        :param url: The URL of the sample
        :type url: str
        """

        self.url = url
        self.id = None
        self.creation_date = datetime.now()
        self.analysis_date = datetime.now()
        self.sample_status = SampleStatus.PROCESSING
        self.representations = []
        
#LabelInfo
class LabelInfo:
    
    def __init__(self, label: str, sub_label: str):
        """
        The function __init__() is a constructor that initializes the 
        class with the label and sub_label
        attributes
        
        :param label: The label of the button
        :type label: str
        :param sub_label: The sub-label of the label
        :type sub_label: str
        """
        
        self.label = label
        self.sub_label = sub_label
    
#Representation
class Representation:
    
    def __init__(self, name: str, description: str):
        """
        The function __init__() is a special function in Python classes. 
        It is run as soon as an object
        of a class is instantiated. The method __init__() 
        is analogous to constructors in C++ and Java
        
        :param name: The name of the item
        :type name: str
        :param description: A description of the parameter
        :type description: str
        """
        
        self.name = name
        self.description = description
        
    def get_indexable_items(self) -> list:
        """
        Arguments
        ----------
        None
        
        Return
        ----------
        list
            Lista de indexable items
        """
    
    def has_label_info(self) -> bool:
        """
        Arguments
        ----------
        None
        
        Return
        ----------
        bool
            Si hay o no informacion de la etiqueta
        """
    
    def get_label_info(self) -> LabelInfo:
        """
        Arguments
        ----------
        None
        
        Return
        ----------
        LabelInfo
            Elemento
        """
    
#IndexableItem
class IndexableItem:
    
    def __init__(self, name: str, values: list):
        """
        The function takes in two arguments, a string and a list, 
        and assigns them to the attributes
        name and values, respectively.
        
        :param name: The name of the column
        :type name: str
        :param values: A list of values that the column can take on
        :type values: list
        """
        
        self.name = name
        self.values = values
        

#SampleStatus
# The SampleStatus class is an enumeration of the possible statuses of a sample
class SampleStatus(enum.Enum):
    PROCESSING = 3
    ANALYZED = 2
    INDEXED = 1
    ERROR = 0
