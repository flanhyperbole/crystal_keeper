import secretstorage
import yaml


def CrystalConnect(Protocol):
    pass

def connectFuctHome():
    conn = secretstorage.dbus_init()
    assert secretstorage.check_service_availability(conn), 'secrect service is nor running'
    collection = secretstorage.get_default_collection(conn)
    return collection

class Crystal:
    def __init__(self, connectFunc):
        self.connection = connectFuctHome




class Keeper:
    """the interface to local secret storage"""
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_crystal(name: str = 'homeCrystal'):
        if name == 'homeCrystal':
            return Crystal()


    def do(self):
        print('just for while we debug, no?')