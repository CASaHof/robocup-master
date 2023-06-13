class Token:
    UUID:str = ""
    type:str = "none"

    def __init__(self,UUID:str,type:str) -> None:
        self.UUID = UUID
        self.type = type

class CameraClient(Token):
    def __init__(self,UUID:str) -> None:
        super().__init__(UUID,"client")

class TeamClient(Token):
    def __init__(self,UUID:str) -> None:
        super().__init__(UUID,"team")

class WebClient(Token):
    def __init__(self,UUID:str) -> None:
        super().__init__(UUID,"web")

CASTOKEN = {
    "po1JTmRxNCQOCLn7MJAT": CameraClient("CameraClient-1"),
    "hm1qUiCgRG9L3pLmvEgW": CameraClient("CameraClient-2"),
    "WOtEpKyRaD3cLKIcQG5J": CameraClient("CameraClient-3"),
    "gegsqIDA0HKwRygxPNpU": TeamClient("TeamClient-1"),
    "tXXdFi3IDsRU3tjOTm9S": TeamClient("TeamClient-2"),
    "61OfXnt2prlDjM2xUb3S": WebClient("WebClient"),
}