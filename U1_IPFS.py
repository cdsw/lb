import ipfshttpclient as ip
from os import remove
from tensorflow.python.keras.models import load_model
import pickle as pkl

class IPFS:
    def __init__(self, id_):
        self.id_ = id_
        self.cli = ip.connect()
        self.id = self.cli.id()['ID']
    
    def sendToIPFS(self, file_loc):
        res = self.cli.add(file_loc)
        hash_ = res['Hash']
        del res
        return hash_
    
    def getFromIPFS(self, hash_, destination):
        self.cli.get(hash_, destination)

    def close(self):
        self.cli.close()

def saveToFile(content, location):
    f = open(location, 'w')
    f.write(content)
    f.close()
    return location

def readFromFile(location):
    f = open(location, 'r')
    g = f.read()
    f.close()
    return g

def IPFStoObj(ipfs_obj, hash_, location):
    ipfs_obj.getFromIPFS(hash_, location)
    obj_ = readFromFile(location + hash_)
    remove(location + hash_)
    return obj_

def IPFStoModObj(ipfs_obj, hash_, location):
    ipfs_obj.getFromIPFS(hash_, location)
    obj_ = load_model(location + hash_)
    remove(location + hash_)
    return obj_

def objToIPFS(ipfs_obj, obj_, location):
    saveToFile(obj_, location + 'temp')
    hash_ = ipfs_obj.sendToIPFS(location + 'temp')
    remove(location + 'temp')
    return hash_

def objPickleToIPFS(ipfs_obj, obj_, location):
    pkl.dump(obj_, open(location + 'temp', 'wb'))
    hash_ = ipfs_obj.sendToIPFS(location + 'temp')
    remove(location + 'temp')
    return hash_

def IPFStoPickleObj(ipfs_obj, hash_, location):
    ipfs_obj.getFromIPFS(hash_, location)
    obj_ = pkl.load(open(location + hash_, 'rb'))
    remove(location + hash_)
    return obj_
