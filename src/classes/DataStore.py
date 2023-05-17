class DataStore(object):
    _instance = None

    data = {
        "clients": {},
        "teamServer": {},
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def setBalls(self,balls):
        self.data["balls"] = balls

    def setRobots(self,robots):
        self.data["robots"] = robots

    def checkClient(self,id):
        return id in self.data["clients"]

    def addClient(self,id,websocket,user):
        if not self.checkClient(id):
            self.data["clients"][id] = {
                "websocket":websocket,
                "user":user
            }
        return self.data["clients"][id]
        
    def removeClient(self,id):
        if self.checkClient(id):
            del self.data["clients"][id]
    
    def getClient(self,id):
        if self.checkClient(id):
            return self.data["clients"][id]["user"]
        return None
