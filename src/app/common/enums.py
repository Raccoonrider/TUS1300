from enum import IntEnum

def translate(text:str):
    match(text):
        case "M":
            return "Мужской"
        case "F":
            return "Женский"
    return text

class BaseEnum(IntEnum):
    @classmethod
    def choices(cls):
        return tuple((i.value, translate(i.name)) for i in cls)

    @classmethod
    def test_int(cls, n:int):
        return n in iter(cls)

    @classmethod
    def name_int(cls, n:int):
        if cls.test_int(n):
            return cls(n).name
        else:
            return '-'        

class Gender(BaseEnum):
    M = 1
    F = 2

class ResultStatus(BaseEnum):
    OK = 0
    OTL = 1
    DNF = 2
    DSQ = 3

class Category(BaseEnum):
    Default = 0
    Elite = 1
    Junior = 2
    EliteW = 3