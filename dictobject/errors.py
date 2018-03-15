from collections import Mapping, Sequence
from inspect import isclass

import six

from . import errors


class DictObject(dict):
    '''
    Store data as a dictionary but expose it as attributes.
    Offer basic validation of data by checking presence of fields.
    Uses an opportunistic duck-typing algorithm to determine type of nested structures.
    '''
    
    MANDATORY_FIELDS = ()
    OPTIONAL_FIELDS = ()
    
    def __init__(self, data=None):
        'Takes either nothing or a dict-like.'
        
        if data:
            self.assert_fields(data) #raise exception if bad
            
            super(DictObject, self).__init__((k,v) for k,v in data.iteritems() if not isinstance(v, Mapping))
            
            for k,v in data.iteritems():
                self.set_recursive(k, v)
        else:
            super(DictObject, self).__init__()
    
    def __setitem__(self, key, value):
        if key in self.MANDATORY_FIELDS or key in self.OPTIONAL_FIELDS:
            if not self.set_recursive(key, value):
                super(DictObject, self).__setitem__(key, value)
        else:
            raise errors.SuperfluousFields([key])
    
    def set_recursive(self, key, value):
        if isinstance(value, Mapping):
            super(DictObject, self).__setitem__(key, self.find_applicable_nested_class(value)(value))
        elif isinstance(value, Sequence) and not isinstance(value, six.string_types):
            super(DictObject, self).__setitem__(key, [self.find_applicable_nested_class(i)(i) for i in value])
        elif isinstance(value, DictObject):
            super(DictObject, self).__setitem__(key, value)
        else:
            return False
        
        return True
    
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, value):
        if key in self.__dict__: #bypass magic
            super(DictObject, self).__setattr__(key, value)
        else:
            self.__setitem__(key, value)
    
    @classmethod
    def find_applicable_nested_class(cls, data):
        for ncls in (v for k,v in cls.__dict__.iteritems() if isclass(v) and issubclass(v,DictObject)):
            if ncls.check_fields(data):
                return ncls
        
        raise errors.NoNestedClassFound(cls, data.keys())
    
    @classmethod
    def check_fields(cls, data):
        try:
            cls.assert_fields(data)
        except errors.DataStructureError:
            return False
        else:
            return True
    
    @classmethod
    def assert_fields(cls, data):
        missed_mandatory_fields = set(cls.MANDATORY_FIELDS) - set(data.keys())
        if missed_mandatory_fields:
            raise errors.MissingMandatoryFields(missed_mandatory_fields)
        
        extra_fields = set(data.keys()) - set(cls.MANDATORY_FIELDS + cls.OPTIONAL_FIELDS)
        if extra_fields:
            raise errors.SuperfluousFields(extra_fields)
