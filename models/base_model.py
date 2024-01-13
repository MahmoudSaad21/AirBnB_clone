"""Defines all common attributes/methods for other classes
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Base class for all models"""
    def __init__(self):
        """Initialization of a Base instance."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Returns a readable string representation
        of BaseModel instances"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary that contains all
        keys/values of the instance"""
        model_dict = self.__dict__.copy()
        model_dict['__class__'] = self.__class__.__name__
        model_dict['created_at'] = self.created_at.isoformat()
        model_dict['updated_at'] = self.updated_at.isoformat()
        return model_dict
