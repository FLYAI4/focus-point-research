from enum import Enum

class TTSErrorCode(Enum):
    NonTokenError = {
    "code": 401,
    "message": "Failed to connect. Contact service administrator.",
    "log": "Focus Point API request error with non token. Please purchase token."
    }
    APIError = {
        "code": 500,
        "message": "Failed to request. Contact service administrator.",
        "log": "API Error. Please check api."
    }




class FocusPointErrorCode(Enum):
    NonImageError = {
        "code": 400,
        "message": "The ID is no image. Please image upload again.",
        "log": "Focus Point API request error with non image."
    }
    NonTokenError = {
        "code": 404,
        "message": "Failed to connect. Contact service administrator.",
        "log": "Focus Point API request error with non token. Please purchase token."
    }
    UnknownError = {
        "code": 500,
        "message": "Failed to connect. Contact service administrator.",
        "log": "Unkonw focus point error. Please check error log."
    }
    APIError = {
        "code": 500,
        "message": "Failed to request. Contact service administrator.",
        "log": "API Error. Please check api."
    }