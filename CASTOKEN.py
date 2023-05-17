class Token:
    UUID:str = ""
    type:str = "none"

    def __init__(self,UUID:str,type:str) -> None:
        self.UUID = UUID
        self.type = type

class Client(Token):
    def __init__(self,UUID:str) -> None:
        super().__init__(UUID,"client")

CASTOKEN = {
    "po1JTmRxNCQOCLn7MJAT": Client("Client-1"),
    "hm1qUiCgRG9L3pLmvEgW": Client("Client-2")
}