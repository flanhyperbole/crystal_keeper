from dataclasses import dataclass, field
import re
import uuid
from abc import abstractmethod
from typing import Any, Protocol, Optional
from functools import wraps

import secretstorage

import yaml

# defines the structural information that must be contained in a shard
# allows consitency across interfaces, and should be held in order
# shard:
#   structure: #key:value pairs in the lookup mechanisim of the crystal.
#     requred:
#       label: 'human readable name'
#       uniqueId: 'label_snakecase_by_default'
#       scope: 
#         - local
#         - remote
#       type:
#         - config # general info that we want to sync, but isn't as sensitive
#         - environment # infrormation that we'd like to include in an environment for general use 
#         - secret # passwords, usernames, keys etc
#         - unknowable # extra layer of security here, probably cannot be accessed without a pw prompt similar, not for general secret -> app use
#     optional:
#       related: 'name of an app or service you want to relate for ease  of grouping'
#       collection: 'antoher name for ease of grouping'


@dataclass
class Shard:
    secret: str
    label: str
    uuid: uuid.UUID
    scope: str
    type: str
    related: Optional[str] = None
    collection: Optional[str] = None

    


class AbstractCrystal(Protocol):
    connection = Any #function to connect to resource, must destroy connection after use
    shard_map = [Shard] #list of currently accessed secrets 
    
    def labelCheck(self, label: str) -> bool:
        if re.search('/W', label):
            raise Exception(f"""
                Label can only contain lowercase alphanumerics 
                and underscores. Labels are lowered() and have 
                spaces replaced with "_" before this check is run. 
                Label checked: {label}""")
        return True    

    @abstractmethod
    def connectionWrapper(function):
        """ wrap the functions connecting to the resource, disconnecting after use"""

    @abstractmethod
    def setSecret(label: str, scope: str, type: str, related: str = None, collection: str = None) -> Shard:
        """ sets the secret with the above requred and optional settings"""

    @abstractmethod
    def getSecret(*args, **kwargs) -> Shard:
        """ set a set of arguments return the corresponding secret"""

    @abstractmethod 
    def destroyMethod(uuid) -> None:
        """ remove secret from storage"""



def connectFuncHome():
    conn = secretstorage.dbus_init()
    assert secretstorage.check_service_availability(conn), 'secrect service is nor running'
    return conn
    
    # collection = secretstorage.get_default_collection(conn)
    # return collection


class HomeCrystal(AbstractCrystal):
    def __init__(self, connect_function = connectFuncHome) -> None:
        self.connect = connect_function
        self.shard_map = {}

    def connectionWrapper(self, function):
        with self.connect_function() as conn:
            @wraps(function)
            def with_connection_context(*args, **kwargs):
                kwargs.add(conn=conn)
                function(*args, **kwargs)
        return with_connection_context

    def parseToShard(cls, _item: secretstorage.item.Item):
        return Shard(_item.get_secret()
        , _item.get_label()
        , uuid.UUID(_item.get_attributes()['uuid'])
        , _item.get_attributes()['scope']
        , _item.get_attributes()['type']
        , _item.get_attributes().get('related')
        , _item.get_attributes().get('collection'))

    def currentShardsCheck(self, lookup, value):
        checklist = [i.__dict__[lookup] for i in self.shard_map]
        if value in checklist and (_idx := checklist.index(value)) >=0:
            return self.shard_map[_idx]
        return False

    def setSecret(self, secret, label: str, scope: str, type: str, related: str = None, collection: str = None):
        _attrs = {
            "scope": scope 
            , "type": type
            , "related": related
            , "collection": collection 
        }
        _attrs = {k:v for k,v in _attrs.items() if v is not None}
        label = label.lower().replace(' ', '_')
        self.labelCheck(label)
        shard = self.currentShardsCheck('label', label)
        with self.connect() as conn:
            collection = secretstorage.get_default_collection(conn)
            if shard:
                pass
            else:
                _uuid = uuid.uuid4()
                _attrs.update({'uuid':str(_uuid)})
                #  collection.create_item('My first item', attributes, b'pa$$word')
                secret_obj = collection.create_item(label, _attrs, secret)
                shard = self.parseToShard(secret_obj)
        return shard

    def getSecret():
        pass

    def destroyMethod(uuid) -> None:
        pass


class Keeper:
    """the interface to local secret storage"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_crystal(name: str = 'homeCrystal'):
        if name == 'homeCrystal':
            return HomeCrystal()


    def do(self):
        homeCrystal = Keeper.get_crystal()
        shard = homeCrystal.setSecret('gremlins', 'test', 'cope',  'type')
        print(shard)
        print('just for while we debug, no?')