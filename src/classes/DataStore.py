from CASTOKEN import CameraClient


class DataStore(object):
    _instance = None

    data = {
        "clients": {},
        "teamServer": {},
        "webClient": {},
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def setBalls(self,balls):
        self.data["balls"] = balls

    def setRobots(self,robots):
        self.data["robots"] = robots

    def checkClient(self,id:str):
        return id in self.data["clients"]

    def addWebClient(self,id:str,websocket,user):
        if not self.checkClient(id):
            self.data["webClient"][id] = {
                "websocket":websocket,
                "user":user
            }
        return self.data["webClient"][id]
        
    def addClient(self,id:str,websocket,user):
        if not self.checkClient(id):
            self.data["clients"][id] = {
                "websocket":websocket,
                "user":user
            }
        return self.data["clients"][id]
        
    def addTeamServer(self,id:str,websocket,user):
        if not self.checkClient(id):
            self.data["teamServer"][id] = {
                "websocket":websocket,
                "user":user
            }
        return self.data["teamServer"][id]
        
    def removeClient(self,id:str):
        if self.checkClient(id):
            del self.data["clients"][id]
    
    def getClient(self,id:str) -> CameraClient:
        if self.checkClient(id):
            return self.data["clients"][id]["user"]
        return None
    
    def getTeamServerClients(self) -> CameraClient:
        return self.data["teamServer"]

    def getWebClients(self) -> CameraClient:
        return self.data["webClient"]
